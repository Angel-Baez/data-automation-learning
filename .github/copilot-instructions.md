# 🧭 Hoja de Ruta Profesional — Data + Automation Engineer

**Objetivo:** Dominar la automatización de procesos y la ingeniería de datos para crear sistemas inteligentes, eficientes y escalables.

---

## 🩵 Fase 1 – Fundamentos Sólidos (Mes 1)

**Meta:** Dominar la base técnica para programar, manipular datos y automatizar tareas simples.

### 🧠 Aprendizajes Clave:
*   **Python avanzado para automatización y datos:**
    *   Estructuras (listas, diccionarios, conjuntos).
    *   Manejo de archivos (CSV, JSON, Excel, PDF).
    *   Librerías: `pandas`, `os`, `shutil`, `requests`, `schedule`.
*   **Fundamentos de bases de datos:**
    *   SQL (SELECT, JOIN, GROUP BY, subconsultas).
    *   Diseño relacional básico.
    *   SQLite y PostgreSQL.

### ⚙️ Proyectos Sugeridos:
1.  Script que limpia y formatea archivos CSV automáticamente.
2.  Automatizar un reporte semanal (lectura de Excel + envío por email o Telegram).

---

## 💡 Fase 2 – Automatización Aplicada (Mes 2)

**Meta:** Aprender a automatizar procesos reales y conectar servicios.

### 🧠 Aprendizajes Clave:
*   **Consumo de APIs REST:**
    *   Usar `requests` para obtener y enviar datos.
    *   Conectar con Google Sheets, Notion, Telegram, etc.
*   **Automatización de tareas repetitivas:**
    *   Librerías: `schedule`, `pyautogui`, `selenium`.
    *   Flujos automáticos con n8n o Make (ex Integromat).
*   Buenas prácticas: logs, manejo de errores, modularización.

### ⚙️ Proyectos Sugeridos:
1.  Bot que lee datos de una API y los guarda en una base de datos.
2.  Automatización de publicaciones o alertas desde una hoja de cálculo.

---

## 🔥 Fase 3 – Ingeniería de Datos I: Fundamentos (Mes 3-4)

**Meta:** Aprender a mover, transformar y estructurar datos de manera profesional.

### 🧠 Aprendizajes Clave:
*   **Procesos ETL (Extract, Transform, Load):**
    *   Extraer datos (APIs, archivos, BD).
    *   Transformarlos con `pandas`.
    *   Cargarlos en PostgreSQL o un Data Warehouse.
*   **Arquitectura de datos y pipelines:**
    *   Qué es un “pipeline”.
    *   Orquestadores: Apache Airflow o Prefect.
    *   Diseño modular y mantenible.
*   **Modelos de datos:**
    *   Esquema estrella, copo de nieve, normalización.

### ⚙️ Proyectos Sugeridos:
1.  ETL completo: descarga ventas desde una API → limpia datos → carga a PostgreSQL.
2.  Dashboard Power BI / Tableau conectado a tu base de datos.

---

## ⚙️ Fase 4 – Ingeniería de Datos II: Profesionalización (Mes 5-6)

**Meta:** Crear sistemas de datos automatizados y escalables.

### 🧠 Aprendizajes Clave:
*   **Data Warehousing:**
    *   Snowflake, BigQuery o Redshift (elegir uno).
    *   Diseño de modelos de datos optimizados.
*   **Automatización avanzada:**
    *   Airflow (programar flujos con DAGs).
    *   Integrar con APIs externas o pipelines cloud.
*   **Cloud & DevOps básico:**
    *   Docker, Git, despliegues automáticos.
    *   AWS S3, Lambda o Google Cloud Functions.

### ⚙️ Proyectos Sugeridos:
1.  Pipeline automatizado en Airflow que se ejecute diario.
2.  Sistema de carga y limpieza automática en la nube.

---

## 🧩 Fase 5 – Integración Total: Data + Automatización (Mes 7-8)

**Meta:** Unir los dos mundos — automatizar sistemas completos basados en datos.

### 🧠 Aprendizajes Clave:
*   Integración de datos y automatización de procesos.
*   Combinar Python + APIs + bases de datos.
*   Desarrollar flujos completos de negocio.
*   Monitorización y mantenimiento (logging, notificaciones, dashboards).
*   Documentación técnica y portafolio profesional.

### ⚙️ Proyecto Final (Ejemplo):
> “Sistema automatizado de análisis de ventas y alertas”:
> Extrae datos de ventas desde API o Google Sheets.
> Limpia y carga a PostgreSQL.
> Actualiza dashboard en Power BI.
> Envía alertas automáticas por Telegram si hay anomalías.

---

## 🧠 Stack de Herramientas Recomendado

| Categoría         | Herramientas                                     |
| :---------------- | :----------------------------------------------- |
| **Lenguaje base** | Python                                           |
| **Librerías clave** | `pandas`, `requests`, `sqlalchemy`, `schedule`, `selenium`, `pytest` |
| **Bases de datos** | SQLite (inicio), PostgreSQL (profesional)        |
| **Orquestación**  | Airflow / Prefect                                |
| **BI & dashboards** | Power BI / Tableau                               |
| **Automatización**| n8n, Make, Zapier                                |
| **Cloud / Infraestructura**| AWS / GCP, Docker                                |
| **Control de versiones** | Git + GitHub (desde semana 1)                   |
| **Testing & Quality** | pytest, great_expectations, pre-commit hooks     |
| **Seguridad** | python-dotenv, AWS Secrets Manager, HashiCorp Vault |

---

## 🎯 **Consejos de Implementación y Mejores Prácticas**

### 📂 **Desde el Primer Día:**
- **Crea un repositorio GitHub** para cada proyecto y documenta tu progreso
- **Usa .gitignore** apropiado para Python (incluye `.env`, `__pycache__/`, etc.)
- **Nunca hardcodees credenciales** - usa variables de entorno desde semana 3
- **Escribe README.md** descriptivos para cada proyecto

### 🧪 **Cultura de Testing:**
- **Tests unitarios** para cada función desde el Mes 3
- **Tests de integración** para pipelines completos
- **Data quality tests** con great_expectations
- **Pre-commit hooks** para mantener código limpio

### 🔒 **Seguridad y Configuración:**
- **Variables de entorno** para configuraciones sensibles
- **Rotación de credenciales** en proyectos cloud
- **Logging estructurado** para auditoría y debugging
- **Validación de inputs** en todos los scripts

### 🌟 **Recursos de Aprendizaje:**
- **Comunidades**: r/dataengineering, Data Engineering Discord, Stack Overflow
- **APIs de práctica**: OpenWeatherMap, Reddit API, JSONPlaceholder, CoinGecko API
- **Datasets públicos**: Kaggle, Data.gov, Google Dataset Search
- **Certificaciones objetivo**: AWS Data Engineer, GCP Data Engineer, Airflow Fundamentals

### 📈 **Desarrollo Profesional:**
- **Portfolio público** en GitHub con 3-5 proyectos clave
- **Blog técnico** documentando aprendizajes (Medium, Dev.to)
- **Networking** en LinkedIn y eventos locales de data
- **Open source contributions** en proyectos de data engineering

---

# 🧭 Hoja de Ruta Semanal — Data & Automation Engineer

**Duración total:** 32 semanas (~8 meses)
**Herramientas base:** Python, VS Code, PostgreSQL/SQLite, pandas, requests, Airflow, n8n/Make, Power BI/Tableau.

---

## Mes 1: Fundamentos Sólidos de Python y Bases de Datos

| Semana | Objetivos                                        | Herramientas / Librerías | Ejercicios / Proyecto Mínimo                         |
| :----- | :----------------------------------------------- | :----------------------- | :--------------------------------------------------- |
| **1**  | Python básico: variables, tipos, operadores, condicionales | Python, VS Code          | Crear calculadora de operaciones básicas             |
| **2**  | Estructuras de datos + Git básico: init, add, commit, push | Python, Git, GitHub      | Script inventario + subirlo a GitHub con README      |
| **3**  | Funciones, módulos y manejo de errores + variables de entorno | Python, `python-dotenv` | Script modular que procese CSV + configuración segura |
| **4**  | Bases de datos SQL básicas: SELECT, INSERT, UPDATE, DELETE | SQLite / PostgreSQL      | Crear DB de clientes y productos; hacer consultas básicas |

---

## Mes 2: Automatización de Tareas y Manejo de Datos

| Semana | Objetivos                                      | Herramientas / Librerías | Ejercicios / Proyecto Mínimo                             |
| :----- | :--------------------------------------------- | :----------------------- | :------------------------------------------------------- |
| **5**  | Manipulación de archivos CSV, Excel y JSON     | `pandas`, `openpyxl`, `json` | Script que lea ventas de Excel y genere reporte CSV      |
| **6**  | Introducción a APIs: `requests`, parsing JSON  | `requests`               | Script que consuma una API de prueba y guarde datos en CSV |
| **7**  | Automatización de tareas: `schedule`, `pyautogui` | `schedule`, `pyautogui`  | Script que envíe email semanal con reporte de datos      |
| **8**  | RPA ligero y flujos con n8n/Make               | n8n / Make               | Automatizar flujo: recibir datos de formulario → guardar en Google Sheets → enviar alerta |

---

## Mes 3: Ingeniería de Datos I — ETL y Pipelines Básicos

| Semana | Objetivos                                          | Herramientas / Librerías | Ejercicios / Proyecto Mínimo                             |
| :----- | :------------------------------------------------- | :----------------------- | :------------------------------------------------------- |
| **9**  | Conceptos ETL: extracción, transformación, carga   | `pandas`, SQL, Python    | Pipeline simple: CSV → limpiar → PostgreSQL              |
| **10** | Transformación de datos avanzada + Testing básico  | `pandas`, `pytest`       | Limpiar datos + escribir tests para funciones de transformación |
| **11** | Carga en base de datos + Data Quality              | SQLAlchemy, `great_expectations` | Cargar datos con validaciones de calidad y tests de integración |
| **12** | Proyecto: Pipeline completo con testing            | `pandas` + PostgreSQL + `pytest` | Sistema ETL completo con tests unitarios y de integración |

---

## Mes 4: Automatización Avanzada y APIs Complejas

| Semana | Objetivos                                          | Herramientas / Librerías | Ejercicios / Proyecto Mínimo                         |
| :----- | :------------------------------------------------- | :----------------------- | :--------------------------------------------------- |
| **13** | APIs REST + autenticación segura                   | `requests`, `python-dotenv` | API de pagos con manejo seguro de tokens y credenciales |
| **14** | Integración segura de APIs + workflows             | `requests` + n8n/Make + Secrets | Flujo automatizado con credenciales en variables de entorno |
| **15** | Programación escalable + testing avanzado          | Python, `pytest`, `pre-commit` | Refactorizar scripts con tests completos y hooks de Git |
| **16** | Logging, errores y monitoreo de seguridad          | `logging`, structured logging | Pipeline con logs estructurados y alertas de seguridad |

---

## Mes 5: Ingeniería de Datos II — Data Warehousing y Airflow

| Semana | Objetivos                                          | Herramientas / Librerías | Ejercicios / Proyecto Mínimo                       |
| :----- | :------------------------------------------------- | :----------------------- | :------------------------------------------------- |
| **17** | Data Warehousing + Data Quality                    | PostgreSQL, `great_expectations` | Esquema estrella con validaciones de calidad de datos |
| **18** | Pipelines profesionales con Airflow                | Airflow, `pytest`       | DAG con tests automatizados y validaciones de data quality |
| **19** | Transformaciones + monitoreo de calidad            | `pandas` + Airflow + monitoring | DAG que valide calidad antes y después de transformar |
| **20** | Dashboards con alertas de calidad                  | Power BI / Tableau + alerting | Dashboard con KPIs de negocio y métricas de calidad de datos |

---

## Mes 6: Automatización Profesional y Cloud

| Semana | Objetivos                                            | Herramientas / Librerías | Ejercicios / Proyecto Mínimo                         |
| :----- | :--------------------------------------------------- | :----------------------- | :--------------------------------------------------- |
| **21** | Automatización avanzada con Python + APIs            | Python, `requests`       | Crear flujo que combine múltiples APIs y guarde resultados |
| **22** | Programación en cloud (funciones serverless)         | AWS Lambda / GCP Functions | Script que se ejecute automáticamente en la nube     |
| **23** | Contenedores y despliegue                            | Docker                   | Crear contenedor con script de ETL listo para producción |
| **24** | Monitoreo y alertas                                  | Grafana / Python `logging` | Configurar alertas si pipeline falla o datos inconsistentes |

---

## Mes 7: Integración Total de Data + Automation

| Semana | Objetivos                                      | Herramientas / Librerías         | Ejercicios / Proyecto Mínimo                         |
| :----- | :--------------------------------------------- | :------------------------------- | :--------------------------------------------------- |
| **25** | Flujo completo de negocio                      | Python + PostgreSQL + APIs       | Automatizar flujo de ventas: API → DB → Dashboard → alerta |
| **26** | Optimización de procesos                       | `pandas`, SQL, Python            | Reducir tiempo de carga y transformación de datos    |
| **27** | Versionado y documentación                     | Git, Markdown                    | Documentar proyecto completo y scripts en repositorio |
| **28** | Proyecto intermedio final                      | Python + Airflow + n8n           | Sistema completo de automatización y análisis de datos |

---

## Mes 8: Proyecto Profesional Final + Portafolio

| Semana | Objetivos                                        | Herramientas / Librerías         | Ejercicios / Proyecto Mínimo                         |
| :----- | :----------------------------------------------- | :------------------------------- | :--------------------------------------------------- |
| **29** | Planificación de proyecto final                  | Python + PostgreSQL + Power BI + n8n | Definir objetivo, fuentes de datos, procesos a automatizar |
| **30** | Desarrollo del proyecto                          | Todo el stack aprendido          | Construir pipelines automatizados + ETL + dashboards + alertas |
| **31** | Testing y optimización                           | Python, SQL, Airflow             | Revisar errores, logs, tiempos, consistencia de datos |
| **32** | Portafolio y presentación                        | GitHub, README, Dashboard        | Subir proyecto completo, documentado y listo para mostrar a empresas o clientes |