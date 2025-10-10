#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📜 Módulo de Historial - Sistema de Inventario
Proyecto del roadmap Data + Automation Engineer - Semana 2

Autor: Angel Baez
Fecha: Octubre 2025
Descripción: Sistema de logging y seguimiento de movimientos de inventario
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from productos import Product


class MovimientoInventario:
    """
    Clase para representar un movimiento en el inventario
    """

    def __init__(
        self,
        tipo: str,
        producto_id: int,
        producto_nombre: str,
        detalle: str,
        usuario: str = "Sistema",
        cantidad_anterior: Optional[int] = None,
        cantidad_nueva: Optional[int] = None,
    ):
        """
        Inicializa un movimiento de inventario

        Args:
            tipo: Tipo de movimiento ('CREATE', 'UPDATE', 'DELETE', 'STOCK_IN', 'STOCK_OUT')
            producto_id: ID del producto afectado
            producto_nombre: Nombre del producto
            detalle: Descripción detallada del movimiento
            usuario: Usuario que realizó la acción
            cantidad_anterior: Stock anterior (para movimientos de stock)
            cantidad_nueva: Stock nuevo (para movimientos de stock)
        """
        self.timestamp = datetime.now().isoformat()
        self.tipo = tipo
        self.producto_id = producto_id
        self.producto_nombre = producto_nombre
        self.detalle = detalle
        self.usuario = usuario
        self.cantidad_anterior = cantidad_anterior
        self.cantidad_nueva = cantidad_nueva

    def to_dict(self) -> Dict:
        """Convierte el movimiento a diccionario para JSON"""
        return {
            "timestamp": self.timestamp,
            "tipo": self.tipo,
            "producto_id": self.producto_id,
            "producto_nombre": self.producto_nombre,
            "detalle": self.detalle,
            "usuario": self.usuario,
            "cantidad_anterior": self.cantidad_anterior,
            "cantidad_nueva": self.cantidad_nueva,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "MovimientoInventario":
        """Crea un movimiento desde diccionario"""
        movimiento = cls(
            tipo=data["tipo"],
            producto_id=data["producto_id"],
            producto_nombre=data["producto_nombre"],
            detalle=data["detalle"],
            usuario=data.get("usuario", "Sistema"),
            cantidad_anterior=data.get("cantidad_anterior"),
            cantidad_nueva=data.get("cantidad_nueva"),
        )
        movimiento.timestamp = data["timestamp"]
        return movimiento

    def __str__(self) -> str:
        """Representación string del movimiento"""
        fecha = datetime.fromisoformat(self.timestamp).strftime("%Y-%m-%d %H:%M")
        if self.cantidad_anterior is not None and self.cantidad_nueva is not None:
            return f"[{fecha}] {self.tipo}: {self.producto_nombre} - {self.detalle} ({self.cantidad_anterior} → {self.cantidad_nueva})"
        return f"[{fecha}] {self.tipo}: {self.producto_nombre} - {self.detalle}"


class HistorialInventario:
    """
    Gestor del historial de movimientos del inventario
    """

    def __init__(self, archivo_historial: str = "historial_inventario.json"):
        """Inicializa el historial"""
        self.archivo_historial = archivo_historial
        self.movimientos: List[MovimientoInventario] = []
        self.cargar_historial()

    def cargar_historial(self):
        """Carga el historial desde archivo"""
        try:
            if os.path.exists(self.archivo_historial):
                with open(self.archivo_historial, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    self.movimientos = [
                        MovimientoInventario.from_dict(item) for item in datos
                    ]
        except Exception as e:
            print(f"❌ Error al cargar historial: {e}")
            self.movimientos = []

    def guardar_historial(self):
        """Guarda el historial en archivo"""
        try:
            with open(self.archivo_historial, "w", encoding="utf-8") as f:
                datos = [mov.to_dict() for mov in self.movimientos]
                json.dump(datos, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ Error al guardar historial: {e}")

    def registrar_movimiento(
        self,
        tipo: str,
        producto: Product,
        detalle: str,
        cantidad_anterior: Optional[int] = None,
        cantidad_nueva: Optional[int] = None,
        usuario: str = "Sistema",
    ):
        """
        Registra un nuevo movimiento en el historial

        Args:
            tipo: Tipo de movimiento
            producto: Producto afectado
            detalle: Descripción del movimiento
            cantidad_anterior: Stock anterior
            cantidad_nueva: Stock nuevo
            usuario: Usuario que realizó la acción
        """
        movimiento = MovimientoInventario(
            tipo=tipo,
            producto_id=producto.id,
            producto_nombre=producto.nombre,
            detalle=detalle,
            usuario=usuario,
            cantidad_anterior=cantidad_anterior,
            cantidad_nueva=cantidad_nueva,
        )

        self.movimientos.append(movimiento)
        self.guardar_historial()

    def obtener_historial_producto(
        self, producto_id: int, limite: Optional[int] = None
    ) -> List[MovimientoInventario]:
        """Obtiene el historial de un producto específico"""
        movimientos_producto = [
            mov for mov in self.movimientos if mov.producto_id == producto_id
        ]
        movimientos_producto.sort(key=lambda x: x.timestamp, reverse=True)

        if limite:
            return movimientos_producto[:limite]
        return movimientos_producto

    def obtener_movimientos_recientes(
        self, limite: int = 10
    ) -> List[MovimientoInventario]:
        """Obtiene los movimientos más recientes"""
        movimientos_ordenados = sorted(
            self.movimientos, key=lambda x: x.timestamp, reverse=True
        )
        return movimientos_ordenados[:limite]

    def obtener_movimientos_por_tipo(self, tipo: str) -> List[MovimientoInventario]:
        """Obtiene movimientos por tipo"""
        return [mov for mov in self.movimientos if mov.tipo == tipo]

    def obtener_resumen_movimientos(self, dias: int = 7) -> Dict:
        """Obtiene resumen de movimientos de los últimos N días"""
        fecha_limite = datetime.now().timestamp() - (dias * 24 * 3600)

        movimientos_recientes = [
            mov
            for mov in self.movimientos
            if datetime.fromisoformat(mov.timestamp).timestamp() > fecha_limite
        ]

        resumen = {
            "total_movimientos": len(movimientos_recientes),
            "productos_creados": len(
                [m for m in movimientos_recientes if m.tipo == "CREATE"]
            ),
            "productos_actualizados": len(
                [m for m in movimientos_recientes if m.tipo == "UPDATE"]
            ),
            "productos_eliminados": len(
                [m for m in movimientos_recientes if m.tipo == "DELETE"]
            ),
            "entradas_stock": len(
                [m for m in movimientos_recientes if m.tipo == "STOCK_IN"]
            ),
            "salidas_stock": len(
                [m for m in movimientos_recientes if m.tipo == "STOCK_OUT"]
            ),
        }

        return resumen

    def limpiar_historial_antiguo(self, dias: int = 90):
        """Limpia movimientos más antiguos de N días"""
        fecha_limite = datetime.now().timestamp() - (dias * 24 * 3600)

        movimientos_validos = [
            mov
            for mov in self.movimientos
            if datetime.fromisoformat(mov.timestamp).timestamp() > fecha_limite
        ]

        cantidad_eliminada = len(self.movimientos) - len(movimientos_validos)
        self.movimientos = movimientos_validos
        self.guardar_historial()

        return cantidad_eliminada


# Funciones de utilidad para integrar con el sistema existente


def mostrar_historial_producto(
    historial: HistorialInventario, producto_id: int, limite: int = 10
):
    """Muestra el historial de un producto específico"""
    movimientos = historial.obtener_historial_producto(producto_id, limite)

    if not movimientos:
        print(f"📜 No hay movimientos registrados para el producto ID: {producto_id}")
        return

    print(f"\n📜 HISTORIAL DEL PRODUCTO - ID: {producto_id}")
    print("=" * 80)

    for mov in movimientos:
        icono = {
            "CREATE": "✨",
            "UPDATE": "✏️",
            "DELETE": "🗑️",
            "STOCK_IN": "📈",
            "STOCK_OUT": "📉",
        }.get(mov.tipo, "📋")

        fecha = datetime.fromisoformat(mov.timestamp).strftime("%Y-%m-%d %H:%M")
        print(f"{icono} {fecha} | {mov.tipo:10} | {mov.detalle}")

        if mov.cantidad_anterior is not None and mov.cantidad_nueva is not None:
            cambio = mov.cantidad_nueva - mov.cantidad_anterior
            signo = "+" if cambio >= 0 else ""
            print(
                f"   └─ Stock: {mov.cantidad_anterior} → {mov.cantidad_nueva} ({signo}{cambio})"
            )

    print("=" * 80)


def mostrar_resumen_actividad(historial: HistorialInventario, dias: int = 7):
    """Muestra resumen de actividad reciente"""
    resumen = historial.obtener_resumen_movimientos(dias)

    print(f"\n📊 RESUMEN DE ACTIVIDAD - Últimos {dias} días")
    print("=" * 50)
    print(f"📋 Total de movimientos: {resumen['total_movimientos']}")
    print(f"✨ Productos creados: {resumen['productos_creados']}")
    print(f"✏️ Productos actualizados: {resumen['productos_actualizados']}")
    print(f"🗑️ Productos eliminados: {resumen['productos_eliminados']}")
    print(f"📈 Entradas de stock: {resumen['entradas_stock']}")
    print(f"📉 Salidas de stock: {resumen['salidas_stock']}")
    print("=" * 50)


def mostrar_movimientos_recientes(historial: HistorialInventario, limite: int = 10):
    """Muestra los movimientos más recientes"""
    movimientos = historial.obtener_movimientos_recientes(limite)

    if not movimientos:
        print("📜 No hay movimientos registrados")
        return

    print(f"\n📜 MOVIMIENTOS RECIENTES - Últimos {limite}")
    print("=" * 80)

    for mov in movimientos:
        icono = {
            "CREATE": "✨",
            "UPDATE": "✏️",
            "DELETE": "🗑️",
            "STOCK_IN": "📈",
            "STOCK_OUT": "📉",
        }.get(mov.tipo, "📋")

        fecha = datetime.fromisoformat(mov.timestamp).strftime("%m-%d %H:%M")
        print(
            f"{icono} {fecha} | {mov.tipo:10} | {mov.producto_nombre:20} | {mov.detalle}"
        )

    print("=" * 80)
