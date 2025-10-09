# 🔧 Comandos Git Esenciales

## 📚 **Configuración inicial (solo una vez)**

```bash
# Configurar identidad
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@ejemplo.com"

# Ver configuración
git config --list
```

## 🚀 **Flujo básico diario**

```bash
# Ver estado actual
git status

# Agregar archivos al staging
git add .                    # Todos los archivos
git add archivo.py          # Archivo específico
git add carpeta/            # Carpeta específica

# Hacer commit
git commit -m "✨ Descripción del cambio"

# Subir a GitHub
git push origin main
```

## 📝 **Convenciones de commits**

### **Emojis para commits:**

- ✨ `:sparkles:` - Nueva funcionalidad
- 🐛 `:bug:` - Bug fix
- 📚 `:books:` - Documentación
- 🔧 `:wrench:` - Configuración
- ♻️ `:recycle:` - Refactoring
- ✅ `:white_check_mark:` - Tests
- 🚀 `:rocket:` - Deploy/Release

### **Ejemplos:**

```bash
git commit -m "✨ Añadir calculadora básica - Semana 1"
git commit -m "🐛 Corregir división por cero en calculadora"
git commit -m "📚 Actualizar README con instrucciones de instalación"
git commit -m "🔧 Agregar .env.example para configuración"
```

## 🌿 **Trabajo con branches**

```bash
# Ver branches
git branch                   # Locales
git branch -r               # Remotas
git branch -a               # Todas

# Crear nueva branch
git checkout -b feature/nueva-funcionalidad
git checkout -b semana-05-apis

# Cambiar de branch
git checkout main
git checkout nombre-branch

# Merge (desde main)
git checkout main
git merge feature/nueva-funcionalidad

# Eliminar branch
git branch -d nombre-branch     # Local
git push origin --delete nombre-branch  # Remota
```

## 🔄 **Sincronización con GitHub**

```bash
# Clonar repositorio
git clone https://github.com/usuario/repo.git

# Actualizar desde GitHub
git pull origin main

# Ver remotes
git remote -v

# Agregar remote
git remote add origin https://github.com/usuario/repo.git
```

## 🕰️ **Historial y navegación**

```bash
# Ver historial
git log --oneline           # Compacto
git log --graph            # Con gráfico
git log -5                 # Últimos 5 commits

# Ver cambios
git diff                   # Cambios no staged
git diff --staged          # Cambios staged
git diff HEAD~1            # Comparar con commit anterior

# Ver archivos en un commit
git show --name-only commit-hash
```

## ⚡ **Comandos útiles**

```bash
# Deshacer cambios
git checkout -- archivo.py     # Descartar cambios no staged
git reset HEAD archivo.py      # Quitar del staging
git reset --soft HEAD~1        # Deshacer último commit (mantener cambios)
git reset --hard HEAD~1        # Deshacer último commit (perder cambios)

# Stash (guardar cambios temporalmente)
git stash                      # Guardar cambios
git stash list                 # Ver stashes
git stash apply                # Aplicar último stash
git stash drop                 # Eliminar último stash

# Información útil
git status -s                  # Status compacto
git blame archivo.py           # Ver quién modificó cada línea
git ls-files                   # Lista archivos trackeados
```

## 🔍 **Troubleshooting común**

### **Error: "Please tell me who you are"**

```bash
git config --global user.email "tu-email@ejemplo.com"
git config --global user.name "Tu Nombre"
```

### **Conflicto de merge**

```bash
# 1. Ver archivos con conflicto
git status

# 2. Editar archivos manualmente (eliminar <<<< ==== >>>>)

# 3. Agregar archivos resueltos
git add archivo-conflictivo.py

# 4. Completar merge
git commit -m "🔀 Resolver conflictos de merge"
```

### **Olvidé hacer pull antes de push**

```bash
# Si hay conflictos:
git pull origin main    # Resolver conflictos si los hay
git push origin main

# Si no hay conflictos pero hay commits nuevos:
git pull --rebase origin main
git push origin main
```

## 📋 **Flujo de trabajo semanal sugerido**

### **Lunes - Inicio de semana:**

```bash
git checkout main
git pull origin main
git checkout -b semana-XX-nombre
```

### **Durante la semana - Commits frecuentes:**

```bash
git add .
git commit -m "🚧 WIP: Avance en [funcionalidad]"
git push origin semana-XX-nombre
```

### **Viernes - Finalizar semana:**

```bash
git add .
git commit -m "✅ Completar proyecto semana XX - [nombre]"
git push origin semana-XX-nombre

# Merge a main
git checkout main
git merge semana-XX-nombre
git push origin main
```

## 🎯 **Git hooks útiles (avanzado)**

### **Pre-commit hook para Python:**

```bash
# Instalar pre-commit
pip install pre-commit

# Crear .pre-commit-config.yaml
```

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
```

```bash
# Instalar hooks
pre-commit install
```
