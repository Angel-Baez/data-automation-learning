#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛠️ Utilidades - Sistema de Inventario
Proyecto del roadmap Data + Automation Engineer - Semana 2

Autor: Angel Baez
Fecha: Octubre 2025
Descripción: Funciones auxiliares para manejo de archivos, validaciones y UI
"""

import json
import os
from datetime import datetime
from typing import List, Optional
from productos import Product


# Configuración
ARCHIVO_INVENTARIO = "inventario.json"
BACKUP_DIR = "backups"


def cargar_inventario(archivo: str = ARCHIVO_INVENTARIO) -> List[Product]:
    """
    Carga el inventario desde archivo JSON

    Args:
        archivo: Ruta del archivo JSON

    Returns:
        List[Product]: Lista de productos cargados
    """
    try:
        if not os.path.exists(archivo):
            print(f"📄 Archivo {archivo} no existe. Creando inventario nuevo...")
            return []

        with open(archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
            productos = [Product.from_dict(item) for item in datos]
            print(f"✅ Inventario cargado: {len(productos)} productos")
            return productos

    except json.JSONDecodeError as e:
        print(f"❌ Error al leer JSON: {e}")
        return []
    except Exception as e:
        print(f"❌ Error al cargar inventario: {e}")
        return []


def guardar_inventario(
    productos: List[Product], archivo: str = ARCHIVO_INVENTARIO
) -> bool:
    """
    Guarda el inventario en archivo JSON

    Args:
        productos: Lista de productos a guardar
        archivo: Ruta del archivo JSON

    Returns:
        bool: True si se guardó correctamente
    """
    try:
        # Crear backup si el archivo existe
        if os.path.exists(archivo):
            crear_backup(archivo)

        datos = [producto.to_dict() for producto in productos]

        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)

        print(f"💾 Inventario guardado: {len(productos)} productos")
        return True

    except Exception as e:
        print(f"❌ Error al guardar inventario: {e}")
        return False


def crear_backup(archivo: str) -> bool:
    """
    Crea un backup del archivo de inventario

    Args:
        archivo: Archivo a respaldar

    Returns:
        bool: True si se creó el backup
    """
    try:
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_base = os.path.splitext(os.path.basename(archivo))[0]
        backup_path = os.path.join(BACKUP_DIR, f"{nombre_base}_backup_{timestamp}.json")

        import shutil

        shutil.copy2(archivo, backup_path)

        print(f"🔄 Backup creado: {backup_path}")
        return True

    except Exception as e:
        print(f"⚠️  Error al crear backup: {e}")
        return False


def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system("cls" if os.name == "nt" else "clear")


def mostrar_separador(titulo: str = "", char: str = "=", ancho: int = 50):
    """
    Muestra un separador visual con título opcional

    Args:
        titulo: Título a mostrar en el separador
        char: Carácter para el separador
        ancho: Ancho del separador
    """
    if titulo:
        titulo_formateado = f" {titulo} "
        padding = (ancho - len(titulo_formateado)) // 2
        separador = char * padding + titulo_formateado + char * padding
        if len(separador) < ancho:
            separador += char
    else:
        separador = char * ancho

    print(separador)


def mostrar_tabla_productos(productos: List[Product], titulo: str = ""):
    """
    Muestra una tabla formateada de productos

    Args:
        productos: Lista de productos a mostrar
        titulo: Título opcional para la tabla
    """
    if not productos:
        print("📭 No hay productos para mostrar")
        return

    if titulo:
        mostrar_separador(titulo)

    # Headers
    print(
        f"{'ID':<8} {'Nombre':<20} {'Categoría':<15} {'Precio':<10} {'Stock':<8} {'Proveedor':<15}"
    )
    print("-" * 80)

    # Productos
    for producto in productos:
        print(
            f"{producto.id:<8} {producto.nombre[:19]:<20} {producto.categoria[:14]:<15} "
            f"${producto.precio:<9.2f} {producto.stock:<8} {producto.proveedor[:14]:<15}"
        )

    print("-" * 80)
    print(f"Total productos: {len(productos)}")


def obtener_input_validado(
    prompt: str, tipo: str = "str", requerido: bool = True
) -> Optional[str]:
    """
    Obtiene input del usuario con validación

    Args:
        prompt: Mensaje a mostrar
        tipo: Tipo de dato esperado ('str', 'int', 'float')
        requerido: Si el campo es obligatorio

    Returns:
        str: Input validado o None si se cancela
    """
    while True:
        try:
            valor = input(f"{prompt}: ").strip()

            # Permitir cancelar con entrada vacía si no es requerido
            if not valor and not requerido:
                return None

            # Validar si es requerido
            if not valor and requerido:
                print("❌ Este campo es requerido")
                continue

            # Validar según tipo
            if tipo == "int":
                int(valor)
            elif tipo == "float":
                float(valor)

            return valor

        except ValueError:
            print(f"❌ Por favor ingresa un {tipo} válido")
        except KeyboardInterrupt:
            print("\n🚫 Operación cancelada")
            return None


def confirmar_accion(mensaje: str = "¿Estás seguro?") -> bool:
    """
    Solicita confirmación del usuario

    Args:
        mensaje: Mensaje de confirmación

    Returns:
        bool: True si confirma, False si no
    """
    while True:
        respuesta = input(f"{mensaje} (s/n): ").lower().strip()
        if respuesta in ["s", "si", "sí", "y", "yes"]:
            return True
        elif respuesta in ["n", "no"]:
            return False
        else:
            print("❌ Por favor responde con 's' para sí o 'n' para no")


def mostrar_estadisticas(productos: List[Product]):
    """
    Muestra estadísticas del inventario

    Args:
        productos: Lista de productos
    """
    if not productos:
        print("📭 No hay productos para mostrar estadísticas")
        return

    from productos import (
        categorias_disponibles,
        valor_total_inventario,
        producto_mas_caro,
        producto_mas_stock,
        productos_bajo_stock,
    )

    mostrar_separador("📊 ESTADÍSTICAS DEL INVENTARIO")

    # Estadísticas básicas
    total_productos = len(productos)
    total_stock = sum(p.stock for p in productos)
    valor_total = valor_total_inventario(productos)
    precio_promedio = sum(p.precio for p in productos) / total_productos

    print(f"📦 Total de productos: {total_productos}")
    print(f"📈 Stock total: {total_stock} unidades")
    print(f"💰 Valor total del inventario: ${valor_total:,.2f}")
    print(f"💵 Precio promedio: ${precio_promedio:.2f}")

    # Categorías
    categorias = categorias_disponibles(productos)
    print(f"🏷️  Categorías: {len(categorias)} ({', '.join(sorted(categorias))})")

    # Productos destacados
    mas_caro = producto_mas_caro(productos)
    mas_stock = producto_mas_stock(productos)

    if mas_caro:
        print(f"\n🏆 Producto más caro: {mas_caro.nombre} (${mas_caro.precio})")
    else:
        print("\n🏆 Producto más caro: N/A")

    if mas_stock:
        print(f"📦 Mayor stock: {mas_stock.nombre} ({mas_stock.stock} unidades)")
    else:
        print("📦 Mayor stock: N/A")

    # Alertas
    bajo_stock = productos_bajo_stock(productos, 10)
    if bajo_stock:
        print(f"\n⚠️  Productos con stock bajo (≤10): {len(bajo_stock)}")
        for producto in bajo_stock[:5]:  # Mostrar solo los primeros 5
            print(f"   • {producto.nombre}: {producto.stock} unidades")
        if len(bajo_stock) > 5:
            print(f"   ... y {len(bajo_stock) - 5} más")


def pausar():
    """Pausa la ejecución hasta que el usuario presione Enter"""
    input("\n⏸️  Presiona Enter para continuar...")


def mostrar_menu_principal():
    """Muestra el menú principal del sistema"""
    limpiar_pantalla()
    mostrar_separador("📦 SISTEMA DE INVENTARIO - SEMANA 2", "=", 60)
    print("1. ➕ Agregar producto")
    print("2. 📋 Ver todos los productos")
    print("3. 🔍 Buscar producto")
    print("4. ✏️  Actualizar producto")
    print("5. 🗑️  Eliminar producto")
    print("6. 📊 Reportes y estadísticas")
    print("7. 💾 Guardar datos")
    print("8. 🔄 Recargar datos")
    print("9. 🚪 Salir")
    mostrar_separador("", "-", 60)


def obtener_opcion_menu(min_opcion: int = 1, max_opcion: int = 9) -> int:
    """
    Obtiene y valida la opción del menú

    Args:
        min_opcion: Opción mínima válida
        max_opcion: Opción máxima válida

    Returns:
        int: Opción válida seleccionada
    """
    while True:
        try:
            opcion = int(input(f"Elige una opción ({min_opcion}-{max_opcion}): "))
            if min_opcion <= opcion <= max_opcion:
                return opcion
            else:
                print(
                    f"❌ Por favor elige una opción entre {min_opcion} y {max_opcion}"
                )
        except ValueError:
            print("❌ Por favor ingresa un número válido")
        except KeyboardInterrupt:
            print("\n🚫 Operación cancelada")
            return max_opcion  # Opción de salir por defecto


def exportar_reporte_csv(
    productos: List[Product], archivo: Optional[str] = None
) -> bool:
    """
    Exporta el inventario a CSV

    Args:
        productos: Lista de productos
        archivo: Nombre del archivo (opcional)

    Returns:
        bool: True si se exportó correctamente
    """
    try:
        import csv

        if not archivo:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archivo = f"inventario_reporte_{timestamp}.csv"

        with open(archivo, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "id",
                    "nombre",
                    "categoria",
                    "precio",
                    "stock",
                    "fecha_ingreso",
                    "proveedor",
                ],
            )
            writer.writeheader()
            for producto in productos:
                writer.writerow(producto.to_dict())

        print(f"📄 Reporte CSV exportado: {archivo}")
        return True

    except Exception as e:
        print(f"❌ Error al exportar CSV: {e}")
        return False
