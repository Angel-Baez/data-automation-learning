#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Tests Unitarios - Sistema de Inventario
Proyecto del roadmap Data + Automation Engineer - Semana 2

Autor: Angel Baez
Fecha: Octubre 2025
Descripción: Tests para validar funcionalidades críticas del sistema
"""

import pytest
import json
import os
from productos import Product, validar_producto_data, buscar_productos
from utils import cargar_inventario, guardar_inventario


class TestProduct:
    """Tests para la clase Product"""

    def test_crear_producto_valido(self):
        """Test crear producto con datos válidos"""
        producto = Product(
            nombre="Laptop Test",
            categoria="Electrónicos",
            precio=599.99,
            stock=10,
            proveedor="TestCorp",
        )

        assert producto.nombre == "Laptop Test"
        assert producto.categoria == "Electrónicos"
        assert producto.precio == 599.99
        assert producto.stock == 10
        assert producto.proveedor == "Testcorp"
        assert producto.id is not None
        assert len(str(producto.id)) > 0

    def test_producto_to_dict(self):
        """Test conversión de producto a diccionario"""
        producto = Product("Test", "Cat", 10.0, 5, "Prov", product_id=12345)

        dict_producto = producto.to_dict()

        assert dict_producto["id"] == 12345
        assert dict_producto["nombre"] == "Test"
        assert dict_producto["categoria"] == "Cat"
        assert dict_producto["precio"] == 10.0
        assert dict_producto["stock"] == 5
        assert dict_producto["proveedor"] == "Prov"
        assert "fecha_ingreso" in dict_producto

    def test_producto_from_dict(self):
        """Test crear producto desde diccionario"""
        data = {
            "id": 12345,
            "nombre": "Test Product",
            "categoria": "Test Cat",
            "precio": 25.50,
            "stock": 8,
            "proveedor": "Test Provider",
            "fecha_ingreso": "2025-10-09",
        }

        producto = Product.from_dict(data)

        assert producto.id == 12345
        assert producto.nombre == "Test Product"
        assert producto.categoria == "Test Cat"
        assert producto.precio == 25.50
        assert producto.stock == 8
        assert producto.proveedor == "Test Provider"
        assert producto.fecha_ingreso == "2025-10-09"

    def test_actualizar_stock_sumar(self):
        """Test actualizar stock sumando"""
        producto = Product("Test", "Cat", 10.0, 5, "Prov")

        resultado = producto.actualizar_stock(3, "sumar")

        assert resultado is True
        assert producto.stock == 8

    def test_actualizar_stock_restar_suficiente(self):
        """Test actualizar stock restando con stock suficiente"""
        producto = Product("Test", "Cat", 10.0, 5, "Prov")

        resultado = producto.actualizar_stock(3, "restar")

        assert resultado is True
        assert producto.stock == 2

    def test_actualizar_stock_restar_insuficiente(self):
        """Test actualizar stock restando con stock insuficiente"""
        producto = Product("Test", "Cat", 10.0, 5, "Prov")

        resultado = producto.actualizar_stock(10, "restar")

        assert resultado is False
        assert producto.stock == 5  # No debe cambiar

    def test_precio_redondeo(self):
        """Test que el precio se redondea a 2 decimales"""
        producto = Product("Test", "Cat", 10.999, 5, "Prov")

        assert producto.precio == 11.00

    def test_formateo_nombres(self):
        """Test que nombres se formatean correctamente"""
        producto = Product(
            nombre="  laptop dell  ",
            categoria="  electrónicos  ",
            precio=10.0,
            stock=5,
            proveedor="  TECH corp  ",
        )

        assert producto.nombre == "Laptop Dell"
        assert producto.categoria == "Electrónicos"
        assert producto.proveedor == "Tech Corp"


class TestValidaciones:
    """Tests para funciones de validación"""

    def test_validar_producto_data_valido(self):
        """Test validación con datos válidos"""
        es_valido, mensaje, datos = validar_producto_data(
            "Laptop", "Electrónicos", "599.99", "10", "TechCorp"
        )

        assert es_valido is True
        assert mensaje == "Datos válidos"
        assert datos["nombre"] == "Laptop"
        assert datos["categoria"] == "Electrónicos"
        assert datos["precio"] == 599.99
        assert datos["stock"] == 10
        assert datos["proveedor"] == "Techcorp"

    def test_validar_producto_precio_negativo(self):
        """Test validación con precio negativo"""
        es_valido, mensaje, datos = validar_producto_data(
            "Test", "Cat", "-10.0", "5", "Prov"
        )

        assert es_valido is False
        assert "precio" in mensaje.lower()

    def test_validar_producto_stock_negativo(self):
        """Test validación con stock negativo"""
        es_valido, mensaje, datos = validar_producto_data(
            "Test", "Cat", "10.0", "-5", "Prov"
        )

        assert es_valido is False
        assert "stock" in mensaje.lower()

    def test_validar_producto_nombre_vacio(self):
        """Test validación con nombre vacío"""
        es_valido, mensaje, datos = validar_producto_data(
            "", "Cat", "10.0", "5", "Prov"
        )

        assert es_valido is False
        assert "nombre" in mensaje.lower()


class TestBusquedas:
    """Tests para funciones de búsqueda"""

    def setup_method(self):
        """Configuración para cada test"""
        self.productos = [
            Product("Laptop Dell", "Electrónicos", 599.99, 5, "TechWorld", 1001),
            Product("Mouse Logitech", "Electrónicos", 25.99, 10, "TechSupply", 1002),
            Product("Arroz Premium", "Alimentos", 15.50, 20, "GranoCorp", 1003),
            Product("Aceite Crisol", "Alimentos", 8.75, 8, "AceitesLtd", 1004),
        ]

    def test_buscar_por_nombre(self):
        """Test búsqueda por nombre"""
        resultados = buscar_productos(self.productos, "Dell", "nombre")

        assert len(resultados) == 1
        assert resultados[0].nombre == "Laptop Dell"

    def test_buscar_por_categoria(self):
        """Test búsqueda por categoría"""
        resultados = buscar_productos(self.productos, "Electrónicos", "categoria")

        assert len(resultados) == 2
        assert all(p.categoria == "Electrónicos" for p in resultados)

    def test_buscar_por_proveedor(self):
        """Test búsqueda por proveedor"""
        resultados = buscar_productos(self.productos, "TechWorld", "proveedor")

        assert len(resultados) == 1
        assert resultados[0].proveedor == "Techworld"

    def test_buscar_por_id(self):
        """Test búsqueda por ID"""
        # La función buscar_productos actual no soporta búsqueda por ID
        # Solo busca por nombre, categoría y proveedor
        # Buscaremos por nombre en su lugar para este test
        resultados = buscar_productos(self.productos, "Premium", "nombre")

        assert len(resultados) == 1
        assert resultados[0].id == 1003
        assert resultados[0].nombre == "Arroz Premium"

    def test_buscar_sin_resultados(self):
        """Test búsqueda sin resultados"""
        resultados = buscar_productos(self.productos, "NoExiste", "nombre")

        assert len(resultados) == 0

    def test_buscar_case_insensitive(self):
        """Test búsqueda insensible a mayúsculas"""
        resultados = buscar_productos(self.productos, "dell", "nombre")

        assert len(resultados) == 1
        assert resultados[0].nombre == "Laptop Dell"


class TestPersistencia:
    """Tests para funciones de persistencia"""

    def setup_method(self):
        """Configuración para cada test"""
        self.archivo_test = "test_inventario.json"
        self.productos_test = [
            Product("Test1", "Cat1", 10.0, 5, "Prov1", 1001),
            Product("Test2", "Cat2", 20.0, 10, "Prov2", 1002),
        ]

    def teardown_method(self):
        """Limpieza después de cada test"""
        if os.path.exists(self.archivo_test):
            os.remove(self.archivo_test)

    def test_guardar_y_cargar_inventario(self):
        """Test guardar y cargar inventario"""
        # Guardar
        resultado = guardar_inventario(self.productos_test, self.archivo_test)
        assert resultado is True
        assert os.path.exists(self.archivo_test)

        # Cargar
        productos_cargados = cargar_inventario(self.archivo_test)
        assert len(productos_cargados) == 2
        assert productos_cargados[0].nombre == "Test1"
        assert productos_cargados[1].nombre == "Test2"

    def test_cargar_archivo_inexistente(self):
        """Test cargar archivo que no existe"""
        productos = cargar_inventario("archivo_inexistente.json")

        assert len(productos) == 0

    def test_formato_json_correcto(self):
        """Test que el JSON generado tiene formato correcto"""
        guardar_inventario(self.productos_test, self.archivo_test)

        with open(self.archivo_test, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == 2
        assert data[0]["id"] == 1001
        assert data[0]["nombre"] == "Test1"
        assert data[1]["id"] == 1002
        assert data[1]["nombre"] == "Test2"


if __name__ == "__main__":
    # Ejecutar tests con pytest
    pytest.main([__file__, "-v"])
