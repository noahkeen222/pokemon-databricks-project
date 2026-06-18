# Databricks notebook source
# MAGIC %md
# MAGIC # Bronze to Silver strategy
# MAGIC ## Tables:
# MAGIC - Normalize data by pk=number
# MAGIC     - number, name, typeID, statsID, metaID
# MAGIC     - typeID, type1, type2
# MAGIC     - statsID, total, hp, attack, defense, sp_attack, sp_defense, speed
# MAGIC     - metaID, generation, legendary

# COMMAND ----------

# MAGIC %md
# MAGIC #### Table Creation

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG pokemon_catalog;
# MAGIC USE SCHEMA `02_silver`;
# MAGIC
# MAGIC CREATE OR REPLACE TABLE types (
# MAGIC     typeID BIGINT GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
# MAGIC     type1 STRING NOT NULL,
# MAGIC     type2 STRING
# MAGIC );
# MAGIC
# MAGIC CREATE OR REPLACE TABLE meta (
# MAGIC     metaID BIGINT GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
# MAGIC     generation BIGINT NOT NULL,
# MAGIC     legendary BOOLEAN NOT NULL
# MAGIC );
# MAGIC
# MAGIC CREATE OR REPLACE TABLE stats (
# MAGIC     statID BIGINT NOT NULL PRIMARY KEY,
# MAGIC     hp BIGINT NOT NULL,
# MAGIC     attack BIGINT NOT NULL,
# MAGIC     defense BIGINT NOT NULL,
# MAGIC     sp_attack BIGINT NOT NULL,
# MAGIC     sp_defense BIGINT NOT NULL,
# MAGIC     speed BIGINT NOT NULL,
# MAGIC     total BIGINT GENERATED ALWAYS AS (hp + attack + defense + sp_attack + sp_defense + speed)
# MAGIC );
# MAGIC
# MAGIC CREATE OR REPLACE TABLE main (
# MAGIC     number BIGINT NOT NULL,
# MAGIC     name STRING NOT NULL UNIQUE,
# MAGIC     typeID BIGINT NOT NULL,
# MAGIC     statID BIGINT NOT NULL,
# MAGIC     metaID BIGINT NOT NULL,
# MAGIC     PRIMARY KEY (number),
# MAGIC     FOREIGN KEY (typeID) REFERENCES types(typeID),
# MAGIC     FOREIGN KEY (statID) REFERENCES stats(statID),
# MAGIC     FOREIGN KEY (metaID) REFERENCES meta(metaID)
# MAGIC );
# MAGIC
# MAGIC SHOW TABLES IN `02_silver`;

# COMMAND ----------

# MAGIC %md
# MAGIC #### Loading Data

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO types (type1, type2)
# MAGIC SELECT DISTINCT type1, type2
# MAGIC FROM pokemon_catalog.`01_bronze`.pokemon;
# MAGIC
# MAGIC INSERT INTO meta (generation, legendary)
# MAGIC SELECT DISTINCT generation, legendary
# MAGIC FROM pokemon_catalog.`01_bronze`.pokemon;
# MAGIC
# MAGIC INSERT INTO stats (statID, hp, attack, defense, sp_attack, sp_defense, speed)
# MAGIC SELECT number, hp, attack, defense, sp_attack, sp_defense, speed
# MAGIC FROM pokemon_catalog.`01_bronze`.pokemon;
# MAGIC
# MAGIC INSERT INTO main (number, name, typeID, statID, metaID)
# MAGIC SELECT
# MAGIC     b.number,
# MAGIC     b.name,
# MAGIC     t.typeID,
# MAGIC     b.number,
# MAGIC     m.metaID
# MAGIC FROM pokemon_catalog.`01_bronze`.pokemon b
# MAGIC JOIN types t
# MAGIC     ON b.type1 = t.type1 AND (b.type2 = t.type2 OR (b.type2 IS NULL AND t.type2 IS NULL))
# MAGIC JOIN meta m
# MAGIC     ON b.generation = m.generation AND b.legendary = m.legendary;

# COMMAND ----------

# MAGIC %md
# MAGIC #### Validations

# COMMAND ----------

import pandas as pd

main = spark.table('pokemon_catalog.02_silver.main').limit(5).toPandas()
meta = spark.table('pokemon_catalog.02_silver.meta').limit(5).toPandas()
stats = spark.table('pokemon_catalog.02_silver.stats').limit(5).toPandas()
types = spark.table('pokemon_catalog.02_silver.types').limit(5).toPandas()

display(main.head())
display(meta.head())
display(stats.head())
display(types.head())

# COMMAND ----------

print("==== Counts ==== ")
print(f"Main: {spark.table("pokemon_catalog.02_silver.main").count()}")
print(f"Stats: {spark.table("pokemon_catalog.02_silver.stats").count()}")
print(f"Types (combos): {spark.table("pokemon_catalog.02_silver.types").count()}")
print(f"Meta (combos): {spark.table("pokemon_catalog.02_silver.meta").count()}")

# COMMAND ----------

spark.sql('SELECT COUNT(*) AS Stats_Main FROM main m LEFT JOIN stats s ON m.statID = s.statID WHERE s.statID IS NULL;').show()
spark.sql('SELECT COUNT(*) AS Types_Main FROM main m LEFT JOIN types t ON m.typeID = t.typeID WHERE t.typeID IS NULL;').show()
spark.sql('SELECT COUNT(*) AS Meta_Main FROM main m LEFT JOIN meta t ON m.metaID = t.metaID WHERE t.metaID IS NULL;').show()
