DROP TABLE IF EXISTS etl_data.point_mai;

CREATE DATABASE IF NOT EXISTS etl_data;

CREATE TABLE etl_data.point_mai
(
    device_id String,
    time_signal UInt64,
    x Float64,
    y Float64
)
ENGINE = MergeTree
ORDER BY time_signal;