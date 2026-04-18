from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.connectors.kafka import KafkaSource
from pyflink.datastream.connectors.jdbc import JdbcSink
from pyflink.common.watermark_strategy import WatermarkStrategy
import json
import os


BOOTSTRAP_SERVER = os.environ.get("BOOTSTRAP_SERVER", "locklahost:9092")
REGION = os.environ.get("REGION", "mai")

CLICKHOUSE_URL = os.environ.get("CLICKHOUSE_URL", "jdbc:clickhouse://clickhouse:8123/default")

CLICKHOUSE_USER = os.environ.get("CLICKHOUSE_USER", "default")
CLICKHOUSE_PASS = os.environ.get("CLICKHOUSE_PASS", "pass")

CLICKHOUSE_DRIVER = os.environ.get("CLICKHOUSE_DRIVER", "com.clickhouse.jdbc.ClickHouseDriver")


class FlinkETL:
    def __init__(self):
        self.env = StreamExecutionEnvironment.get_execution_environment()
        self.env.set_parallelism(1)
    def transform(self, value: str):
        try:
            data = json.loads(value)

            return (
                data["device_id"],
                int(data.get("time", 0)),
                float(data.get("x", 0)),
                float(data.get("y", 0))
            )

        except Exception:
            return None

    def etl(self):
        source = KafkaSource.builder() \
            .set_bootstrap_servers(BOOTSTRAP_SERVER) \
            .set_topics(REGION) \
            .set_group_id("flink-group") \
            .set_value_only_deserializer(SimpleStringSchema()) \
            .build()

        stream = self.env.from_source(
            source=source,
            watermark_strategy=WatermarkStrategy.no_watermarks(),
            source_name="kafka"
        )

        clean_stream = stream \
            .map(self.transform) \
            .filter(lambda x: x is not None)
        props = {
            "user": CLICKHOUSE_USER,
            "password": CLICKHOUSE_PASS
        }

        sink = JdbcSink.sink(
            f"""
            INSERT INTO point_{REGION}
            (device_id, time, x, y)
            VALUES (?, ?, ?, ?)
            """,
            lambda ps, t: (
                ps.set_string(1, t[0]),
                ps.set_long(2, t[1]),
                ps.set_double(3, t[2]),
                ps.set_double(4, t[3])
            ),
            jdbc_url=CLICKHOUSE_URL,
            driver_name=CLICKHOUSE_DRIVER,
            jdbc_properties=props
        )

        clean_stream.add_sink(sink)

        self.env.execute("Kafka → Flink ETL → ClickHouse")


flink_etl = FlinkETL()
flink_etl.etl()

