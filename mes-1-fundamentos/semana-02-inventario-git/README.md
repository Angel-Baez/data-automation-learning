# 📦 Sistema de Inventario - Semana 2

**Proyecto del roadmap Data + Automation Engineer**

Un sistema completo de gestión de inventario desarrollado en Python con persistencia JSON, interfaz interactiva y funcionalidades avanzadas de reportes.

## 🎯 Objetivos de Aprendizaje

✅ **Python avanzado:** Estructuras de datos, OOP, type hints  
✅ **Git básico:** Control de versiones y buenas prácticas  
✅ **Manejo de archivos:** JSON, CSV, backups automáticos  
✅ **Modularización:** Separación de responsabilidades

## 🚀 Características

### 📋 **Funcionalidades CRUD**

- ➕ **Agregar productos** con validación completa
- 📖 **Ver inventario** con tabla formateada
- 🔍 **Buscar productos** por nombre, categoría, proveedor o ID
- ✏️ **Actualizar productos** con confirmaciones
- 🗑️ **Eliminar productos** con validación de seguridad

### 📊 **Reportes y Analytics**

- 📈 **Estadísticas generales:** Total productos, stock, valor del inventario
- ⚠️ **Alertas de stock bajo** (≤10 unidades)
- 📂 **Agrupación por categorías**
- 💾 **Exportación a CSV** para análisis externos

### 🛡️ **Características Avanzadas**

- 🔄 **Backups automáticos** con timestamp
- 💾 **Persistencia JSON** con manejo de errores
- 🎨 **Interfaz amigable** con emojis y formato claro
- ✅ **Validación de datos** robusta
- 🔢 **IDs únicos automáticos**
- ⚠️ **Control de cambios sin guardar**

## 🏗️ Arquitectura

```
semana-02-inventario-git/
├── inventario.py       # 🎮 Aplicación principal y menús
├── productos.py        # 📦 Clase Product y validaciones
├── utils.py           # 🛠️ Utilidades, persistencia y UI
├── inventario.json    # 💾 Base de datos JSON
├── backups/          # 🔄 Respaldos automáticos
└── README.md         # 📚 Documentación
```

### 🧩 **Separación de Responsabilidades**

| Módulo          | Responsabilidad                            |
| --------------- | ------------------------------------------ |
| `inventario.py` | Flujo principal, menús, coordinación       |
| `productos.py`  | Modelo de datos, validaciones de negocio   |
| `utils.py`      | Persistencia, utilidades, interfaz usuario |

## 🛠️ Instalación y Uso

### **Prerrequisitos**

- Python 3.8+
- Entorno virtual configurado

### **1. Configurar entorno**

```bash
# Activar entorno virtual
source .venv/bin/activate

# Verificar Python
python --version
```

### **2. Ejecutar el sistema**

```bash
cd mes-1-fundamentos/semana-02-inventario-git
python inventario.py
```

### **3. Primer uso**

```
🚀 Iniciando Sistema de Inventario...
📄 Archivo inventario.json no existe. Creando inventario nuevo...
============ 📦 SISTEMA DE INVENTARIO - SEMANA 2 ============
1. ➕ Agregar producto
2. 📋 Ver todos los productos
[...]
```

## 💡 Ejemplos de Uso

### **Agregar un producto**

```
Nombre del producto: Laptop Dell Inspiron
Categoría: Electrónicos
Precio: 599.99
Stock inicial: 5
Proveedor: TechWorld
✅ Producto agregado exitosamente: [123456] Laptop Dell Inspiron - $599.99
```

### **Ver estadísticas**

```
📦 Total de productos: 15
📈 Stock total: 234 unidades
💰 Valor total del inventario: $12,450.75
💵 Precio promedio: $83.01
🏷️ Categorías: 5 (Electrónicos, Hogar, Oficina, ...)
```

### **Búsqueda por categoría**

```
Categoría a buscar: Electrónicos
========= RESULTADOS - CATEGORÍA: 'Electrónicos' ==========
ID       Nombre               Precio     Stock    Proveedor
--------------------------------------------------------
123456   Laptop Dell Inspiron $599.99    5       TechWorld
789012   Mouse Logitech       $25.99     12      TechSupply
```

## 📂 **Estructura de Datos**

### **Modelo Product**

```python
{
    "id": 123456,
    "nombre": "Laptop Dell Inspiron",
    "categoria": "Electrónicos",
    "precio": 599.99,
    "stock": 5,
    "fecha_ingreso": "2025-10-09",
    "proveedor": "TechWorld"
}
```

### **Archivo inventario.json**

```json
[
  {
    "id": 466155,
    "nombre": "Arroz",
    "categoria": "Cereales",
    "precio": 34.95,
    "stock": 20,
    "fecha_ingreso": "2025-10-09",
    "proveedor": "Agromesa"
  }
]
```

## 🎮 **Menú Principal**

| Opción | Funcionalidad                                      |
| ------ | -------------------------------------------------- |
| 1      | ➕ Agregar nuevo producto                          |
| 2      | 📋 Ver todos los productos                         |
| 3      | 🔍 Buscar producto (nombre/categoría/proveedor/ID) |
| 4      | ✏️ Actualizar producto existente                   |
| 5      | 🗑️ Eliminar producto                               |
| 6      | 📊 Reportes y estadísticas                         |
| 7      | 💾 Guardar datos                                   |
| 8      | 🔄 Recargar datos del archivo                      |
| 9      | 🚪 Salir                                           |

## 📊 **Reportes Disponibles**

| Reporte                    | Descripción                                         |
| -------------------------- | --------------------------------------------------- |
| **Estadísticas generales** | Total productos, stock, valor inventario, promedios |
| **Stock bajo**             | Productos con ≤10 unidades                          |
| **Por categoría**          | Agrupación y conteo por categorías                  |
| **Exportar CSV**           | Generar reporte para análisis externos              |

## 🔧 **Funciones Principales**

### **Validaciones**

- Precio > 0
- Stock ≥ 0
- Campos obligatorios no vacíos
- Formato de datos correcto

### **Persistencia**

- Auto-guardado opcional
- Backups automáticos con timestamp
- Recuperación de errores JSON
- Confirmación de cambios no guardados

### **Interfaz Usuario**

- Menús interactivos con navegación intuitiva
- Tablas formateadas para visualización de datos
- Confirmaciones para acciones destructivas
- Mensajes de error y éxito claros

## 🐛 **Manejo de Errores**

- **JSON corrupto:** Se crea inventario nuevo
- **Archivo no encontrado:** Inicialización automática
- **Entrada inválida:** Validación y re-solicitud
- **División por cero:** Manejado en estadísticas
- **IDs duplicados:** Generación automática única

## 📋 **Próximas Mejoras**

- [ ] 🧪 Tests unitarios con pytest
- [ ] 📊 Dashboard web con Flask
- [ ] 🔍 Búsqueda por rango de precios
- [ ] 📱 API REST para integración
- [ ] 📈 Historial de movimientos de stock
- [ ] 🏷️ Sistema de etiquetas/tags

## 🏆 **Logros de Aprendizaje**

✅ **Python Avanzado:** OOP, type hints, manejo de excepciones  
✅ **Modularización:** Separación clara de responsabilidades  
✅ **Persistencia:** JSON y CSV con validación  
✅ **UX/UI:** Interfaz intuitiva y amigable  
✅ **Validación:** Control robusto de entrada de datos  
✅ **Documentación:** Docstrings completos

## 👤 **Autor**

**Angel Baez**  
📧 Proyecto: Data + Automation Engineer Journey  
📅 Fecha: Octubre 2025  
🎯 Semana 2: Estructuras de datos + Git básico

---

## 📖 **Parte del Roadmap**

Este proyecto corresponde a la **Semana 2** del roadmap de 32 semanas para convertirse en **Data + Automation Engineer**.

**Objetivos cumplidos:**

- ✅ Dominar estructuras de datos de Python
- ✅ Crear script de inventario funcional
- ✅ Implementar Git básico
- ✅ Manejo profesional de archivos

**Siguiente paso:** → **Semana 3** - Procesamiento CSV modular + Variables de entorno
