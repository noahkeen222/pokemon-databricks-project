# Databricks notebook source
# MAGIC %md
# MAGIC # Raw to Bronze strategy
# MAGIC - Clean and load data onto unstructured table

# COMMAND ----------

import pandas as pd

# COMMAND ----------

# DBTITLE 1,Read File
pokemon = pd.read_csv("/Volumes/pokemon_catalog/01_bronze/raw_data/Pokemon.csv")
print(pokemon.head())

# COMMAND ----------

print(f"Shape:\n{pokemon.shape}\n\nNulls:\n{pokemon.isnull().sum()}\n\nDuplicates:\n{pokemon.duplicated().sum()}")

# COMMAND ----------

(spark.createDataFrame(pokemon)).write.format("delta").mode("overwrite").saveAsTable("pokemon_catalog.01_bronze.pokemon")

# COMMAND ----------

# DBTITLE 1,Verify Count
print("Did this work:", f"YES\n{spark.table("pokemon_catalog.01_bronze.pokemon").head()}\n" if len(pokemon) == spark.table("pokemon_catalog.01_bronze.pokemon").count() else "no")

try:
    print(f"\n\n{spark.table('pokemon_catalog.01_bronze.pokemon').printSchema()}")
except Exception as e:
    print(e)