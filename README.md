# 🏢 Real Estate Insight Fabric - BrickVista

**Plataforma analítica inmobiliaria sobre Microsoft Fabric**

Este repositorio contiene el desarrollo completo del proyecto integrador de Microsoft Fabric para la empresa ficticia **BrickVista S.A.**, una desarrolladora inmobiliaria en LATAM. El objetivo es centralizar, transformar y analizar datos del negocio inmobiliario (ventas, leads, propiedades, campañas, etc.) en una arquitectura moderna, escalable y gobernada.

---

## 🧩 Caso de uso

> **“Reducir el time-to-insight de 48h a 3h mediante una plataforma data-driven que integre datos comerciales, de marketing e inventario para análisis y toma de decisiones.”**

---

## 🧱 Arquitectura



- **Ingesta**: Data Factory Pipelines (Fabric) desde Azure Data Lake Gen2.
- **Almacenamiento**: Lakehouse con estructura medallion (`Raw ➝ Bronze ➝ Silver ➝ Gold`).
- **Transformación**: Notebooks PySpark con validaciones, esquemas y enriquecimientos.
- **Modelo semántico**: Warehouse con diseño en estrella (Sales, Leads, Properties, etc.).
- **Visualización**: Power BI (App: *Real Estate Command Center*).

---


## 🛠 Tecnologías utilizadas

- **Microsoft Fabric**:
  - OneLake
  - Data Factory Pipelines
  - Lakehouse
  - Notebooks PySpark
  - Warehouse
  - Power BI

- **Lenguajes**:
  - Python (PySpark)
  - SQL (modelo semántico)
  - DAX (Power BI, opcional)

---

## 🧪 Buenas prácticas implementadas

- Arquitectura Medallion (Bronze, Silver, Gold).
- Validación de esquemas con `StructType`.
- Registro de tablas como vistas temporales y permanentes.
- Trazabilidad de datos desde la ingesta hasta el dashboard.
- Naming conventions y modularidad en notebooks.

---

## ❗ Dificultades enfrentadas

- Integración inicial con ADLS (permisos y autenticación).
- Calidad de datos en CSV heterogéneos.
- Modelado correcto de relaciones entre hechos y dimensiones.

---

## 🚀 Próximos pasos

- Incorporar datos en streaming (leads en tiempo real).
- Implementar alertas y monitoreo con Fabric Metrics.
- Añadir datasets externos: tipo de cambio, tasas hipotecarias, etc.
- Optimización DAX en Power BI con KPIs personalizados.

---

## 👤 Autor

**Aaron Manuel Huaracha Parra**  
Proyecto integrador – Microsoft Fabric  

---

## 📜 Licencia

Este repositorio es de uso educativo y demostrativo. No contiene datos reales de clientes ni transacciones.
