# Databricks notebook source
from pyspark.sql.functions import current_date
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
# 1. stimulate getting data (as from API)
raw_data = [
    ("USD", "US Dollar", 12850.00),  
    ("EUR", "Euro", 13950.00),
    ("RUB", "Russian Ruble", 136.10)
]
# 2. structure of data
schema = StructType([
    StructField("currency_code", StringType(), True),
    StructField("currency_name", StringType(), True),
    StructField("exchange_rate_uzs", DoubleType(), True)
])
# 3. create Spark DataFrame ,add date
df = spark.createDataFrame(raw_data, schema=schema)
df_with_date = df.withColumn("report_date", current_date())
display(df_with_date) # 4. result
# 1. Register the Spark DataFrame as a temporary SQL view so we can query it using SQL syntax
df_with_date.createOrReplaceTempView("current_api_rates")

# 2. Run an upsert (MERGE) operation to update existing rates or insert new ones into the Delta table
spark.sql("""
MERGE INTO silver_exchange_rates AS target
USING current_api_rates AS source
ON target.currency_code = source.currency_code AND target.report_date = source.report_date
WHEN MATCHED THEN
  UPDATE SET target.exchange_rate_uzs = source.exchange_rate_uzs
WHEN NOT MATCHED THEN
  INSERT (currency_code, currency_name, exchange_rate_uzs, report_date) 
  VALUES (source.currency_code, source.currency_name, source.exchange_rate_uzs, source.report_date)
""")

# 3. Print a success message to verify the pipeline execution finished without errors
print("Data successfully updated from the PySpark pipeline!")
