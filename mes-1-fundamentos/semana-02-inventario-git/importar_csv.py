#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 Módulo de Importación CSV - Sistema de Inventario
Proyecto del roadmap Data + Automation Engineer - Semana 2

Autor: Angel Baez
Fecha: Octubre 2025
Descripción: Sistema de importación masiva de productos desde archivos CSV
"""

import csv
import os
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import pandas as pd
from productos import Product, validar_producto_data
from historial import HistorialInventario


class ImportadorCSV:
    """
    Clase para manejar la importación masiva de productos desde CSV
    """

    def __init__(self, historial: Optional[HistorialInventario] = None):
        """Inicializa el importador"""
        self.historial = historial
        self.productos_importados = []
        self.errores = []
        self.estadisticas = {
            "procesados": 0,
            "exitosos": 0,
            "errores": 0,
            "duplicados": 0,
        }

    def validar_archivo_csv(self, archivo_path: str) -> Tuple[bool, str, List[str]]:
        """
        Valida si el archivo CSV existe y tiene el formato correcto

        Returns:
            Tupla (es_valido, mensaje, columnas_encontradas)
        """
        # Verificar que el archivo existe
        if not os.path.exists(archivo_path):
            return False, f"El archivo '{archivo_path}' no existe", []

        # Verificar extensión
        if not archivo_path.lower().endswith(".csv"):
            return False, "El archivo debe tener extensión .csv", []

        try:
            # Leer las primeras filas para validar estructura
            with open(archivo_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                headers = next(reader, None)

                if not headers:
                    return False, "El archivo está vacío o no tiene encabezados", []

                # Verificar columnas requeridas
                columnas_requeridas = {
                    "nombre",
                    "categoria",
                    "precio",
                    "stock",
                    "proveedor",
                }
                headers_lower = [h.lower().strip() for h in headers]

                columnas_faltantes = []
                for col in columnas_requeridas:
                    if col not in headers_lower:
                        columnas_faltantes.append(col)

                if columnas_faltantes:
                    return (
                        False,
                        f"Faltan columnas requeridas: {', '.join(columnas_faltantes)}",
                        headers,
                    )

                return True, "Archivo válido", headers

        except Exception as e:
            return False, f"Error al leer archivo: {str(e)}", []

    def mapear_columnas(self, headers: List[str]) -> Dict[str, str]:
        """
        Mapea los headers del CSV a los campos del producto

        Args:
            headers: Lista de headers del CSV

        Returns:
            Diccionario de mapeo {campo_producto: nombre_columna_csv}
        """
        # Mapeo de posibles nombres de columnas
        mapeo_posible = {
            "nombre": ["nombre", "name", "producto", "product", "item"],
            "categoria": ["categoria", "category", "cat", "tipo", "type"],
            "precio": ["precio", "price", "cost", "costo", "valor", "value"],
            "stock": ["stock", "cantidad", "qty", "inventory", "existencia"],
            "proveedor": ["proveedor", "supplier", "vendor", "distribuidor"],
        }

        mapeo_final = {}
        headers_lower = [h.lower().strip() for h in headers]

        for campo, posibles_nombres in mapeo_posible.items():
            for header_lower in headers_lower:
                if header_lower in posibles_nombres:
                    # Encontrar el header original (con mayúsculas)
                    header_original = headers[headers_lower.index(header_lower)]
                    mapeo_final[campo] = header_original
                    break

        return mapeo_final

    def procesar_fila_csv(
        self, fila: Dict, numero_fila: int, productos_existentes: List[Product]
    ) -> Tuple[bool, Optional[Product], str]:
        """
        Procesa una fila individual del CSV

        Args:
            fila: Diccionario con datos de la fila
            numero_fila: Número de fila para reporte de errores
            productos_existentes: Lista de productos existentes para detectar duplicados

        Returns:
            Tupla (exito, producto_creado, mensaje_error)
        """
        try:
            # Extraer datos de la fila
            nombre = str(fila.get("nombre", "")).strip()
            categoria = str(fila.get("categoria", "")).strip()
            precio_str = str(fila.get("precio", "")).strip()
            stock_str = str(fila.get("stock", "")).strip()
            proveedor = str(fila.get("proveedor", "")).strip()

            # Validar datos básicos
            if not all([nombre, categoria, precio_str, stock_str, proveedor]):
                return False, None, f"Fila {numero_fila}: Faltan campos obligatorios"

            # Convertir y validar tipos de datos
            try:
                precio_validado = float(precio_str.replace(",", "").replace("$", ""))
                stock_validado = int(
                    float(stock_str)
                )  # Permitir decimales que se convertirán a enteros
            except ValueError as e:
                return (
                    False,
                    None,
                    f"Fila {numero_fila}: Error en conversión de datos - {str(e)}",
                )

            # Validar datos del producto (pasar precio y stock como cadenas para coincidir con la firma)
            es_valido, mensaje_validacion, datos_limpios = validar_producto_data(
                nombre, categoria, precio_str, stock_str, proveedor
            )

            if not es_valido:
                return False, None, f"Fila {numero_fila}: {mensaje_validacion}"

            # Verificar duplicados por nombre
            for producto_existente in productos_existentes:
                if producto_existente.nombre.lower() == nombre.lower():
                    self.estadisticas["duplicados"] += 1
                    return (
                        False,
                        None,
                        f"Fila {numero_fila}: Producto duplicado - '{nombre}' ya existe",
                    )

            # Crear producto
            producto = Product(**datos_limpios)

            # Registrar en historial si está disponible
            if self.historial:
                self.historial.registrar_movimiento(
                    tipo="IMPORT",
                    producto=producto,
                    detalle=f"Importado desde CSV - fila {numero_fila}",
                    cantidad_nueva=producto.stock,
                    usuario="Sistema CSV",
                )

            return True, producto, ""

        except Exception as e:
            return False, None, f"Fila {numero_fila}: Error inesperado - {str(e)}"

    def importar_desde_csv(
        self,
        archivo_path: str,
        productos_existentes: Optional[List[Product]] = None,
        continuar_con_errores: bool = True,
    ) -> Tuple[bool, Dict, List[str]]:
        """
        Importa productos desde archivo CSV

        Args:
            archivo_path: Ruta al archivo CSV
            productos_existentes: Lista de productos existentes para evitar duplicados
            continuar_con_errores: Si continuar procesando cuando hay errores

        Returns:
            Tupla (exito_general, estadisticas, lista_errores)
        """
        # Reiniciar estadísticas
        self.estadisticas = {
            "procesados": 0,
            "exitosos": 0,
            "errores": 0,
            "duplicados": 0,
        }
        self.productos_importados = []
        self.errores = []

        if productos_existentes is None:
            productos_existentes = []

        # Validar archivo
        es_valido, mensaje, headers = self.validar_archivo_csv(archivo_path)
        if not es_valido:
            return False, self.estadisticas, [mensaje]

        # Mapear columnas
        mapeo = self.mapear_columnas(headers)
        campos_requeridos = ["nombre", "categoria", "precio", "stock", "proveedor"]

        campos_faltantes = [campo for campo in campos_requeridos if campo not in mapeo]
        if campos_faltantes:
            error = f"No se pudieron mapear las columnas: {', '.join(campos_faltantes)}"
            return False, self.estadisticas, [error]

        try:
            # Usar pandas para lectura más robusta
            df = pd.read_csv(archivo_path, encoding="utf-8")

            # Renombrar columnas según el mapeo
            df_renamed = df.rename(columns={v: k for k, v in mapeo.items()})

            # Asegurar índice entero para evitar errores al sumar
            df_renamed = df_renamed.reset_index(drop=True)

            # Procesar cada fila
            for idx, row in enumerate(df_renamed.iterrows()):
                numero_fila = idx + 2  # +2 porque pandas es 0-indexed y hay header
                _, row_data = row
                self.estadisticas["procesados"] += 1
                # Convertir fila a diccionario
                fila_dict = row_data.to_dict()

                # Procesar fila
                exito, producto, error = self.procesar_fila_csv(
                    fila_dict,
                    numero_fila,
                    productos_existentes + self.productos_importados,
                )

                if exito and producto:
                    self.productos_importados.append(producto)
                    self.estadisticas["exitosos"] += 1
                else:
                    self.errores.append(error)
                    self.estadisticas["errores"] += 1

                    if not continuar_con_errores:
                        break

            # Determinar éxito general
            exito_general = self.estadisticas["exitosos"] > 0

            return exito_general, self.estadisticas, self.errores

        except Exception as e:
            error = f"Error al procesar archivo CSV: {str(e)}"
            return False, self.estadisticas, [error]

    def generar_reporte_importacion(self, archivo_salida: Optional[str] = None) -> str:
        """
        Genera un reporte detallado de la importación

        Args:
            archivo_salida: Ruta del archivo donde guardar el reporte (opcional)

        Returns:
            str: Contenido del reporte
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        reporte = f"""
📊 REPORTE DE IMPORTACIÓN CSV
============================================
📅 Fecha: {timestamp}
📁 Productos procesados: {self.estadisticas['procesados']}
✅ Importados exitosamente: {self.estadisticas['exitosos']}
❌ Errores encontrados: {self.estadisticas['errores']}
🔄 Duplicados detectados: {self.estadisticas['duplicados']}

"""

        if self.productos_importados:
            reporte += "✅ PRODUCTOS IMPORTADOS:\n"
            reporte += "-" * 50 + "\n"
            for i, producto in enumerate(self.productos_importados, 1):
                reporte += f"{i:2}. {producto.nombre} - {producto.categoria} - ${producto.precio} (Stock: {producto.stock})\n"
            reporte += "\n"

        if self.errores:
            reporte += "❌ ERRORES ENCONTRADOS:\n"
            reporte += "-" * 50 + "\n"
            for i, error in enumerate(self.errores, 1):
                reporte += f"{i:2}. {error}\n"
            reporte += "\n"

        # Calcular porcentaje de éxito
        if self.estadisticas["procesados"] > 0:
            porcentaje_exito = (
                self.estadisticas["exitosos"] / self.estadisticas["procesados"]
            ) * 100
            reporte += f"📈 Tasa de éxito: {porcentaje_exito:.1f}%\n"

        reporte += "============================================\n"

        # Guardar en archivo si se especifica
        if archivo_salida:
            try:
                with open(archivo_salida, "w", encoding="utf-8") as f:
                    f.write(reporte)
            except Exception as e:
                reporte += f"\n❌ Error al guardar reporte: {str(e)}\n"

        return reporte

    def exportar_plantilla_csv(
        self, archivo_salida: str = "plantilla_productos.csv"
    ) -> bool:
        """
        Exporta un archivo CSV de plantilla con ejemplos

        Args:
            archivo_salida: Nombre del archivo de plantilla

        Returns:
            bool: True si se exportó exitosamente
        """
        try:
            # Datos de ejemplo
            datos_ejemplo = [
                {
                    "nombre": "Laptop Dell Inspiron",
                    "categoria": "Tecnología",
                    "precio": 599.99,
                    "stock": 5,
                    "proveedor": "TechWorld",
                },
                {
                    "nombre": "Arroz Premium 5kg",
                    "categoria": "Alimentos",
                    "precio": 15.50,
                    "stock": 25,
                    "proveedor": "GranoCorp",
                },
                {
                    "nombre": "Detergente Líquido",
                    "categoria": "Limpieza",
                    "precio": 8.75,
                    "stock": 12,
                    "proveedor": "CleanCorp",
                },
            ]

            with open(archivo_salida, "w", newline="", encoding="utf-8") as csvfile:
                fieldnames = ["nombre", "categoria", "precio", "stock", "proveedor"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for producto in datos_ejemplo:
                    writer.writerow(producto)

            return True

        except Exception as e:
            print(f"❌ Error al exportar plantilla: {str(e)}")
            return False


# Funciones de utilidad para integrar con el sistema existente


def mostrar_vista_previa_csv(archivo_path: str, filas: int = 5):
    """Muestra una vista previa del archivo CSV"""
    try:
        df = pd.read_csv(archivo_path, encoding="utf-8")

        print(f"\n📋 VISTA PREVIA DE '{os.path.basename(archivo_path)}'")
        print("=" * 70)
        print(f"📊 Total de filas: {len(df)}")
        print(f"📋 Columnas: {', '.join(df.columns.tolist())}")
        print("\n🔍 Primeras filas:")
        print("-" * 70)

        # Mostrar las primeras filas
        vista_previa = df.head(filas)

        # Formatear para mostrar
        for i, (index, row) in enumerate(vista_previa.iterrows()):
            print(f"Fila {i + 2}:")  # +2 por header y 0-index
            for col in df.columns:
                valor = row[col]
                if pd.isna(valor):
                    valor = "VACÍO"
                print(f"  {col}: {valor}")
            print()

        print("=" * 70)

    except Exception as e:
        print(f"❌ Error al leer archivo: {str(e)}")


def proceso_importacion_interactivo(
    importador: ImportadorCSV, productos_existentes: List[Product]
):
    """Proceso interactivo de importación de CSV"""
    print("\n📊 IMPORTACIÓN MASIVA DESDE CSV")
    print("=" * 50)

    # Solicitar archivo
    archivo_csv = input(
        "📁 Ruta del archivo CSV (o 'plantilla' para generar ejemplo): "
    ).strip()

    if archivo_csv.lower() == "plantilla":
        if importador.exportar_plantilla_csv():
            print("✅ Plantilla 'plantilla_productos.csv' creada exitosamente")
            print(
                "📝 Edita el archivo con tus productos y vuelve a ejecutar la importación"
            )
        return

    if not archivo_csv:
        print("❌ Debes especificar un archivo CSV")
        return

    # Validar archivo
    es_valido, mensaje, headers = importador.validar_archivo_csv(archivo_csv)
    if not es_valido:
        print(f"❌ {mensaje}")
        return

    print(f"✅ Archivo válido encontrado")
    print(f"📋 Columnas detectadas: {', '.join(headers)}")

    # Mostrar vista previa
    mostrar_vista_previa = (
        input("\n¿Ver vista previa del archivo? (s/n): ").lower().strip()
    )
    if mostrar_vista_previa in ["s", "si", "sí", "y", "yes"]:
        mostrar_vista_previa_csv(archivo_csv)

    # Confirmar importación
    continuar = input("\n¿Proceder con la importación? (s/n): ").lower().strip()
    if continuar not in ["s", "si", "sí", "y", "yes"]:
        print("❌ Importación cancelada")
        return

    # Opciones de importación
    continuar_errores = (
        input("¿Continuar procesando si hay errores? (s/n): ").lower().strip()
    )
    continuar_con_errores = continuar_errores in ["s", "si", "sí", "y", "yes"]

    # Ejecutar importación
    print("\n🔄 Procesando archivo...")
    exito, stats, errores = importador.importar_desde_csv(
        archivo_csv, productos_existentes, continuar_con_errores
    )

    # Mostrar resultados
    print(f"\n📊 RESULTADOS DE LA IMPORTACIÓN")
    print("=" * 50)
    print(f"📁 Procesados: {stats['procesados']}")
    print(f"✅ Exitosos: {stats['exitosos']}")
    print(f"❌ Errores: {stats['errores']}")
    print(f"🔄 Duplicados: {stats['duplicados']}")

    if stats["procesados"] > 0:
        porcentaje = (stats["exitosos"] / stats["procesados"]) * 100
        print(f"📈 Tasa de éxito: {porcentaje:.1f}%")

    # Mostrar errores si los hay
    if errores:
        print(f"\n❌ ERRORES ENCONTRADOS:")
        for error in errores[:10]:  # Mostrar solo los primeros 10
            print(f"   • {error}")
        if len(errores) > 10:
            print(f"   ... y {len(errores) - 10} errores más")

    # Generar reporte
    generar_reporte = input("\n¿Generar reporte detallado? (s/n): ").lower().strip()
    if generar_reporte in ["s", "si", "sí", "y", "yes"]:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo_reporte = f"reporte_importacion_{timestamp}.txt"
        importador.generar_reporte_importacion(archivo_reporte)
        print(f"📄 Reporte guardado en: {archivo_reporte}")

    print("=" * 50)

    return importador.productos_importados
