Automated Central Bank Currency Data Pipeline (Azure Gen2 & Databricks)

An end-to-end data engineering pipeline automating daily exchange rate ingestion (USD, EUR, RUB to UZS) from **The Central Bank of the Republic of Uzbekistan** into a retail analytics platform. 

This project demonstrates an architectural migration from **Microsoft Azure Infrastructure** to a scalable **Databricks Lakehouse**.

---

Architecture & Core Pipeline Steps

### Step 1: Staging & Warehousing (Microsoft Azure)
* **Ingestion Layer:** Provisioned **Azure Data Lake Storage (ADLS) Gen2** for raw blob file storage.
* **Warehouse Layer:** Deployed **Azure SQL Database** (`dwh-retail-analytics`).
* **Initial Setup:** Executed baseline DDL scripts and built a standard SQL ELT loop script for staging data.

### Step 2: Data Lake Migration (Databricks Delta Lake)
* **Storage Engine:** Migrated target tables to **Delta Lake** to ensure ACID transactions.
* **Target Schema Setup:** Configured an explicit SQL DDL file (`ddl_setup.sql`) to define storage data types for the target exchange rates table.

### Step 3: Streamlined Processing (PySpark)
* **Engine:** Replaced manual SQL scripts with a dynamic **PySpark** ETL pipeline.
* **Schema Validation:** Defined strict boundaries using Spark schemas matching the Central Bank API payload structure.
* **Audit Fields:** Appended dynamic runtime processing markers using execution date variables.

### Step 4: Idempotent Storage Architecture (MERGE)
* **Data Integrity:** Programmed an upsert framework in the core pipeline script (`pyspark_pipeline.py`) to completely block duplicate entries from multi-run batch executions.
* **Pipeline Logic:** The Python script automatically registers the incoming data stream as a temporary view and triggers a SQL `MERGE` statement to update existing records or insert new rows.

### Step 5: Production Orchestration (Databricks Workflows)
* **Scheduler:** Built a dedicated workflow named `daily_exchange_rates_pipeline`.
* **Compute Layer:** Configured execution on an elastic, automated **Serverless Spark Cluster**.
* **Automation:** Set up an automated daily cron trigger scheduled to deploy every night at **00:00**.

