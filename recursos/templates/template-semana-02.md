# 📁 Template Semana 2: Sistema de Inventario con Git

## 🎯 **Objetivo**

Desarrollar un sistema completo de gestión de inventario con persistencia JSON, control de versiones Git y arquitectura modular profesional.

## 🧠 **Conceptos Clave**

- **Programación Orientada a Objetos:** Clases, métodos, encapsulación
- **Persistencia de datos:** JSON, backups automáticos
- **Control de versiones:** Git básico (init, add, commit, push)
- **Arquitectura modular:** Separación de responsabilidades
- **Manejo de archivos:** Lectura/escritura, validación de datos
- **Type hints:** Tipado estático en Python

## ⚙️ **Herramientas/Librerías**

- `Python 3.8+` - Lenguaje base con type hints
- `json` - Persistencia de datos
- `datetime` - Timestamps para backups
- `typing` - Type annotations
- `Git` - Control de versiones
- `GitHub` - Repositorio remoto
- `pandas` (opcional) - Procesamiento de datos CSV

## 🚀 **Proyecto: Sistema de Inventario Empresarial**

### **¿Qué construirás?**

Un sistema completo de gestión de inventario con interfaz interactiva, persistencia JSON, funcionalidades CRUD, reportes avanzados y características empresariales.

### **Requisitos obligatorios:**

- [ ] **CRUD completo:** Crear, leer, actualizar, eliminar productos
- [ ] **Persistencia JSON:** Guardar/cargar datos automáticamente
- [ ] **Arquitectura modular:** Mínimo 3 archivos Python separados
- [ ] **Control de versiones:** Git con commits descriptivos
- [ ] **Validación robusta:** Type hints y validación de datos
- [ ] **Interfaz amigable:** Menús claros y navegación intuitiva

### **Funcionalidades avanzadas (opcionales):**

- [ ] **Historial de movimientos:** Log completo de cambios
- [ ] **Categorías inteligentes:** Sugerencias automáticas
- [ ] **Importación CSV:** Carga masiva de productos
- [ ] **Backups automáticos:** Respaldos con timestamp
- [ ] **Reportes analytics:** Estadísticas y alertas
- [ ] **Testing:** Suite de pruebas unitarias

### **Archivos del proyecto:**

```
semana-02-inventario-git/
├── inventario.py       # 🎮 Aplicación principal y menús
├── productos.py        # 📦 Clase Product y validaciones  
├── utils.py           # 🛠️ Utilidades y persistencia
├── historial.py       # 📜 Sistema de auditoría (opcional)
├── categorias.py      # 🏷️ Gestión de categorías (opcional)
├── importar_csv.py    # 📊 Importación masiva (opcional)
├── test_inventario.py # 🧪 Suite de pruebas (opcional)
├── inventario.json    # 💾 Base de datos
├── productos_ejemplo.csv # 📄 Datos de prueba
├── backups/           # 🔄 Respaldos automáticos
└── README.md          # 📚 Documentación profesional
```

## 📚 **Lo que aprenderás**

### **Nuevas habilidades técnicas:**

- **OOP avanzado:** Clases, herencia, encapsulación
- **Persistencia de datos:** JSON como base de datos ligera
- **Git workflow:** add, commit, push, branches
- **Arquitectura de software:** Modularización y responsabilidades
- **Type hints:** Tipado estático para mejor código
- **Testing:** Pruebas unitarias con pytest
- **Documentación:** README profesional con Markdown

### **Habilidades profesionales:**

- **Planificación de software:** Diseño antes de implementación
- **Buenas prácticas:** Código limpio y mantenible
- **Control de versiones:** Commits descriptivos y organizados
- **Testing mindset:** Validación proactiva del código
- **Documentación técnica:** Comunicación efectiva

### **Desafíos comunes y soluciones:**

- **Arquitectura modular** → Separar lógica de negocio, persistencia e interfaz
- **Validación de datos** → Type hints + funciones de validación robustas
- **Manejo de archivos** → Try/except para errores de I/O y JSON
- **Git conflicts** → Commits frecuentes y descriptivos
- **Testing complexity** → Empezar con casos simples, crecer gradualmente

### **Mejoras futuras:**

- [ ] **Base de datos real:** SQLite o PostgreSQL
- [ ] **API REST:** Flask/FastAPI para servicios web  
- [ ] **Interfaz web:** HTML/CSS/JavaScript frontend
- [ ] **Autenticación:** Sistema de usuarios y permisos
- [ ] **Dockerización:** Contenedores para despliegue
- [ ] **CI/CD:** GitHub Actions para automatización

## 📊 **Métricas de éxito**

- ✅ **Funcionalidad:** Todas las operaciones CRUD funcionan
- ✅ **Persistencia:** Datos se mantienen entre sesiones  
- ✅ **Modularidad:** Código organizado en archivos lógicos
- ✅ **Git:** Historial de commits limpio y descriptivo
- ✅ **Validación:** Sistema robusto ante errores de usuario
- ✅ **Testing:** Pruebas cubren funcionalidad crítica
- ✅ **Documentación:** README completo y profesional

## 🔗 **Recursos útiles**

- [Documentación Python - Clases](https://docs.python.org/3/tutorial/classes.html)
- [JSON en Python](https://docs.python.org/3/library/json.html)
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)
- [Type Hints](https://docs.python.org/3/library/typing.html)
- [pytest Documentation](https://docs.pytest.org/)
- [Markdown Guide](https://www.markdownguide.org/)

---

**Dificultad:** ⭐⭐⭐☆☆ (Intermedio)  
**Tiempo estimado:** 8-12 horas  
**Semana del roadmap:** 2/32  
**Prerrequisitos:** Completar Semana 1 - Calculadora Básica