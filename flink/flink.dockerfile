FROM flink:1.18.1-scala_2.12-java11

USER root
RUN apt-get update \
    && apt-get install -y python3 python3-pip wget \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

RUN python3 -m pip install --upgrade pip setuptools wheel

RUN python3 -m pip install --no-cache-dir --default-timeout=300 \
    apache-flink==1.18.1 \
    kafka-python \
    psycopg2-binary

# ✅ Kafka connector (ok)
RUN wget -O /opt/flink/lib/flink-sql-connector-kafka-3.2.0-1.18.jar \
    https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.2.0-1.18/flink-sql-connector-kafka-3.2.0-1.18.jar

# 🔥 ДОБАВИТЬ ЭТО (главное)
RUN wget -O /opt/flink/lib/flink-connector-jdbc-3.1.2-1.18.jar \
    https://repo1.maven.org/maven2/org/apache/flink/flink-connector-jdbc/3.1.2-1.18/flink-connector-jdbc-3.1.2-1.18.jar

# ✅ ClickHouse driver
RUN wget -O /opt/flink/lib/clickhouse-jdbc-0.6.0.jar \
    https://repo1.maven.org/maven2/com/clickhouse/clickhouse-jdbc/0.6.0/clickhouse-jdbc-0.6.0.jar
# flink run -py /opt/flink/etl/flink_etl.py
USER flink