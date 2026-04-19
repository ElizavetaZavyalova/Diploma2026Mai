import os
import clickhouse_connect


class ClickhouseRepository:
    def __init__(self):
        self.client = clickhouse_connect.get_client(
            host=os.getenv("CLICKHOUSE_HOST", "clickhouse"),
            port=int(os.getenv("CLICKHOUSE_PORT", 8123)),
            username=os.getenv("CLICKHOUSE_USER", "default"),
            password=os.getenv("CLICKHOUSE_PASS", "clickhouse"),
            database=os.getenv("CLICKHOUSE_DB", "etl_data"),
        )

    def get_last_points(self, count: int, device_id: str, region="mai"):
        query = f"""
        SELECT
            device_id,
            time_signal,
            x,
            y
        FROM point_{region}
        WHERE device_id = %(device_id)s
        ORDER BY time_signal DESC
        LIMIT %(limit)s
        """

        result = self.client.query(
            query,
            parameters={
                "device_id": device_id,
                "limit": int(count)
            }
        )

        return [
            {
                "device_id": row[0],
                "time_signal": row[1],
                "x": row[2],
                "y": row[3],
            }
            for row in result.result_rows
        ]