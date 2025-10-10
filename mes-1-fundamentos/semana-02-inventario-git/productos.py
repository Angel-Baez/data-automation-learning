#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📦 Módulo de Productos - Sistema de Inventario
Proyecto del roadmap Data + Automation Engineer - Semana 2

Autor: Angel Baez
Fecha: Octubre 2025
Descripción: Clase Product y funciones de validación para el sistema de inventario
"""

from datetime import datetime
from typing import Dict, List, Optional


class Product:
    """
    Clase que representa un producto en el inventario

    Attributes:
        id (int): Identificador único del producto
        nombre (str): Nombre del producto
        categoria (str): Categoría del producto
        precio (float): Precio unitario
        stock (int): Cantidad en inventario
        fecha_ingreso (str): Fecha de ingreso al inventario
        proveedor (str): Proveedor del producto
    """

    def __init__(
        self,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int,
        proveedor: str,
        product_id: Optional[int] = None,
    ):
        """
        Inicializa un nuevo producto

        Args:
            nombre: Nombre del producto
            categoria: Categoría del producto
            precio: Precio unitario
            stock: Cantidad inicial
            proveedor: Proveedor del producto
            product_id: ID del producto (opcional, se genera automáticamente)
        """
        self.id = product_id if product_id else self._generate_id()
        self.nombre = nombre.strip().title()
        self.categoria = categoria.strip().title()
        self.precio = round(float(precio), 2)
        self.stock = int(stock)
        self.fecha_ingreso = datetime.now().strftime("%Y-%m-%d")
        self.proveedor = proveedor.strip().title()

    def _generate_id(self) -> int:
        """Genera un ID único basado en timestamp"""
        return int(datetime.now().timestamp() * 1000) % 1000000

    def to_dict(self) -> Dict:
        """Convierte el producto a diccionario para JSON"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock,
            "fecha_ingreso": self.fecha_ingreso,
            "proveedor": self.proveedor,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Product":
        """Crea un producto desde un diccionario"""
        product = cls(
            nombre=data["nombre"],
            categoria=data["categoria"],
            precio=data["precio"],
            stock=data["stock"],
            proveedor=data["proveedor"],
            product_id=data["id"],
        )
        product.fecha_ingreso = data["fecha_ingreso"]
        return product

    def actualizar_stock(self, cantidad: int, operacion: str = "sumar") -> bool:
        """
        Actualiza el stock del producto

        Args:
            cantidad: Cantidad a sumar o restar
            operacion: 'sumar' o 'restar'

        Returns:
            bool: True si la operación fue exitosa
        """
        if operacion == "sumar":
            self.stock += cantidad
            return True
        elif operacion == "restar":
            if self.stock >= cantidad:
                self.stock -= cantidad
                return True
            else:
                return False
        return False

    def __str__(self) -> str:
        """Representación en string del producto"""
        return f"[{self.id}] {self.nombre} - ${self.precio} (Stock: {self.stock})"

    def __repr__(self) -> str:
        """Representación técnica del producto"""
        return f"Product(id={self.id}, nombre='{self.nombre}', stock={self.stock})"


def validar_producto_data(
    nombre: str, categoria: str, precio: str, stock: str, proveedor: str
) -> tuple[bool, str, Dict]:
    """
    Valida los datos de entrada para crear/actualizar un producto

    Args:
        nombre: Nombre del producto
        categoria: Categoría del producto
        precio: Precio como string
        stock: Stock como string
        proveedor: Proveedor del producto

    Returns:
        tuple: (es_valido, mensaje_error, datos_limpiados)
    """
    errores = []
    datos_limpiados = {}

    # Validar nombre
    if not nombre or len(nombre.strip()) < 2:
        errores.append("El nombre debe tener al menos 2 caracteres")
    else:
        datos_limpiados["nombre"] = nombre.strip().title()

    # Validar categoría
    if not categoria or len(categoria.strip()) < 2:
        errores.append("La categoría debe tener al menos 2 caracteres")
    else:
        datos_limpiados["categoria"] = categoria.strip().title()

    # Validar precio
    try:
        precio_float = float(precio)
        if precio_float < 0:
            errores.append("El precio no puede ser negativo")
        else:
            datos_limpiados["precio"] = round(precio_float, 2)
    except ValueError:
        errores.append("El precio debe ser un número válido")

    # Validar stock
    try:
        stock_int = int(stock)
        if stock_int < 0:
            errores.append("El stock no puede ser negativo")
        else:
            datos_limpiados["stock"] = stock_int
    except ValueError:
        errores.append("El stock debe ser un número entero válido")

    # Validar proveedor
    if not proveedor or len(proveedor.strip()) < 2:
        errores.append("El proveedor debe tener al menos 2 caracteres")
    else:
        datos_limpiados["proveedor"] = proveedor.strip().title()

    if errores:
        return False, "; ".join(errores), {}

    return True, "Datos válidos", datos_limpiados


def categorias_disponibles(productos: List[Product]) -> set:
    """
    Obtiene todas las categorías únicas de los productos

    Args:
        productos: Lista de productos

    Returns:
        set: Conjunto de categorías únicas
    """
    return {producto.categoria for producto in productos}


def productos_por_categoria(productos: List[Product]) -> Dict[str, List[Product]]:
    """
    Agrupa productos por categoría

    Args:
        productos: Lista de productos

    Returns:
        Dict: Diccionario con categorías como keys y listas de productos como values
    """
    resultado = {}
    for producto in productos:
        if producto.categoria not in resultado:
            resultado[producto.categoria] = []
        resultado[producto.categoria].append(producto)
    return resultado


def buscar_productos(
    productos: List[Product], termino: str, campo: str = "nombre"
) -> List[Product]:
    """
    Busca productos por diferentes campos

    Args:
        productos: Lista de productos
        termino: Término de búsqueda
        campo: Campo a buscar ('nombre', 'categoria', 'proveedor')

    Returns:
        List: Lista de productos que coinciden
    """
    termino = termino.lower().strip()
    resultados = []

    for producto in productos:
        valor_campo = ""
        if campo == "nombre":
            valor_campo = producto.nombre.lower()
        elif campo == "categoria":
            valor_campo = producto.categoria.lower()
        elif campo == "proveedor":
            valor_campo = producto.proveedor.lower()

        if termino in valor_campo:
            resultados.append(producto)

    return resultados


def productos_bajo_stock(productos: List[Product], limite: int = 10) -> List[Product]:
    """
    Encuentra productos con stock bajo

    Args:
        productos: Lista de productos
        limite: Límite de stock bajo (default: 10)

    Returns:
        List: Productos con stock por debajo del límite
    """
    return [producto for producto in productos if producto.stock <= limite]


def valor_total_inventario(productos: List[Product]) -> float:
    """
    Calcula el valor total del inventario

    Args:
        productos: Lista de productos

    Returns:
        float: Valor total (precio * stock) de todos los productos
    """
    return sum(producto.precio * producto.stock for producto in productos)


def producto_mas_caro(productos: List[Product]) -> Optional[Product]:
    """
    Encuentra el producto más caro

    Args:
        productos: Lista de productos

    Returns:
        Product: Producto con el precio más alto, None si lista vacía
    """
    if not productos:
        return None
    return max(productos, key=lambda p: p.precio)


def producto_mas_stock(productos: List[Product]) -> Optional[Product]:
    """
    Encuentra el producto con más stock

    Args:
        productos: Lista de productos

    Returns:
        Product: Producto con el stock más alto, None si lista vacía
    """
    if not productos:
        return None
    return max(productos, key=lambda p: p.stock)
