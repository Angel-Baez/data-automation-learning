# 🔢 Calculadora Básica - Semana 1

## 🎯 **Objetivo**

Crear una calculadora básica con Python que demuestre el manejo de funciones, variables, operadores y estructuras de control.

## 🧠 **Conceptos Clave**

- **Funciones:** Definición, parámetros, return
- **Tipos de datos:** int, float, string
- **Estructuras de control:** if/elif/else, while/for
- **Manejo de errores:** try/except básico
- **Input/Output:** input(), print()

## ⚙️ **Herramientas/Librerías**

- `Python 3.11+` - Lenguaje base
- `VS Code` - Editor de código
- `Git` - Control de versiones

## 🚀 **Proyecto: Calculadora Interactiva**

### **¿Qué construirás?**

Una calculadora de consola que permita realizar operaciones matemáticas básicas con manejo de errores y interfaz amigable.

### **Requisitos:**

- [ ] Operaciones básicas: suma, resta, multiplicación, división
- [ ] Manejo de división por cero
- [ ] Interfaz de usuario en consola
- [ ] Validación de entrada de datos
- [ ] Opción para realizar múltiples cálculos
- [ ] Código modular con funciones separadas

### **Archivos creados:**

- `calculadora.py` - Programa principal
- `README.md` - Documentación del proyecto

## 📁 **Estructura del proyecto:**

```
semana-01-calculadora/
├── calculadora.py
├── README.md
└── screenshots/
    └── demo.png
```

## 🎮 **Funcionalidades**

### **Menú principal:**

```
🔢 CALCULADORA BÁSICA
==================
1. ➕ Sumar
2. ➖ Restar
3. ✖️  Multiplicar
4. ➗ Dividir
5. 🚪 Salir

Elige una operación (1-5):
```

### **Validaciones:**

- Entrada de números válidos
- División por cero
- Opciones de menú válidas
- Continuar o salir después de cada operación

## 📚 **Lo que aprenderé**

### **Nuevas habilidades:**

- Definir y usar funciones en Python
- Manejo básico de excepciones
- Validación de entrada de usuario
- Estructuras de control y bucles
- Organización de código modular

### **Conceptos Python:**

```python
# Función básica
def sumar(a, b):
    return a + b

# Manejo de errores
try:
    resultado = dividir(10, 0)
except ZeroDivisionError:
    print("Error: División por cero")

# Validación de entrada
while True:
    try:
        numero = float(input("Ingresa un número: "))
        break
    except ValueError:
        print("Por favor ingresa un número válido")
```

## 🔗 **Recursos útiles**

- [Python Functions - Documentación oficial](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
- [Exception Handling](https://docs.python.org/3/tutorial/errors.html)
- [Input/Output Tutorial](https://docs.python.org/3/tutorial/inputoutput.html)

---

**Fecha inicio:** 09/10/2025  
**Fecha finalización:** **_/_**/**\_**  
**Tiempo estimado:** 2-3 horas
