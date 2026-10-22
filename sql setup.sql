-- Databricks notebook source
CREATE TABLE IF NOT EXISTS silver_exchange_rates (
    currency_code STRING,
    currency_name STRING,
    exchange_rate_uzs DOUBLE,
    report_date DATE
)
USING DELTA;
