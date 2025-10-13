# 📁 Template Semana 3: Procesamiento CSV Modular + Variables de Entorno

## 🎯 **Objetivo**

Desarrollar un sistema modular de procesamiento de archivos CSV con configuración segura mediante variables de entorno, aplicando conceptos avanzados de modularización y buenas prácticas de seguridad.

## 🧠 **Conceptos Clave**

- **Modularización avanzada:** Separación en múltiples archivos Python
- **Variables de entorno:** Configuración segura con `python-dotenv`
- **Procesamiento CSV:** Manipulación avanzada con `pandas` y `csv`
- **Manejo de errores robusto:** Try/catch específicos y logging
- **Configuración externa:** Separación de código y configuración
- **Validación de datos:** Esquemas y tipos de datos
- **Logging estructurado:** Trazabilidad y debugging

## ⚙️ **Herramientas/Librerías**

- `Python 3.8+` - Lenguaje base con type hints
- `pandas` - Manipulación y análisis de datos CSV
- `python-dotenv` - Gestión de variables de entorno
- `csv` - Procesamiento nativo de CSV (alternativa ligera)
- `pathlib` - Manejo moderno de rutas de archivos
- `logging` - Sistema de logs estructurado
- `typing` - Type annotations avanzadas
- `dataclasses` - Estructuras de datos modernas
- `configparser` - Configuración avanzada (opcional)

## 🚀 **Proyecto: Sistema de Procesamiento CSV Empresarial**

### **¿Qué construirás?**

Un sistema modular de procesamiento de archivos CSV que permita limpiar, transformar y validar datos con configuración segura mediante variables de entorno y arquitectura escalable.

### **Requisitos obligatorios:**

- [ ] **Arquitectura modular:** Mínimo 4 archivos Python separados
- [ ] **Variables de entorno:** Configuración con `.env` y `python-dotenv`
- [ ] **Procesamiento CSV:** Lectura, limpieza y transformación de datos
- [ ] **Validación robusta:** Esquemas de datos y tipos
- [ ] **Logging estructurado:** Sistema de logs completo
- [ ] **Manejo de errores:** Try/catch específicos por tipo de error
- [ ] **Configuración segura:** Separación completa de credenciales

### **Funcionalidades core:**

- [ ] **Lectura inteligente:** Detección automática de delimitadores y encoding
- [ ] **Limpieza de datos:** Eliminación de duplicados, valores nulos, normalización
- [ ] **Transformaciones:** Conversión de tipos, cálculos derivados, agregaciones
- [ ] **Validación de esquemas:** Verificación de estructura esperada
- [ ] **Exportación flexible:** Múltiples formatos de salida
- [ ] **Reportes de calidad:** Estadísticas de procesamiento

### **Funcionalidades avanzadas (opcionales):**

- [ ] **Procesamiento por lotes:** Múltiples archivos en una ejecución
- [ ] **Configuración dinámica:** Diferentes perfiles de procesamiento
- [ ] **Notificaciones:** Alertas por email/Slack al completar
- [ ] **Monitoreo:** Métricas de rendimiento y calidad
- [ ] **Tests automatizados:** Suite completa de pruebas
- [ ] **CLI interactiva:** Interfaz de línea de comandos

### **Archivos del proyecto:**

```
semana-03-csv-modular/
├── src/                           # 📁 Código fuente principal
│   ├── __init__.py               # 🐍 Inicialización del paquete
│   ├── main.py                   # 🎮 Punto de entrada principal
│   ├── csv_processor.py          # 📊 Lógica de procesamiento CSV
│   ├── data_validator.py         # ✅ Validación y esquemas de datos
│   ├── config_manager.py         # ⚙️ Gestión de configuración
│   └── utils.py                  # 🛠️ Utilidades y helpers
├── config/                       # 📋 Archivos de configuración
│   ├── .env.example             # 📄 Template de variables de entorno
│   ├── logging.conf             # 📝 Configuración de logging
│   └── processing_rules.json    # 🔧 Reglas de procesamiento
├── data/                        # 📁 Datos de entrada y salida
│   ├── input/                   # 📥 CSVs de entrada
│   ├── output/                  # 📤 Archivos procesados
│   └── samples/                 # 📋 Datos de prueba
├── logs/                        # 📜 Archivos de log
├── tests/                       # 🧪 Suite de pruebas
│   ├── test_csv_processor.py    # 🧪 Tests del procesador
│   ├── test_validator.py        # 🧪 Tests del validador
│   └── conftest.py              # 🧪 Configuración de pytest
├── requirements.txt             # 📦 Dependencias del proyecto
├── .env                         # 🔒 Variables de entorno (NO commit)
├── .gitignore                   # 🚫 Archivos a ignorar en Git
└── README.md                    # 📚 Documentación del proyecto
```

## 📚 **Lo que aprenderás**

### **Nuevas habilidades técnicas:**

- **Modularización profesional:** Separación en packages y módulos
- **Gestión de configuración:** Variables de entorno y archivos config
- **Procesamiento de datos:** Pandas avanzado para CSV complejos
- **Logging empresarial:** Trazabilidad y debugging profesional
- **Validación de datos:** Esquemas y control de calidad
- **Manejo de rutas:** Pathlib para gestión moderna de archivos
- **Type hints avanzadas:** Anotaciones complejas y dataclasses
- **Testing modular:** Pruebas por componente individual

### **Habilidades profesionales:**

- **Arquitectura de software:** Diseño escalable y mantenible
- **Seguridad:** Gestión segura de credenciales y configuración
- **DevOps básico:** Configuración de entornos y despliegue
- **Code quality:** Estándares industriales de calidad
- **Documentation:** README técnico y documentación de APIs
- **Error handling:** Recuperación graciosa y logging de errores

### **Patrones de diseño aplicados:**

- **Separación de responsabilidades:** Un módulo, una responsabilidad
- **Dependency injection:** Configuración inyectada, no hardcodeada
- **Factory pattern:** Creación dinámica de procesadores
- **Strategy pattern:** Diferentes estrategias de procesamiento
- **Observer pattern:** Notificaciones de eventos (opcional)

## 💡 **Casos de Uso Reales**

### **🏢 Escenarios Empresariales**

1. **Sistema de ventas:** Procesar exports diarios de CRM
2. **HR Analytics:** Limpiar datos de empleados para reporting
3. **Finanzas:** Normalizar reportes bancarios para conciliación
4. **Marketing:** Procesar leads de múltiples fuentes
5. **Inventario:** Consolidar stocks de diferentes almacenes

### **📊 Tipos de Datos a Procesar**

- **Ventas:** fechas, montos, productos, clientes
- **Usuarios:** emails, nombres, demografía, actividad
- **Transacciones:** IDs, timestamps, estados, montos
- **Inventario:** SKUs, cantidades, ubicaciones, proveedores
- **Logs:** timestamps, eventos, IPs, user agents

## 🛡️ **Buenas Prácticas de Seguridad**

### **🔐 Variables de Entorno**

```python
# ❌ NUNCA hacer esto
DATABASE_URL = "postgresql://user:password@localhost/db"

# ✅ Siempre usar variables de entorno
import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
```

### **📁 Estructura de .env**

```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost/db
DATABASE_TIMEOUT=30

# File Paths
INPUT_DIRECTORY=/path/to/input
OUTPUT_DIRECTORY=/path/to/output

# Processing Configuration
BATCH_SIZE=1000
MAX_FILE_SIZE_MB=100

# Notifications
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/processing.log
```

## 🧪 **Estrategia de Testing**

### **📋 Tipos de Tests**

| Tipo de Test           | Archivo                 | Responsabilidad        |
| ---------------------- | ----------------------- | ---------------------- |
| **Unit Tests**         | `test_csv_processor.py` | Funciones individuales |
| **Integration Tests**  | `test_integration.py`   | Flujo completo         |
| **Data Quality Tests** | `test_data_quality.py`  | Validación de esquemas |
| **Config Tests**       | `test_config.py`        | Variables de entorno   |

### **🔍 Casos de Prueba Críticos**

- ✅ **Archivos malformados:** CSV con errores de formato
- ✅ **Encoding incorrecto:** UTF-8, Latin-1, etc.
- ✅ **Datos faltantes:** Campos vacíos o nulos
- ✅ **Tipos incorrectos:** Strings en campos numéricos
- ✅ **Variables de entorno:** Missing o malformadas
- ✅ **Archivos grandes:** Performance y memoria
- ✅ **Permisos de archivos:** Lectura/escritura restringida

## 📊 **Métricas de Éxito**

### **✅ Criterios de Aceptación**

- **Modularidad:** Código distribuido en 4+ archivos especializados
- **Configuración:** 100% de configuración via variables de entorno
- **Procesamiento:** Manejo de archivos CSV de hasta 100MB
- **Validación:** Detección automática de 5+ tipos de errores de datos
- **Logging:** Trazabilidad completa de todas las operaciones
- **Testing:** Cobertura mínima del 80% en funciones core
- **Documentación:** README con instalación, configuración y uso

### **🎯 KPIs Técnicos**

- **Performance:** Procesar 10,000 filas por segundo mínimo
- **Robustez:** 0 crashes por archivos malformados
- **Escalabilidad:** Procesar archivos de 1GB+ sin memory overflow
- **Mantenibilidad:** Agregar nueva transformación en <30 min
- **Usabilidad:** Setup inicial en <5 minutos siguiendo README

## 🔗 **Recursos Recomendados**

### **📚 Documentación Técnica**

- [Pandas User Guide](https://pandas.pydata.org/docs/user_guide/) - Manipulación de datos
- [Python-dotenv](https://github.com/theskumar/python-dotenv) - Variables de entorno
- [Python Logging HOWTO](https://docs.python.org/3/howto/logging.html) - Sistema de logs
- [Pathlib Guide](https://docs.python.org/3/library/pathlib.html) - Manejo de rutas
- [Type Hints PEP](https://www.python.org/dev/peps/pep-0484/) - Anotaciones de tipos

### **🛠️ Herramientas de Desarrollo**

- [Black](https://github.com/psf/black) - Formatter automático
- [Flake8](https://flake8.pycqa.org/) - Linter y style checker
- [pytest](https://docs.pytest.org/) - Framework de testing
- [mypy](http://mypy-lang.org/) - Type checker estático
- [pre-commit](https://pre-commit.com/) - Hooks de Git

### **📊 Datasets de Práctica**

- [Kaggle Datasets](https://www.kaggle.com/datasets) - Datos reales para practicar
- [UCI ML Repository](https://archive.ics.uci.edu/ml/) - Datasets académicos
- [Government Open Data](https://data.gov/) - Datos públicos gubernamentales
- [Awesome Public Datasets](https://github.com/awesomedata/awesome-public-datasets) - Curación de datasets

## 🎯 **Roadmap de Desarrollo**

### **📅 Cronograma Sugerido (5 días)**

| Día       | Enfoque                   | Actividades                                           |
| --------- | ------------------------- | ----------------------------------------------------- |
| **Día 1** | Setup y arquitectura      | Crear estructura, configurar .env, logging básico     |
| **Día 2** | Procesamiento core        | CSV reader, transformaciones básicas, validación      |
| **Día 3** | Funcionalidades avanzadas | Limpieza de datos, múltiples formatos, error handling |
| **Día 4** | Testing y calidad         | Suite de tests, documentación, optimización           |
| **Día 5** | Integración y deploy      | Tests de integración, README, demo completa           |

### **🚀 Próximos Pasos Post-Semana 3**

**Preparación para Semana 4 (SQL básico):**

- Base sólida en modularización ✅
- Experiencia con configuración externa ✅
- Procesamiento de datos estructurado ✅
- Logging y debugging avanzado ✅
- Testing automatizado establecido ✅

---

**Dificultad:** ⭐⭐⭐☆☆ (Intermedio)  
**Tiempo estimado:** 12-16 horas  
**Semana del roadmap:** 3/32  
**Prerrequisitos:** Completar Semanas 1-2 (Python + Git + OOP)
