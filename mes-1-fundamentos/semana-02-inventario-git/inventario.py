#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📦 Sistema de Inventario - Semana 2
Proyecto del roadmap Data + Automation Engineer

Autor: Angel Baez
Fecha: Octubre 2025
Descripción: Sistema completo de inventario con CRUD, persistencia JSON y Git
"""

from typing import List, Optional
from productos import (
    Product,
    validar_producto_data,
    buscar_productos,
    productos_bajo_stock,
)
from utils import (
    cargar_inventario,
    guardar_inventario,
    mostrar_tabla_productos,
    obtener_input_validado,
    confirmar_accion,
    mostrar_estadisticas,
    pausar,
    mostrar_menu_principal,
    obtener_opcion_menu,
    exportar_reporte_csv,
    mostrar_separador,
    limpiar_pantalla,
)

# Nuevos módulos agregados
from historial import (
    HistorialInventario,
    mostrar_historial_producto,
    mostrar_resumen_actividad,
    mostrar_movimientos_recientes,
)
from categorias import (
    GestorCategorias,
    obtener_categoria_con_sugerencias,
    mostrar_estadisticas_categorias,
)
from importar_csv import ImportadorCSV, proceso_importacion_interactivo


class SistemaInventario:
    """
    Clase principal del sistema de inventario
    """

    def __init__(self):
        """Inicializa el sistema de inventario"""
        self.productos: List[Product] = []
        self.cambios_sin_guardar = False

        # Inicializar nuevos módulos
        self.historial = HistorialInventario()
        self.gestor_categorias = GestorCategorias()
        self.importador_csv = ImportadorCSV(self.historial)

        print("🚀 Iniciando Sistema de Inventario Avanzado...")
        self.cargar_datos()

    def cargar_datos(self):
        """Carga los datos del inventario"""
        self.productos = cargar_inventario()
        self.cambios_sin_guardar = False

    def marcar_cambios(self):
        """Marca que hay cambios sin guardar"""
        self.cambios_sin_guardar = True

    def agregar_producto(self):
        """Agrega un nuevo producto al inventario"""
        limpiar_pantalla()
        mostrar_separador("➕ AGREGAR NUEVO PRODUCTO")

        print("Ingresa los datos del producto (Ctrl+C para cancelar):")

        try:
            nombre = obtener_input_validado("Nombre del producto")
            if not nombre:
                return

            categoria = obtener_categoria_con_sugerencias(
                self.gestor_categorias, "Categoría"
            )
            if not categoria:
                return

            precio = obtener_input_validado("Precio", "float")
            if not precio:
                return

            stock = obtener_input_validado("Stock inicial", "int")
            if not stock:
                return

            proveedor = obtener_input_validado("Proveedor")
            if not proveedor:
                return

            # Validar datos
            es_valido, mensaje, datos = validar_producto_data(
                nombre, categoria, precio, stock, proveedor
            )

            if not es_valido:
                print(f"❌ Errores en los datos: {mensaje}")
                pausar()
                return

            # Crear producto
            nuevo_producto = Product(**datos)
            self.productos.append(nuevo_producto)

            # Registrar en historial
            self.historial.registrar_movimiento(
                tipo="CREATE",
                producto=nuevo_producto,
                detalle=f"Producto creado - Stock inicial: {nuevo_producto.stock}",
                cantidad_nueva=nuevo_producto.stock,
                usuario="Usuario Manual",
            )

            self.marcar_cambios()

            print(f"✅ Producto agregado exitosamente:")
            print(f"   {nuevo_producto}")

        except KeyboardInterrupt:
            print("\n🚫 Operación cancelada")

        pausar()

    def ver_todos_productos(self):
        """Muestra todos los productos del inventario"""
        limpiar_pantalla()
        mostrar_tabla_productos(self.productos, "📋 TODOS LOS PRODUCTOS")
        pausar()

    def buscar_producto(self):
        """Busca productos por diferentes criterios"""
        limpiar_pantalla()
        mostrar_separador("🔍 BUSCAR PRODUCTOS")

        print("¿Por qué campo deseas buscar?")
        print("1. Nombre")
        print("2. Categoría")
        print("3. Proveedor")
        print("4. Buscar por ID")

        try:
            opcion = obtener_opcion_menu(1, 4)

            if opcion == 4:
                # Buscar por ID
                producto_id = obtener_input_validado("ID del producto", "int")
                if not producto_id:
                    return

                producto = self.encontrar_producto_por_id(int(producto_id))
                if producto:
                    mostrar_tabla_productos([producto], f"PRODUCTO ID: {producto_id}")
                else:
                    print(f"❌ No se encontró producto con ID: {producto_id}")
            else:
                # Buscar por texto
                campos = {1: "nombre", 2: "categoria", 3: "proveedor"}
                campo = campos[opcion]

                termino = obtener_input_validado(f"Término de búsqueda ({campo})")
                if not termino:
                    return

                resultados = buscar_productos(self.productos, termino, campo)

                if resultados:
                    mostrar_tabla_productos(
                        resultados, f"RESULTADOS - {campo.upper()}: '{termino}'"
                    )
                else:
                    print(f"❌ No se encontraron productos con '{termino}' en {campo}")

        except KeyboardInterrupt:
            print("\n🚫 Búsqueda cancelada")

        pausar()

    def encontrar_producto_por_id(self, product_id: int) -> Optional[Product]:
        """
        Encuentra un producto por su ID

        Args:
            product_id: ID del producto a buscar

        Returns:
            Product: Producto encontrado o None
        """
        for producto in self.productos:
            if producto.id == product_id:
                return producto
        return None

    def actualizar_producto(self):
        """Actualiza un producto existente"""
        limpiar_pantalla()
        mostrar_separador("✏️ ACTUALIZAR PRODUCTO")

        if not self.productos:
            print("📭 No hay productos para actualizar")
            pausar()
            return

        try:
            product_id = obtener_input_validado("ID del producto a actualizar", "int")
            if not product_id:
                return

            producto = self.encontrar_producto_por_id(int(product_id))
            if not producto:
                print(f"❌ No se encontró producto con ID: {product_id}")
                pausar()
                return

            print(f"\n📦 Producto actual:")
            mostrar_tabla_productos([producto])

            print("\n¿Qué deseas actualizar?")
            print("1. Nombre")
            print("2. Categoría")
            print("3. Precio")
            print("4. Stock")
            print("5. Proveedor")
            print("6. Todo")

            opcion = obtener_opcion_menu(1, 6)

            if opcion == 1:
                nuevo_nombre = obtener_input_validado("Nuevo nombre", requerido=False)
                if nuevo_nombre:
                    producto.nombre = nuevo_nombre.strip().title()
                    self.marcar_cambios()

            elif opcion == 2:
                nueva_categoria = obtener_input_validado(
                    "Nueva categoría", requerido=False
                )
                if nueva_categoria:
                    producto.categoria = nueva_categoria.strip().title()
                    self.marcar_cambios()

            elif opcion == 3:
                nuevo_precio = obtener_input_validado(
                    "Nuevo precio", "float", requerido=False
                )
                if nuevo_precio:
                    producto.precio = round(float(nuevo_precio), 2)
                    self.marcar_cambios()

            elif opcion == 4:
                print(f"Stock actual: {producto.stock}")
                print("1. Establecer stock específico")
                print("2. Sumar al stock actual")
                print("3. Restar del stock actual")

                tipo_actualizacion = obtener_opcion_menu(1, 3)

                if tipo_actualizacion == 1:
                    nuevo_stock = obtener_input_validado(
                        "Nuevo stock", "int", requerido=False
                    )
                    if nuevo_stock:
                        producto.stock = int(nuevo_stock)
                        self.marcar_cambios()

                elif tipo_actualizacion == 2:
                    cantidad = obtener_input_validado(
                        "Cantidad a sumar", "int", requerido=False
                    )
                    if cantidad:
                        producto.actualizar_stock(int(cantidad), "sumar")
                        self.marcar_cambios()

                elif tipo_actualizacion == 3:
                    cantidad = obtener_input_validado(
                        "Cantidad a restar", "int", requerido=False
                    )
                    if cantidad:
                        if producto.actualizar_stock(int(cantidad), "restar"):
                            self.marcar_cambios()
                        else:
                            print("❌ Stock insuficiente para realizar la operación")

            elif opcion == 5:
                nuevo_proveedor = obtener_input_validado(
                    "Nuevo proveedor", requerido=False
                )
                if nuevo_proveedor:
                    producto.proveedor = nuevo_proveedor.strip().title()
                    self.marcar_cambios()

            elif opcion == 6:
                # Actualizar todo
                datos_actuales = {
                    "nombre": producto.nombre,
                    "categoria": producto.categoria,
                    "precio": str(producto.precio),
                    "stock": str(producto.stock),
                    "proveedor": producto.proveedor,
                }

                print("\nIngresa los nuevos datos (Enter para mantener el actual):")

                for campo, valor_actual in datos_actuales.items():
                    nuevo_valor = input(
                        f"{campo.capitalize()} [{valor_actual}]: "
                    ).strip()
                    if nuevo_valor:
                        if campo == "nombre":
                            producto.nombre = nuevo_valor.title()
                        elif campo == "categoria":
                            producto.categoria = nuevo_valor.title()
                        elif campo == "precio":
                            try:
                                producto.precio = round(float(nuevo_valor), 2)
                            except ValueError:
                                print(f"❌ Precio inválido, manteniendo {valor_actual}")
                        elif campo == "stock":
                            try:
                                producto.stock = int(nuevo_valor)
                            except ValueError:
                                print(f"❌ Stock inválido, manteniendo {valor_actual}")
                        elif campo == "proveedor":
                            producto.proveedor = nuevo_valor.title()

                self.marcar_cambios()

            if self.cambios_sin_guardar:
                print(f"\n✅ Producto actualizado:")
                mostrar_tabla_productos([producto])

        except KeyboardInterrupt:
            print("\n🚫 Actualización cancelada")

        pausar()

    def eliminar_producto(self):
        """Elimina un producto del inventario"""
        limpiar_pantalla()
        mostrar_separador("🗑️ ELIMINAR PRODUCTO")

        if not self.productos:
            print("📭 No hay productos para eliminar")
            pausar()
            return

        try:
            product_id = obtener_input_validado("ID del producto a eliminar", "int")
            if not product_id:
                return

            producto = self.encontrar_producto_por_id(int(product_id))
            if not producto:
                print(f"❌ No se encontró producto con ID: {product_id}")
                pausar()
                return

            print(f"\n📦 Producto a eliminar:")
            mostrar_tabla_productos([producto])

            if confirmar_accion("¿Estás seguro de eliminar este producto?"):
                self.productos.remove(producto)
                self.marcar_cambios()
                print(f"✅ Producto eliminado: {producto.nombre}")
            else:
                print("🚫 Eliminación cancelada")

        except KeyboardInterrupt:
            print("\n🚫 Operación cancelada")

        pausar()

    def mostrar_reportes(self):
        """Muestra reportes y estadísticas"""
        limpiar_pantalla()
        mostrar_separador("📊 REPORTES Y ESTADÍSTICAS")

        if not self.productos:
            print("📭 No hay productos para generar reportes")
            pausar()
            return

        print("¿Qué reporte deseas ver?")
        print("1. Estadísticas generales")
        print("2. Productos con stock bajo")
        print("3. Productos por categoría")
        print("4. Exportar a CSV")

        try:
            opcion = obtener_opcion_menu(1, 4)

            if opcion == 1:
                limpiar_pantalla()
                mostrar_estadisticas(self.productos)

            elif opcion == 2:
                limite = obtener_input_validado(
                    "Límite de stock bajo (default: 10)", "int", False
                )
                limite = int(limite) if limite else 10

                productos_low_stock = productos_bajo_stock(self.productos, limite)
                limpiar_pantalla()

                if productos_low_stock:
                    mostrar_tabla_productos(
                        productos_low_stock, f"PRODUCTOS CON STOCK ≤ {limite}"
                    )
                else:
                    print(f"✅ No hay productos con stock por debajo de {limite}")

            elif opcion == 3:
                from productos import productos_por_categoria

                productos_por_cat = productos_por_categoria(self.productos)

                limpiar_pantalla()
                mostrar_separador("📋 PRODUCTOS POR CATEGORÍA")

                for categoria, productos_cat in productos_por_cat.items():
                    print(f"\n🏷️ {categoria} ({len(productos_cat)} productos):")
                    for producto in productos_cat:
                        print(
                            f"   • {producto.nombre} - ${producto.precio} (Stock: {producto.stock})"
                        )

            elif opcion == 4:
                if exportar_reporte_csv(self.productos):
                    print("✅ Reporte CSV generado exitosamente")
                else:
                    print("❌ Error al generar reporte CSV")

        except KeyboardInterrupt:
            print("\n🚫 Operación cancelada")

        pausar()

    def guardar_datos(self):
        """Guarda los datos del inventario"""
        if guardar_inventario(self.productos):
            self.cambios_sin_guardar = False
            print("✅ Datos guardados exitosamente")
        else:
            print("❌ Error al guardar los datos")
        pausar()

    def recargar_datos(self):
        """Recarga los datos desde el archivo"""
        if self.cambios_sin_guardar:
            if not confirmar_accion(
                "Hay cambios sin guardar. ¿Deseas recargar y perder los cambios?"
            ):
                return

        self.cargar_datos()
        print("🔄 Datos recargados desde archivo")
        pausar()

    def salir_sistema(self):
        """Maneja la salida del sistema"""
        if self.cambios_sin_guardar:
            print("⚠️ Hay cambios sin guardar")
            if confirmar_accion("¿Deseas guardar antes de salir?"):
                self.guardar_datos()

        print("\n👋 ¡Gracias por usar el Sistema de Inventario!")
        print("🚀 Continúa con tu journey de Data Engineering - Semana 2")
        return True

    def gestionar_categorias(self):
        """Gestiona las categorías del sistema"""
        limpiar_pantalla()
        mostrar_separador("🏷️ GESTIÓN DE CATEGORÍAS")

        print("¿Qué deseas hacer?")
        print("1. Ver estadísticas de categorías")
        print("2. Buscar categorías")
        print("3. Ver todas las categorías disponibles")
        print("4. Volver al menú principal")

        try:
            opcion = int(input("\nElige una opción (1-4): "))

            if opcion == 1:
                limpiar_pantalla()
                mostrar_estadisticas_categorias(self.gestor_categorias, self.productos)

            elif opcion == 2:
                termino = input("Término a buscar: ").strip()
                if termino:
                    resultados = self.gestor_categorias.buscar_categoria(termino)
                    if resultados:
                        print(f"\n🔍 Categorías encontradas para '{termino}':")
                        for cat in resultados:
                            print(f"   • {cat}")
                    else:
                        print(f"❌ No se encontraron categorías para '{termino}'")

            elif opcion == 3:
                from categorias import mostrar_menu_categorias

                mostrar_menu_categorias(self.gestor_categorias)

                # Opción para ver subcategorías
                while True:
                    try:
                        print(
                            "\nIngresa el número de categoría para ver subcategorías (0 para salir):"
                        )
                        num = int(input("Opción: "))
                        if num == 0:
                            break

                        categorias_principales = (
                            self.gestor_categorias.obtener_categorias_principales()
                        )
                        if 1 <= num <= len(categorias_principales):
                            from categorias import mostrar_subcategorias

                            categoria_sel = categorias_principales[num - 1]
                            mostrar_subcategorias(self.gestor_categorias, categoria_sel)
                        else:
                            print("❌ Opción inválida")
                    except ValueError:
                        print("❌ Por favor ingresa un número válido")

            elif opcion == 4:
                return
            else:
                print("❌ Opción inválida")

        except ValueError:
            print("❌ Por favor ingresa un número válido")

        pausar()

    def ver_historial(self):
        """Muestra opciones del historial de movimientos"""
        limpiar_pantalla()
        mostrar_separador("📜 HISTORIAL DE MOVIMIENTOS")

        print("¿Qué deseas ver?")
        print("1. Movimientos recientes (últimos 10)")
        print("2. Historial de un producto específico")
        print("3. Resumen de actividad (últimos 7 días)")
        print("4. Limpiar historial antiguo")
        print("5. Volver al menú principal")

        try:
            opcion = int(input("\nElige una opción (1-5): "))

            if opcion == 1:
                limpiar_pantalla()
                mostrar_movimientos_recientes(self.historial)

            elif opcion == 2:
                if not self.productos:
                    print("❌ No hay productos en el inventario")
                else:
                    print("\nProductos disponibles:")
                    for i, producto in enumerate(self.productos, 1):
                        print(f"{i}. {producto.nombre} (ID: {producto.id})")

                    try:
                        producto_id = int(input("\nIngresa el ID del producto: "))
                        producto = self.encontrar_producto_por_id(producto_id)

                        if producto:
                            mostrar_historial_producto(self.historial, producto_id)
                        else:
                            print(f"❌ Producto con ID {producto_id} no encontrado")
                    except ValueError:
                        print("❌ Por favor ingresa un ID válido")

            elif opcion == 3:
                limpiar_pantalla()
                dias = input("¿Cuántos días atrás? (por defecto 7): ").strip()
                try:
                    dias = int(dias) if dias else 7
                    mostrar_resumen_actividad(self.historial, dias)
                except ValueError:
                    print("❌ Número de días inválido, usando 7 días")
                    mostrar_resumen_actividad(self.historial, 7)

            elif opcion == 4:
                print("⚠️ Esta acción eliminará movimientos antiguos permanentemente")
                if confirmar_accion("¿Continuar?"):
                    dias = input(
                        "¿Eliminar movimientos más antiguos de cuántos días? (por defecto 90): "
                    ).strip()
                    try:
                        dias = int(dias) if dias else 90
                        eliminados = self.historial.limpiar_historial_antiguo(dias)
                        print(f"✅ Se eliminaron {eliminados} movimientos antiguos")
                    except ValueError:
                        print("❌ Número de días inválido")

            elif opcion == 5:
                return
            else:
                print("❌ Opción inválida")

        except ValueError:
            print("❌ Por favor ingresa un número válido")

        pausar()

    def importar_csv(self):
        """Gestiona la importación de productos desde CSV"""
        limpiar_pantalla()
        mostrar_separador("📥 IMPORTACIÓN DESDE CSV")

        productos_importados = proceso_importacion_interactivo(
            self.importador_csv, self.productos
        )

        if productos_importados:
            print(
                f"\n✅ Se importaron {len(productos_importados)} productos exitosamente"
            )

            # Agregar productos importados al inventario
            for producto in productos_importados:
                self.productos.append(producto)

            self.marcar_cambios()

            # Preguntar si guardar inmediatamente
            if confirmar_accion("¿Deseas guardar los cambios ahora?"):
                self.guardar_datos()

        pausar()

    def ejecutar(self):
        """Ejecuta el bucle principal del sistema"""
        while True:
            mostrar_menu_principal()

            # Mostrar indicador de cambios sin guardar
            if self.cambios_sin_guardar:
                print("⚠️  Hay cambios sin guardar")

            opcion = obtener_opcion_menu(1, 12)

            if opcion == 1:
                self.agregar_producto()
            elif opcion == 2:
                self.ver_todos_productos()
            elif opcion == 3:
                self.buscar_producto()
            elif opcion == 4:
                self.actualizar_producto()
            elif opcion == 5:
                self.eliminar_producto()
            elif opcion == 6:
                self.mostrar_reportes()
            elif opcion == 7:
                self.gestionar_categorias()
            elif opcion == 8:
                self.ver_historial()
            elif opcion == 9:
                self.importar_csv()
            elif opcion == 10:
                self.guardar_datos()
            elif opcion == 11:
                self.recargar_datos()
            elif opcion == 12:
                if self.salir_sistema():
                    break


def main():
    """Función principal"""
    try:
        sistema = SistemaInventario()
        sistema.ejecutar()
    except KeyboardInterrupt:
        print("\n\n🚫 Sistema interrumpido por el usuario")
        print("👋 ¡Hasta la próxima!")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("Por favor reporta este error para mejoras futuras")


if __name__ == "__main__":
    main()
