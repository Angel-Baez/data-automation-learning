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


class SistemaInventario:
    """
    Clase principal del sistema de inventario
    """

    def __init__(self):
        """Inicializa el sistema de inventario"""
        self.productos: List[Product] = []
        self.cambios_sin_guardar = False
        print("🚀 Iniciando Sistema de Inventario...")
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

            categoria = obtener_input_validado("Categoría")
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

    def ejecutar(self):
        """Ejecuta el bucle principal del sistema"""
        while True:
            mostrar_menu_principal()

            # Mostrar indicador de cambios sin guardar
            if self.cambios_sin_guardar:
                print("⚠️  Hay cambios sin guardar")

            opcion = obtener_opcion_menu(1, 9)

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
                self.guardar_datos()
            elif opcion == 8:
                self.recargar_datos()
            elif opcion == 9:
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
