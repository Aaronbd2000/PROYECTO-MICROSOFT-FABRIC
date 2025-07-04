#!/usr/bin/env python
# coding: utf-8

# ## NB_ETL_AMHP
# 
# New notebook

# In[1]:


# En este notebook aprenderemos a:
# Leer los datos con PySpark
# Realizar transformaciones
# Guardar los dataframes como tablas Delta
# Crear un modelo estrella para análisis

#Configuración inicial y verificación del entorno
# Este comando verifica que estamos en el entorno correcto de Fabric

import pyspark.sql.functions as F
from pyspark.sql.types import *
from notebookutils import mssparkutils
import pandas as pd

# Verificar versión de Spark
print(f"Versión de Spark: {spark.version}")


# In[2]:


# Crear estructura de carpetas en el lakehouse
# Este comando crea las carpetas necesarias en el lakehouse para almacenar nuestros archivos

try:
    # Crear carpetas para datos brutos y procesados
    mssparkutils.fs.mkdirs("Files/bronze")
    mssparkutils.fs.mkdirs("Files/silver")
    mssparkutils.fs.mkdirs("Files/gold")
    mssparkutils.fs.mkdirs("Files/processed")
    print("✅ Estructura de carpetas creada correctamente")
except Exception as e:
    print(f"Error al crear carpetas: {str(e)}")


# In[3]:


# Definición de esquemas para mejor control de los datos
# Definimos los esquemas de nuestros dataframes para asegurar tipos de datos correctos

# Esquema para brokers
schema_brokers = StructType([
    StructField("BrokerID", IntegerType(), False),
    StructField("BrokerName", StringType(), True),
    StructField("Region", StringType(), True),
    StructField("Email", StringType(), True)
])

# Esquema para campaigns
schema_campaigns = StructType([
    StructField("CampaignID", IntegerType(), False),
    StructField("Channel", StringType(), True),
    StructField("CampaignName", StringType(), True),
    StructField("StartDate", DateType(), True),
    StructField("EndDate", DateType(), True),
    StructField("BudgetUSD", IntegerType(), True)
])

# Esquema para clients
schema_clients = StructType([
    StructField("ClientID", IntegerType(), False),
    StructField("FirstName", StringType(), True),
    StructField("LastName", StringType(), True),
    StructField("Email", StringType(), True),
    StructField("Region", StringType(), True)
])

# Esquema para leads
schema_leads = StructType([
    StructField("LeadID", IntegerType(), False),
    StructField("ClientID", IntegerType(), False),
    StructField("PropertyID", IntegerType(), False),
    StructField("CampaignID", IntegerType(), False),
    StructField("LeadDate", DateType(), True),
    StructField("LeadSource", StringType(), True)
])

# Esquema para projects
schema_projects = StructType([
    StructField("ProjectID", IntegerType(), False),
    StructField("ProjectName", StringType(), True),
    StructField("City", StringType(), True),
    StructField("Region", StringType(), True),
    StructField("LaunchYear", IntegerType(), True),
    StructField("Status", StringType(), True)
])

# Esquema para properties
schema_properties = StructType([
    StructField("PropertyID", IntegerType(), False),
    StructField("ProjectID", IntegerType(), False),
    StructField("PropertyType", StringType(), True),
    StructField("Size_m2", IntegerType(), True),
    StructField("Bedrooms", IntegerType(), True),
    StructField("Bathrooms", IntegerType(), True),
    StructField("ListPriceUSD", IntegerType(), True),
    StructField("AvailabilityStatus", StringType(), True)
])

# Esquema para sales
schema_sales = StructType([
    StructField("SaleID", IntegerType(), False),
    StructField("PropertyID", IntegerType(), False),
    StructField("ClientID", IntegerType(), False),
    StructField("BrokerID", IntegerType(), False),
    StructField("SaleDate", DateType(), True),
    StructField("SalePriceUSD", IntegerType(), True)
])
print("✅ Esquemas definidos correctamente")


# In[4]:


# Leer los archivos CSV con los esquemas definidos
# Este comando lee los archivos CSV utilizando los esquemas definidos anteriormente

try:
    # Leer archivo de brokers
    df_brokers = spark.read.format("csv") \
        .option("header", "true") \
        .schema(schema_brokers) \
        .load("Files/raw/brokers.csv")
    
    # Leer archivo de campañas
    df_campaigns = spark.read.format("csv") \
        .option("header", "true") \
        .schema(schema_campaigns) \
        .load("Files/raw/campaigns.csv")
    
    # Leer archivo de clientes
    df_clients = spark.read.format("csv") \
        .option("header", "true") \
        .schema(schema_clients) \
        .load("Files/raw/clients.csv")
    
    # Leer archivo de leads
    df_leads = spark.read.format("csv") \
        .option("header", "true") \
        .schema(schema_leads) \
        .load("Files/raw/leads.csv")
    
    # Leer archivo de proyectos
    df_projects = spark.read.format("csv") \
        .option("header", "true") \
        .schema(schema_projects) \
        .load("Files/raw/projects.csv")
    
    # Leer archivo de propiedades
    df_properties = spark.read.format("csv") \
        .option("header", "true") \
        .schema(schema_properties) \
        .load("Files/raw/properties.csv")
    
    # Leer archivo de ventas
    df_sales = spark.read.format("csv") \
        .option("header", "true") \
        .schema(schema_sales) \
        .load("Files/raw/sales.csv")
    
    print("✅ Archivos CSV leídos correctamente")

except Exception as e:
    print(f"❌ Error al leer archivos: {str(e)}")


# In[5]:


# Exploración de los datos
# Mostramos una vista previa de los datos cargados

print("📌 Vista previa de los datos de brokers:")
display(df_brokers.limit(5))

print("📌 Vista previa de los datos de campañas:")
display(df_campaigns.limit(5))

print("📌 Vista previa de los datos de clientes:")
display(df_clients.limit(5))

print("📌 Vista previa de los datos de leads:")
display(df_leads.limit(5))

print("📌 Vista previa de los datos de proyectos:")
display(df_projects.limit(5))

print("📌 Vista previa de los datos de propiedades:")
display(df_properties.limit(5))

print("📌 Vista previa de los datos de ventas:")
display(df_sales.limit(5))



# In[6]:


# Información sobre los dataframes
# Mostramos el esquema y contamos los registros en cada tabla

print("🗂️ Información del dataframe de brokers:")
print(f"Número de registros: {df_brokers.count()}")
df_brokers.printSchema()

print("\n🗂️ Información del dataframe de campañas:")
print(f"Número de registros: {df_campaigns.count()}")
df_campaigns.printSchema()

print("\n🗂️ Información del dataframe de clientes:")
print(f"Número de registros: {df_clients.count()}")
df_clients.printSchema()

print("\n🗂️ Información del dataframe de leads:")
print(f"Número de registros: {df_leads.count()}")
df_leads.printSchema()

print("\n🗂️ Información del dataframe de proyectos:")
print(f"Número de registros: {df_projects.count()}")
df_projects.printSchema()

print("\n🗂️ Información del dataframe de propiedades:")
print(f"Número de registros: {df_properties.count()}")
df_properties.printSchema()

print("\n🗂️ Información del dataframe de ventas:")
print(f"Número de registros: {df_sales.count()}")
df_sales.printSchema()


# In[10]:


# Realizar transformaciones en los dataframes
# Aplicamos transformaciones básicas para mejorar la calidad de los datos

# Transformación de clientes: Crear columna nombre_completo
df_clients_procesado = df_clients.withColumn(
    "nombre_completo",
    F.concat(F.col("FirstName"), F.lit(" "), F.col("LastName"))
)

# Transformación de propiedades: Calcular valor estimado solo si están disponibles
df_properties_procesado = df_properties.withColumn(
    "valor_estimado",
    F.when(F.col("AvailabilityStatus") == "Available", F.col("ListPriceUSD"))
     .otherwise(F.lit(0))
)

# Transformación de proyectos: Extraer década de lanzamiento
df_projects_procesado = df_projects.withColumn(
    "decada_lanzamiento",
    (F.col("LaunchYear") / 10).cast("int") * 10
)

# Transformación de campañas: Calcular duración en días
df_campaigns_procesado = df_campaigns.withColumn(
    "duracion_dias",
    F.datediff(F.col("EndDate"), F.col("StartDate"))
)

# Transformación de brokers: Generar dominio a partir del email
df_brokers_procesado = df_brokers.withColumn(
    "dominio",
    F.split(F.col("Email"), "@").getItem(1)
)

# Transformación de leads: Calcular año de generación del lead
df_leads_procesado = df_leads.withColumn(
    "anio_lead",
    F.year(F.col("LeadDate"))
)

# Transformación de ventas: Calcular margen estimado (simulado)
df_sales_procesado = df_sales.withColumn(
    "margen_estimado",
    F.round(F.col("SalePriceUSD") * 0.15, 2)  # Simulamos margen 15%
)

print("✅ Transformaciones aplicadas correctamente")


# In[11]:


# Mostrar ejemplos de las transformaciones

print("📌 Ejemplo de clientes procesados:")
display(df_clients_procesado.limit(5))

print("📌 Ejemplo de propiedades procesadas:")
display(df_properties_procesado.limit(5))

print("📌 Ejemplo de proyectos procesados:")
display(df_projects_procesado.limit(5))

print("📌 Ejemplo de campañas procesadas:")
display(df_campaigns_procesado.limit(5))

print("📌 Ejemplo de brokers procesados:")
display(df_brokers_procesado.limit(5))

print("📌 Ejemplo de leads procesados:")
display(df_leads_procesado.limit(5))

print("📌 Ejemplo de ventas procesadas:")
display(df_sales_procesado.limit(5))



# In[12]:


# Guardar los dataframes como tablas Delta
# Guardamos los dataframes procesados como archivos Delta en el lakehouse

try:
    # Guardar clientes
    df_clients_procesado.write.format("delta").mode("overwrite").save("Files/gold/clients_delta")
    
    # Guardar propiedades
    df_properties_procesado.write.format("delta").mode("overwrite").save("Files/gold/properties_delta")
    
    # Guardar proyectos
    df_projects_procesado.write.format("delta").mode("overwrite").save("Files/gold/projects_delta")
    
    # Guardar campañas
    df_campaigns_procesado.write.format("delta").mode("overwrite").save("Files/gold/campaigns_delta")
    
    # Guardar brokers
    df_brokers_procesado.write.format("delta").mode("overwrite").save("Files/gold/brokers_delta")
    
    # Guardar leads
    df_leads_procesado.write.format("delta").mode("overwrite").save("Files/gold/leads_delta")
    
    # Guardar ventas
    df_sales_procesado.write.format("delta").mode("overwrite").save("Files/gold/sales_delta")
    
    print("✅ DataFrames guardados como archivos Delta correctamente")
except Exception as e:
    print(f"❌ Error al guardar archivos Delta: {str(e)}")



# In[13]:


# Registrar tablas como vistas temporales en la sesión actual

try:
    # Registrar vistas temporales
    df_clients_procesado.createOrReplaceTempView("dim_clients")
    df_properties_procesado.createOrReplaceTempView("dim_properties")
    df_projects_procesado.createOrReplaceTempView("dim_projects")
    df_campaigns_procesado.createOrReplaceTempView("dim_campaigns")
    df_brokers_procesado.createOrReplaceTempView("dim_brokers")
    df_leads_procesado.createOrReplaceTempView("fact_leads")
    df_sales_procesado.createOrReplaceTempView("fact_sales")
    
    # Verificar que se han creado correctamente
    tables = spark.sql("SHOW TABLES").collect()
    print("🧾 Tablas disponibles en la sesión:")
    for table in tables:
        print(f" - {table.tableName}")
    
    print("✅ Vistas temporales creadas correctamente para la sesión actual")

    # Alternativa: Guardar como tablas en el catálogo del Lakehouse
    print("\n📌 Registrando tablas en el catálogo del Lakehouse...")

    df_clients_procesado.write.format("delta").mode("overwrite").saveAsTable("dim_clients")
    df_properties_procesado.write.format("delta").mode("overwrite").saveAsTable("dim_properties")
    df_projects_procesado.write.format("delta").mode("overwrite").saveAsTable("dim_projects")
    df_campaigns_procesado.write.format("delta").mode("overwrite").saveAsTable("dim_campaigns")
    df_brokers_procesado.write.format("delta").mode("overwrite").saveAsTable("dim_brokers")
    df_leads_procesado.write.format("delta").mode("overwrite").saveAsTable("fact_leads")
    df_sales_procesado.write.format("delta").mode("overwrite").saveAsTable("fact_sales")

    print("✅ Tablas registradas correctamente en el catálogo del Lakehouse")

except Exception as e:
    print(f"❌ Error al crear tablas o vistas: {str(e)}")


# In[35]:


# Consultar el modelo estrella completo
# Realizamos una consulta SQL que une todas las tablas del modelo estrella

query = """
SELECT 
    v.id_venta,
    t.fecha,
    t.tipo_dia,
    c.nombre_completo AS cliente,
    c.ciudad AS ciudad_cliente,
    p.nombre AS producto,
    p.categoria,
    p.subcategoria,
    ti.nombre AS tienda,
    ti.ciudad AS ciudad_tienda,
    v.cantidad,
    v.precio_unitario,
    v.descuento,
    v.total,
    v.porcentaje_descuento
FROM 
    fact_ventas v
JOIN 
    dim_tiempo t ON v.id_fecha = t.id_fecha
JOIN 
    dim_clientes c ON v.id_cliente = c.id_cliente
JOIN 
    dim_productos p ON v.id_producto = p.id_producto
JOIN 
    dim_tiendas ti ON v.id_tienda = ti.id_tienda
ORDER BY 
    v.id_venta
"""

try:
    # Ejecutar la consulta
    resultado = spark.sql(query)
    
    # Mostrar los resultados
    print("Consulta del modelo estrella completo:")
    display(resultado)
    
    print("✅ Consulta ejecutada correctamente")
except Exception as e:
    print(f"Error al ejecutar la consulta: {str(e)}")


# In[36]:


# Análisis básico de ventas
# Realizamos un análisis básico de las ventas por categoría de producto

query_analisis = """
SELECT 
    p.categoria,
    COUNT(*) AS num_ventas,
    SUM(v.total) AS ventas_totales,
    AVG(v.total) AS venta_promedio,
    SUM(v.descuento) AS descuentos_totales
FROM 
    fact_ventas v
JOIN 
    dim_productos p ON v.id_producto = p.id_producto
GROUP BY 
    p.categoria
ORDER BY 
    ventas_totales DESC
"""

try:
    # Ejecutar la consulta de análisis
    resultado_analisis = spark.sql(query_analisis)
    
    # Mostrar los resultados
    print("Análisis de ventas por categoría:")
    display(resultado_analisis)
    
    # Convertir a pandas para visualización
    df_analisis_pd = resultado_analisis.toPandas()
    
    # Visualizar con matplotlib (si está disponible)
    try:
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(10, 6))
        plt.bar(df_analisis_pd['categoria'], df_analisis_pd['ventas_totales'])
        plt.title('Ventas totales por categoría')
        plt.xlabel('Categoría')
        plt.ylabel('Ventas totales (€)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        display(plt.gcf())
    except ImportError:
        print("Matplotlib no está disponible para visualización. Mostrando datos en formato tabular.")
        
    print("✅ Análisis completado correctamente")
except Exception as e:
    print(f"Error al ejecutar análisis: {str(e)}")


# In[37]:


# Guardar el resultado del análisis
# Guardamos el resultado del análisis como archivo CSV

try:
    # Convertir a pandas para guardarlo como CSV
    df_analisis_pd.to_csv("/tmp/analisis_ventas_categoria.csv", index=False)
    
    # Subir al lakehouse
    mssparkutils.fs.put("Files/processed/analisis_ventas_categoria.csv", 
                        "/tmp/analisis_ventas_categoria.csv", True)
    
    print("✅ Resultado del análisis guardado como CSV en 'Files/processed/analisis_ventas_categoria.csv'")
except Exception as e:
    print(f"Error al guardar resultado: {str(e)}")

