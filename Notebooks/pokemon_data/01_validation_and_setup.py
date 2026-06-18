# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE CATALOG IF NOT EXISTS pokemon_catalog;
# MAGIC CREATE SCHEMA IF NOT EXISTS pokemon_catalog.01_bronze;
# MAGIC CREATE SCHEMA IF NOT EXISTS pokemon_catalog.02_silver;
# MAGIC CREATE SCHEMA IF NOT EXISTS pokemon_catalog.03_gold;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW SCHEMAS IN pokemon_catalog;

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG pokemon_catalog;
# MAGIC CREATE VOLUME IF NOT EXISTS bronze.exports;
# MAGIC CREATE VOLUME IF NOT EXISTS bronze.raw_data;
# MAGIC CREATE VOLUME IF NOT EXISTS silver.exports;
# MAGIC CREATE VOLUME IF NOT EXISTS gold.exports;

# COMMAND ----------

# DBTITLE 1,Tree View
catalog_name = "pokemon_catalog"
exclude_schemas = {"information_schema", "default"}
layer_order = ["01_bronze", "02_silver", "03_gold"]

spark.sql(f"USE CATALOG {catalog_name}")

schemas = [row.databaseName for row in spark.sql(f"SHOW SCHEMAS IN {catalog_name}").collect()]
schemas = [s for s in schemas if s not in exclude_schemas]
schemas.sort(key=lambda s: (layer_order.index(s) if s in layer_order else len(layer_order), s))

print(f"📁 {catalog_name}")
for schema in schemas:
    print(f"  📂 {schema}")

    try:
        tables = sorted(row.tableName for row in spark.sql(f"SHOW TABLES IN {catalog_name}.{schema}").collect())
        if tables:
            print("    Tables:")
            for table in tables:
                print(f"      📄 {table}")
    except Exception as e:
        print(f"    Tables: ⚠️ {e}")

    try:
        volumes = sorted(row.volume_name for row in spark.sql(f"SHOW VOLUMES IN {catalog_name}.{schema}").collect())
        if volumes:
            print("    Volumes:")
            for volume in volumes:
                print(f"      💾 {volume}")
    except Exception as e:
        print(f"    Volumes: ⚠️ {e}")

    try:
        views = sorted(row.viewName for row in spark.sql(f"SHOW VIEWS IN {schema}").collect())
        if views:
            print("    Views:")
            for view in views:
                print(f"      👁️ {view}")
    except Exception as e:
        print(f"    Views: ⚠️ {e}")

    try:
        functions = sorted(row.function for row in spark.sql(f"SHOW USER FUNCTIONS IN {catalog_name}.{schema}").collect())
        if functions:
            print("    Functions:")
            for function in functions:
                print(f"      🔧 {function}")
    except Exception as e:
        print(f"    Functions: ⚠️ {e}")