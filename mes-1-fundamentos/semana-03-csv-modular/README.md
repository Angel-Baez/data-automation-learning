# 📊 Sistema de Procesamiento CSV Modular

Sistema avanzado de procesamiento de archivos CSV con arquitectura modular, validación de datos y configuración flexible. Proyecto de la **Semana 3** del programa Data + Automation Engineer Journey.

## 🎯 Características Principales

### ✨ Funcionalidades Core

- **Procesamiento Inteligente**: Detección automática de encoding, delimitadores y tipos de datos
- **Validación Avanzada**: Sistema completo de validación con reglas personalizables
- **Arquitectura Modular**: Componentes independientes y reutilizables
- **Configuración Flexible**: Gestión centralizada con archivos .env y JSON
- **Logging Profesional**: Sistema de logs estructurado con múltiples niveles
- **Testing Completo**: Suite de tests unitarios con >95% cobertura

### 🔧 Capacidades Técnicas

- Manejo de archivos CSV de cualquier tamaño
- Transformaciones automáticas de datos
- Limpieza y normalización inteligente
- Generación de reportes de calidad
- Estadísticas detalladas de procesamiento
- Sistema de backup automático

## 🏗️ Arquitectura del Sistema

```
src/
├── config_manager.py     # Gestión centralizada de configuración
├── csv_processor.py      # Procesamiento principal de CSV
├── data_validator.py     # Sistema de validación de datos
└── utils.py             # Utilidades y helpers comunes

tests/                   # Suite completa de tests unitarios
config/                  # Archivos de configuración
data/                   # Directorio para datos de entrada/salida
logs/                   # Archivos de log del sistema
```

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.8+
- pip (gestor de paquetes de Python)

### Instalación

1. **Clonar o descargar el proyecto**

```bash
git clone <repository-url>
cd semana-03-csv-modular
```

2. **Crear entorno virtual (recomendado)**

```bash
python -m venv .venv

# En macOS/Linux:
source .venv/bin/activate

# En Windows:
.venv\Scripts\activate
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

### Configuración Inicial

1. **Variables de entorno** (opcional)

```bash
# Crear archivo .env en la raíz del proyecto
cp .env.example .env

# Editar .env con tus configuraciones:
LOG_LEVEL=INFO
CSV_BATCH_SIZE=10000
ENABLE_BACKUPS=true
MAX_FILE_SIZE_MB=100
```

2. **Configuración de procesamiento** (opcional)

```bash
# El sistema creará automáticamente processing_rules.json
# Puedes personalizarlo según tus necesidades
```

## 📖 Uso del Sistema

### Uso Básico con Script Principal

```bash
# Procesar un archivo CSV
python main.py data/input/mi_archivo.csv

# Procesar con archivo de salida específico
python main.py data/input/ventas.csv --output data/output/ventas_procesadas.csv

# Usar perfil de procesamiento específico
python main.py data/input/datos.csv --profile strict
```

### Uso Programático

```python
from src.config_manager import ConfigManager
from src.csv_processor import CSVProcessor
from src.data_validator import DataValidator

# Inicializar sistema
config = ConfigManager()
processor = CSVProcessor(config)
validator = DataValidator(config)

# Procesar archivo
df, stats, metadata = processor.process_file("datos.csv")

# Validar datos
report = validator.validate_dataframe(df)

print(f"Procesadas {stats.final_rows} filas")
print(f"Calidad de datos: {report.success_rate:.1f}%")
```

### Ejemplos Avanzados

#### Procesamiento por Lotes

```python
import glob
from pathlib import Path

# Procesar múltiples archivos
csv_files = glob.glob("data/input/*.csv")

for file_path in csv_files:
    try:
        df, stats, metadata = processor.process_file(file_path)
        print(f"✅ {file_path}: {stats.final_rows} filas procesadas")
    except Exception as e:
        print(f"❌ Error en {file_path}: {e}")
```

#### Validación Personalizada

```python
from src.data_validator import ValidationRule, ValidationType, ValidationLevel

# Crear regla personalizada
age_rule = ValidationRule(
    name="age_validation",
    description="Edad debe estar entre 18 y 100",
    validation_type=ValidationType.RANGE_CHECK,
    level=ValidationLevel.ERROR,
    column="edad",
    parameters={'min': 18, 'max': 100}
)

validator.add_validation_rule(age_rule)
report = validator.validate_dataframe(df)
```

## 🧪 Testing

Ejecutar la suite completa de tests:

```bash
# Todos los tests
python -m pytest tests/ -v

# Tests con cobertura
python -m pytest tests/ --cov=src --cov-report=html

# Tests específicos
python -m pytest tests/test_csv_processor.py -v
```

### Estructura de Tests

- `test_config_manager.py`: Tests de configuración
- `test_csv_processor.py`: Tests de procesamiento CSV
- `test_data_validator.py`: Tests de validación
- `test_utils.py`: Tests de utilidades

## ⚙️ Configuración Avanzada

### Archivo .env

```env
# Configuración de logging
LOG_LEVEL=INFO
LOG_DIR=logs

# Configuración de procesamiento
CSV_BATCH_SIZE=10000
MAX_FILE_SIZE_MB=100
ENABLE_BACKUPS=true

# Configuración de validación
VALIDATION_ENABLED=true
STRICT_MODE=false
```

### processing_rules.json

```json
{
  "processing_rules": {
    "remove_duplicates": true,
    "fill_missing_values": true,
    "normalize_text": true,
    "convert_data_types": true
  },
  "output_rules": {
    "save_metadata": true,
    "create_summary": true,
    "generate_report": true
  }
}
```

## 📊 Ejemplos de Datos

### CSV de Entrada (ejemplo)

```csv
id,nombre,edad,salario,fecha_ingreso
1,"Juan Pérez",25,50000,2023-01-15
2,"María García",32,65000,2022-11-20
3,"Pedro López",28,,2023-03-10
```

### Salida Procesada

- **Archivo CSV limpio** con datos normalizados
- **Reporte de calidad** con estadísticas detalladas
- **Metadatos** del procesamiento
- **Logs** del proceso completo

## 🔍 Monitoreo y Logs

El sistema genera logs estructurados en múltiples niveles:

```
2025-10-15 10:30:15 - INFO - Iniciando procesamiento de datos.csv
2025-10-15 10:30:16 - DEBUG - Detectado encoding: utf-8, delimitador: ,
2025-10-15 10:30:17 - WARNING - 5 filas con valores faltantes en columna 'salario'
2025-10-15 10:30:18 - INFO - Procesamiento completado: 1000 → 995 filas
```

## 🛠️ Desarrollo y Contribución

### Estructura del Código

- **Tipo hints** completos en todo el código
- **Docstrings** en formato Google Style
- **Tests unitarios** para cada componente
- **Logging profesional** con contexto

### Extensión del Sistema

```python
# Agregar nueva transformación
def mi_transformacion_personalizada(df: pd.DataFrame) -> pd.DataFrame:
    # Tu lógica aquí
    return df

# Registrar en el procesador
processor.add_custom_transformation("mi_transformacion", mi_transformacion_personalizada)
```

## 📈 Rendimiento

### Benchmarks Típicos

- **Archivos pequeños** (<1MB): ~0.1-0.5 segundos
- **Archivos medianos** (1-10MB): ~0.5-2 segundos
- **Archivos grandes** (10-100MB): ~2-10 segundos
- **Memoria utilizada**: ~2-3x el tamaño del archivo

### Optimizaciones Implementadas

- Procesamiento por chunks para archivos grandes
- Detección eficiente de encoding y delimitadores
- Caching de configuraciones frecuentes
- Liberación automática de memoria

## 🎓 Contexto Educativo

Este proyecto forma parte del **programa Data + Automation Engineer Journey**, específicamente de la **Semana 3: CSV Modular**.

### Objetivos de Aprendizaje Alcanzados

- ✅ Arquitectura modular y separación de responsabilidades
- ✅ Manejo profesional de configuración y logging
- ✅ Testing automatizado y TDD
- ✅ Procesamiento eficiente de datos
- ✅ Validación y calidad de datos
- ✅ Documentación técnica completa

### Habilidades Desarrolladas

- Diseño de sistemas escalables
- Manejo avanzado de pandas y numpy
- Testing con pytest
- Gestión de configuración con archivos .env
- Logging estructurado
- Type hints y programación defensiva

## 📝 Notas de Versión

### v1.0.0 (Actual)

- ✨ Sistema completo de procesamiento CSV
- ✨ Validación avanzada de datos
- ✨ Configuración flexible
- ✨ Suite completa de tests (74 tests)
- ✨ Documentación profesional

## 🤝 Soporte

Para reportar bugs o solicitar features:

1. Crear issue en el repositorio
2. Incluir logs y archivos de ejemplo
3. Describir comportamiento esperado vs actual

## 📚 Referencias Técnicas

- **pandas**: Manipulación y análisis de datos
- **pytest**: Framework de testing
- **chardet**: Detección automática de encoding
- **python-dotenv**: Gestión de variables de entorno
- **logging**: Sistema de logs nativo de Python

---

**Desarrollado con ❤️ como parte del Data + Automation Engineer Journey**

_Semana 3: Fundamentos de Python y Procesamiento Modular de Datos_
