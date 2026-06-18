# Databricks notebook source
# MAGIC %md
# MAGIC # Silver to Gold strategy
# MAGIC ## Tables:
# MAGIC - type / legendary / generation - stats | average
# MAGIC - type / legendary / geneartion / stats - phonemes | average

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC USE CATALOG pokemon_catalog;
# MAGIC USE SCHEMA `03_gold`;
# MAGIC
# MAGIC CREATE OR REPLACE TABLE type_stats AS
# MAGIC WITH pokemon_types AS (
# MAGIC     SELECT
# MAGIC         m.number,
# MAGIC         t.type1 AS pokemon_type,
# MAGIC         s.hp,
# MAGIC         s.attack,
# MAGIC         s.defense,
# MAGIC         s.sp_attack,
# MAGIC         s.sp_defense,
# MAGIC         s.speed,
# MAGIC         s.total
# MAGIC     FROM pokemon_catalog.`02_silver`.main m
# MAGIC     JOIN pokemon_catalog.`02_silver`.types t
# MAGIC         ON m.typeID = t.typeID
# MAGIC     JOIN pokemon_catalog.`02_silver`.stats s
# MAGIC         ON m.statID = s.statID
# MAGIC
# MAGIC     UNION ALL
# MAGIC
# MAGIC     SELECT
# MAGIC         m.number,
# MAGIC         t.type2 AS pokemon_type,
# MAGIC         s.hp,
# MAGIC         s.attack,
# MAGIC         s.defense,
# MAGIC         s.sp_attack,
# MAGIC         s.sp_defense,
# MAGIC         s.speed,
# MAGIC         s.total
# MAGIC     FROM pokemon_catalog.`02_silver`.main m
# MAGIC     JOIN pokemon_catalog.`02_silver`.types t
# MAGIC         ON m.typeID = t.typeID
# MAGIC     JOIN pokemon_catalog.`02_silver`.stats s
# MAGIC         ON m.statID = s.statID
# MAGIC     WHERE t.type2 IS NOT NULL
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC     pokemon_type,
# MAGIC     COUNT(*) AS pokemon_count,
# MAGIC     ROUND(AVG(hp), 2) AS avg_hp,
# MAGIC     ROUND(AVG(attack), 2) AS avg_attack,
# MAGIC     ROUND(AVG(defense), 2) AS avg_defense,
# MAGIC     ROUND(AVG(sp_attack), 2) AS avg_sp_attack,
# MAGIC     ROUND(AVG(sp_defense), 2) AS avg_sp_defense,
# MAGIC     ROUND(AVG(speed), 2) AS avg_speed,
# MAGIC     ROUND(AVG(total), 2) AS avg_total
# MAGIC FROM pokemon_types
# MAGIC GROUP BY pokemon_type
# MAGIC ORDER BY pokemon_type;
# MAGIC
# MAGIC
# MAGIC CREATE OR REPLACE TABLE legendary_stats AS
# MAGIC SELECT
# MAGIC     meta.legendary,
# MAGIC     COUNT(*) AS pokemon_count,
# MAGIC     ROUND(AVG(s.hp), 2) AS avg_hp,
# MAGIC     ROUND(AVG(s.attack), 2) AS avg_attack,
# MAGIC     ROUND(AVG(s.defense), 2) AS avg_defense,
# MAGIC     ROUND(AVG(s.sp_attack), 2) AS avg_sp_attack,
# MAGIC     ROUND(AVG(s.sp_defense), 2) AS avg_sp_defense,
# MAGIC     ROUND(AVG(s.speed), 2) AS avg_speed,
# MAGIC     ROUND(AVG(s.total), 2) AS avg_total
# MAGIC FROM pokemon_catalog.`02_silver`.main m
# MAGIC JOIN pokemon_catalog.`02_silver`.meta meta
# MAGIC     ON m.metaID = meta.metaID
# MAGIC JOIN pokemon_catalog.`02_silver`.stats s
# MAGIC     ON m.statID = s.statID
# MAGIC GROUP BY meta.legendary;
# MAGIC
# MAGIC
# MAGIC CREATE OR REPLACE TABLE generation_stats AS
# MAGIC SELECT
# MAGIC     mt.generation,
# MAGIC     COUNT(*) AS pokemon_count,
# MAGIC     ROUND(AVG(s.hp), 2) AS avg_hp,
# MAGIC     ROUND(AVG(s.attack), 2) AS avg_attack,
# MAGIC     ROUND(AVG(s.defense), 2) AS avg_defense,
# MAGIC     ROUND(AVG(s.sp_attack), 2) AS avg_sp_attack,
# MAGIC     ROUND(AVG(s.sp_defense), 2) AS avg_sp_defense,
# MAGIC     ROUND(AVG(s.speed), 2) AS avg_speed,
# MAGIC     ROUND(AVG(s.total), 2) AS avg_total
# MAGIC FROM pokemon_catalog.`02_silver`.main m
# MAGIC JOIN pokemon_catalog.`02_silver`.meta mt
# MAGIC     ON m.metaID = mt.metaID
# MAGIC JOIN pokemon_catalog.`02_silver`.stats s
# MAGIC     ON m.statID = s.statID
# MAGIC GROUP BY mt.generation
# MAGIC ORDER BY mt.generation;
# MAGIC
# MAGIC
# MAGIC CREATE OR REPLACE TABLE phonems_info AS
# MAGIC SELECT
# MAGIC     m.number,
# MAGIC     m.name,
# MAGIC     LENGTH(regexp_replace(LOWER(m.name), '[aeiouy]', '')) AS vowel_count,
# MAGIC     LENGTH(regexp_replace(LOWER(m.name), '[^qwrtpsdfghjklzxcvbnm]', '')) AS consonant_count,
# MAGIC     LENGTH(regexp_replace(LOWER(m.name), '[^a-z]', '')) AS letter_count
# MAGIC FROM pokemon_catalog.`02_silver`.main m;
# MAGIC
# MAGIC
# MAGIC CREATE OR REPLACE TABLE type_phonems AS
# MAGIC WITH pokemon_types AS (
# MAGIC     SELECT
# MAGIC         m.number,
# MAGIC         t.type1 AS pokemon_type,
# MAGIC         p.vowel_count,
# MAGIC         p.consonant_count,
# MAGIC         p.letter_count
# MAGIC     FROM pokemon_catalog.`02_silver`.main m
# MAGIC     JOIN phonems_info p
# MAGIC         ON m.number = p.number
# MAGIC     JOIN pokemon_catalog.`02_silver`.types t
# MAGIC         ON m.typeID = t.typeID
# MAGIC
# MAGIC     UNION ALL
# MAGIC
# MAGIC     SELECT
# MAGIC         m.number,
# MAGIC         t.type2 AS pokemon_type,
# MAGIC         p.vowel_count,
# MAGIC         p.consonant_count,
# MAGIC         p.letter_count
# MAGIC     FROM pokemon_catalog.`02_silver`.main m
# MAGIC     JOIN phonems_info p
# MAGIC         ON m.number = p.number
# MAGIC     JOIN pokemon_catalog.`02_silver`.types t
# MAGIC         ON m.typeID = t.typeID
# MAGIC     WHERE t.type2 IS NOT NULL
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC     pokemon_type,
# MAGIC     COUNT(*) AS pokemon_count,
# MAGIC     ROUND(AVG(vowel_count), 2) AS avg_vowel_count,
# MAGIC     ROUND(AVG(consonant_count), 2) AS avg_consonant_count,
# MAGIC     ROUND(AVG(letter_count), 2) AS avg_letter_count
# MAGIC FROM pokemon_types
# MAGIC GROUP BY pokemon_type
# MAGIC ORDER BY pokemon_type;
# MAGIC
# MAGIC
# MAGIC CREATE OR REPLACE TABLE legendary_phonems AS
# MAGIC SELECT
# MAGIC     meta.legendary,
# MAGIC     COUNT(*) AS pokemon_count,
# MAGIC     ROUND(AVG(vowel_count), 2) AS avg_vowel_count,
# MAGIC     ROUND(AVG(consonant_count), 2) AS avg_consonant_count,
# MAGIC     ROUND(AVG(letter_count), 2) AS avg_letter_count
# MAGIC FROM pokemon_catalog.`02_silver`.main m
# MAGIC JOIN pokemon_catalog.`02_silver`.meta meta
# MAGIC     ON m.metaID = meta.metaID
# MAGIC JOIN phonems_info p
# MAGIC     ON m.number = p.number
# MAGIC GROUP BY meta.legendary;
# MAGIC
# MAGIC
# MAGIC CREATE OR REPLACE TABLE generation_phonems AS
# MAGIC SELECT
# MAGIC     mt.generation,
# MAGIC     COUNT(*) AS pokemon_count,
# MAGIC     ROUND(AVG(vowel_count), 2) AS avg_vowel_count,
# MAGIC     ROUND(AVG(consonant_count), 2) AS avg_consonant_count,
# MAGIC     ROUND(AVG(letter_count), 2) AS avg_letter_count
# MAGIC FROM pokemon_catalog.`02_silver`.main m
# MAGIC JOIN pokemon_catalog.`02_silver`.meta mt
# MAGIC     ON m.metaID = mt.metaID
# MAGIC JOIN phonems_info p
# MAGIC     ON m.number = p.number
# MAGIC GROUP BY mt.generation
# MAGIC ORDER BY mt.generation;
# MAGIC
# MAGIC
# MAGIC SHOW TABLES IN `03_gold`;

# COMMAND ----------

import pandas as pd


type_stats = spark.table('pokemon_catalog.03_gold.type_stats').limit(5).toPandas()
legendary_stats = spark.table('pokemon_catalog.03_gold.legendary_stats').limit(5).toPandas()
generation_stats = spark.table('pokemon_catalog.03_gold.generation_stats').limit(5).toPandas()
phonems_info = spark.table('pokemon_catalog.03_gold.phonems_info').limit(5).toPandas()
type_phonems = spark.table('pokemon_catalog.03_gold.type_phonems').limit(5).toPandas()
legendary_phonems = spark.table('pokemon_catalog.03_gold.legendary_phonems').limit(5).toPandas()
generation_phonems = spark.table('pokemon_catalog.03_gold.generation_phonems').limit(5).toPandas()


display(type_stats.head())
display(legendary_stats.head())
display(generation_stats.head())
display(phonems_info.head())
display(type_phonems.head())
display(legendary_phonems.head())
display(generation_phonems.head())
