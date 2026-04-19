import json
import os
from datetime import datetime

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource
from pyflink.datastream.connectors.jdbc import (
    JdbcSink,
    JdbcConnectionOptions,
    JdbcExecutionOptions
)
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.watermark_strategy import WatermarkStrategy
from pyflink.common import Types, Row


# -------------------------
# ENV
# -------------------------
BOOTSTRAP_SERVER = os.environ.get("BOOTSTRAP_SERVER", "kafka:9092")
REGION = os.environ.get("REGION", "mai")

CLICKHOUSE_URL = os.environ.get(
    "CLICKHOUSE_URL",
    "jdbc:clickhouse://clickhouse:8123/etl_data"
)

CLICKHOUSE_USER = os.environ.get("CLICKHOUSE_USER", "default")
CLICKHOUSE_PASS = os.environ.get("CLICKHOUSE_PASS", "clickhouse")

CLICKHOUSE_DRIVER = os.environ.get(
    "CLICKHOUSE_DRIVER",
    "com.clickhouse.jdbc.ClickHouseDriver"
)


# -------------------------
# TRANSFORM
# -------------------------
def transform(value: str):
    try:
        data = json.loads(value)

        ts = data.get("time")
        time_ms = int(datetime.fromisoformat(ts).timestamp() * 1000)

        return Row(
            data["device_id"],
            time_ms,
            float(data.get("x", 0.0)),
            float(data.get("y", 0.0))
        )

    except Exception as e:
        print("DROP RECORD:", value, e)
        return None


# -------------------------
# MAIN
# -------------------------
def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)

    # -------------------------
    # Kafka Source
    # -------------------------
    source = KafkaSource.builder() \
        .set_bootstrap_servers(BOOTSTRAP_SERVER) \
        .set_topics(REGION) \
        .set_value_only_deserializer(SimpleStringSchema()) \
        .build()

    stream = env.from_source(
        source,
        WatermarkStrategy.no_watermarks(),
        "kafka-source"
    )

    # -------------------------
    # ROW TYPE (ВАЖНО: только ROW)
    # -------------------------
    row_type = Types.ROW([
        Types.STRING(),   # device_id
        Types.LONG(),     # time_signal
        Types.DOUBLE(),   # x
        Types.DOUBLE()    # y
    ])

    # -------------------------
    # Pipeline
    # -------------------------
    clean_stream = (
        stream
        .map(transform, output_type=row_type)
        .filter(lambda x: x is not None)
    )

    # -------------------------
    # JDBC Sink (ClickHouse)
    # -------------------------
    sink = JdbcSink.sink(
        f"""
        INSERT INTO point_{REGION}
        (device_id, time_signal, x, y)
        VALUES (?, ?, ?, ?)
        """,
        row_type,
        JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
            .with_url(CLICKHOUSE_URL)
            .with_driver_name(CLICKHOUSE_DRIVER)
            .with_user_name(CLICKHOUSE_USER)
            .with_password(CLICKHOUSE_PASS)
            .build(),
        JdbcExecutionOptions.builder()
            .with_batch_size(1000)
            .with_batch_interval_ms(200)
            .with_max_retries(3)
            .build()
    )

    # -------------------------
    # Sink attach
    # -------------------------
    clean_stream.add_sink(sink)

    env.execute("Kafka → Flink → ClickHouse ETL")


if __name__ == "__main__":
    main()