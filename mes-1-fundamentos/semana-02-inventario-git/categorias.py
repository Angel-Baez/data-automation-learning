#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏷️ Módulo de Categorías - Sistema de Inventario
Proyecto del roadmap Data + Automation Engineer - Semana 2

Autor: Angel Baez
Fecha: Octubre 2025
Descripción: Sistema de categorías predefinidas con sugerencias inteligentes
"""

from typing import List, Dict, Tuple
from difflib import get_close_matches


class GestorCategorias:
    """
    Gestor de categorías predefinidas con funcionalidades avanzadas
    """

    def __init__(self):
        """Inicializa el gestor con categorías predefinidas"""
        self.categorias_predefinidas = {
            # 🍕 Alimentos y Bebidas
            "Alimentos": [
                "Cereales",
                "Lácteos",
                "Carnes",
                "Pescados",
                "Frutas",
                "Verduras",
                "Legumbres",
                "Especias",
                "Conservas",
                "Congelados",
                "Panadería",
                "Repostería",
                "Snacks",
                "Dulces",
            ],
            "Bebidas": [
                "Refrescos",
                "Jugos",
                "Agua",
                "Café",
                "Té",
                "Bebidas Alcohólicas",
                "Bebidas Energéticas",
                "Smoothies",
                "Leches Vegetales",
            ],
            # 🏠 Hogar y Cuidado Personal
            "Hogar": [
                "Limpieza",
                "Cocina",
                "Baño",
                "Decoración",
                "Textiles",
                "Muebles",
                "Electrodomésticos Menores",
                "Jardinería",
                "Mascotas",
            ],
            "Cuidado Personal": [
                "Higiene",
                "Cosmética",
                "Perfumería",
                "Cuidado Capilar",
                "Cuidado Corporal",
                "Salud",
                "Farmacia",
            ],
            # 💻 Tecnología y Electrónicos
            "Tecnología": [
                "Computación",
                "Celulares",
                "Audio",
                "Video",
                "Gaming",
                "Accesorios Tech",
                "Componentes PC",
                "Software",
                "Gadgets",
            ],
            "Electrodomésticos": [
                "Cocina",
                "Lavandería",
                "Climatización",
                "Audio/Video",
                "Pequeños Electrodomésticos",
            ],
            # 👕 Ropa y Accesorios
            "Vestimenta": [
                "Ropa Hombre",
                "Ropa Mujer",
                "Ropa Infantil",
                "Calzado",
                "Accesorios",
                "Ropa Interior",
                "Ropa Deportiva",
                "Uniformes",
            ],
            # 🏃 Deportes y Recreación
            "Deportes": [
                "Fitness",
                "Deportes de Equipo",
                "Deportes Individuales",
                "Deportes Acuáticos",
                "Deportes de Montaña",
                "Ciclismo",
                "Equipamiento Deportivo",
            ],
            "Recreación": [
                "Juguetes",
                "Juegos de Mesa",
                "Libros",
                "Música",
                "Películas",
                "Coleccionables",
                "Artesanías",
            ],
            # 🏢 Oficina y Educación
            "Oficina": [
                "Papelería",
                "Suministros de Oficina",
                "Mobiliario de Oficina",
                "Equipos de Oficina",
                "Material de Archivo",
            ],
            "Educación": [
                "Libros de Texto",
                "Material Escolar",
                "Material Didáctico",
                "Instrumentos de Medición",
                "Arte y Manualidades",
            ],
            # 🚗 Automotriz y Herramientas
            "Automotriz": [
                "Repuestos",
                "Accesorios Auto",
                "Lubricantes",
                "Neumáticos",
                "Herramientas Auto",
                "Cuidado del Auto",
            ],
            "Herramientas": [
                "Herramientas Manuales",
                "Herramientas Eléctricas",
                "Ferretería",
                "Construcción",
                "Jardín y Exterior",
            ],
            # 🎨 Arte y Creatividad
            "Arte": [
                "Pintura",
                "Dibujo",
                "Escultura",
                "Manualidades",
                "Scrapbook",
                "Costura",
                "Tejido",
                "Cerámica",
            ],
            # 💼 Servicios y Otros
            "Servicios": [
                "Membresías",
                "Suscripciones",
                "Cursos",
                "Consultoría",
                "Mantenimiento",
                "Seguros",
            ],
            "Otros": ["Misceláneos", "Sin Categoría", "Temporales", "Promocionales"],
        }

    def obtener_todas_categorias(self) -> List[str]:
        """Obtiene lista plana de todas las categorías"""
        categorias = []
        for grupo, subcategorias in self.categorias_predefinidas.items():
            categorias.append(grupo)  # Categoría principal
            categorias.extend(subcategorias)  # Subcategorías
        return sorted(categorias)

    def obtener_categorias_principales(self) -> List[str]:
        """Obtiene solo las categorías principales"""
        return sorted(self.categorias_predefinidas.keys())

    def obtener_subcategorias(self, categoria_principal: str) -> List[str]:
        """Obtiene subcategorías de una categoría principal"""
        return self.categorias_predefinidas.get(categoria_principal, [])

    def buscar_categoria(self, termino: str) -> List[str]:
        """Busca categorías que contengan el término"""
        termino_lower = termino.lower()
        resultados = []

        for grupo, subcategorias in self.categorias_predefinidas.items():
            # Buscar en categoría principal
            if termino_lower in grupo.lower():
                resultados.append(grupo)

            # Buscar en subcategorías
            for subcat in subcategorias:
                if termino_lower in subcat.lower():
                    resultados.append(subcat)

        return sorted(list(set(resultados)))

    def sugerir_categoria(self, entrada: str, limite: int = 5) -> List[Tuple[str, int]]:
        """
        Sugiere categorías basadas en la entrada del usuario

        Args:
            entrada: Texto ingresado por el usuario
            limite: Número máximo de sugerencias

        Returns:
            Lista de tuplas (categoria, score_similitud)
        """
        todas_categorias = self.obtener_todas_categorias()

        # Buscar coincidencias exactas primero
        coincidencias_exactas = [
            cat for cat in todas_categorias if entrada.lower() in cat.lower()
        ]

        # Buscar coincidencias aproximadas
        coincidencias_aproximadas = get_close_matches(
            entrada, todas_categorias, n=limite, cutoff=0.4
        )

        # Combinar y ordenar resultados
        sugerencias = []

        # Agregar coincidencias exactas con mayor score
        for cat in coincidencias_exactas[:limite]:
            score = 100 if entrada.lower() == cat.lower() else 90
            sugerencias.append((cat, score))

        # Agregar coincidencias aproximadas
        for cat in coincidencias_aproximadas:
            if not any(s[0] == cat for s in sugerencias):  # Evitar duplicados
                # Calcular score basado en similitud
                ratio = len(entrada) / len(cat) if len(cat) > 0 else 0
                score = int(60 + (ratio * 30))  # Score entre 60-90
                sugerencias.append((cat, min(score, 89)))

        # Ordenar por score descendente y retornar
        sugerencias.sort(key=lambda x: x[1], reverse=True)
        return sugerencias[:limite]

    def validar_categoria(self, categoria: str) -> Tuple[bool, str, List[str]]:
        """
        Valida si una categoría existe o sugiere alternativas

        Returns:
            Tupla (es_valida, mensaje, sugerencias)
        """
        todas_categorias = self.obtener_todas_categorias()

        # Verificar si existe exactamente
        if categoria in todas_categorias:
            return True, "Categoría válida", []

        # Verificar coincidencia case-insensitive
        for cat in todas_categorias:
            if categoria.lower() == cat.lower():
                return True, f"Categoría corregida a: '{cat}'", [cat]

        # Buscar sugerencias
        sugerencias = self.sugerir_categoria(categoria, 3)
        if sugerencias:
            sugerencias_texto = [s[0] for s in sugerencias]
            return (
                False,
                f"Categoría no encontrada. ¿Quizás quisiste decir?",
                sugerencias_texto,
            )

        return False, "Categoría no encontrada y sin sugerencias", []

    def agregar_categoria_personalizada(
        self, categoria: str, grupo: str = "Otros"
    ) -> bool:
        """
        Agrega una categoría personalizada a un grupo

        Args:
            categoria: Nueva categoría a agregar
            grupo: Grupo donde agregar la categoría

        Returns:
            bool: True si se agregó exitosamente
        """
        if grupo not in self.categorias_predefinidas:
            self.categorias_predefinidas[grupo] = []

        if categoria not in self.categorias_predefinidas[grupo]:
            self.categorias_predefinidas[grupo].append(categoria)
            self.categorias_predefinidas[grupo].sort()
            return True

        return False  # Ya existe

    def obtener_estadisticas_categorias(self, productos) -> Dict:
        """
        Obtiene estadísticas de uso de categorías

        Args:
            productos: Lista de productos del inventario

        Returns:
            Diccionario con estadísticas
        """
        from collections import Counter

        # Contar uso de categorías
        categorias_usadas = [p.categoria for p in productos]
        contador = Counter(categorias_usadas)

        # Calcular estadísticas
        total_productos = len(productos)
        categorias_unicas = len(contador)

        # Categorías más usadas
        mas_usadas = contador.most_common(5)

        # Categorías sin usar
        todas_categorias = set(self.obtener_todas_categorias())
        usadas = set(categorias_usadas)
        sin_usar = todas_categorias - usadas

        return {
            "total_productos": total_productos,
            "categorias_unicas": categorias_unicas,
            "categorias_disponibles": len(todas_categorias),
            "mas_usadas": mas_usadas,
            "sin_usar": sorted(list(sin_usar)),
            "cobertura_porcentaje": round(
                (categorias_unicas / len(todas_categorias)) * 100, 2
            ),
        }


# Funciones de utilidad para integrar con el sistema existente


def mostrar_menu_categorias(gestor: GestorCategorias):
    """Muestra menú interactivo de categorías"""
    print("\n🏷️ CATEGORÍAS DISPONIBLES")
    print("=" * 50)

    categorias_principales = gestor.obtener_categorias_principales()

    for i, categoria in enumerate(categorias_principales, 1):
        subcategorias = gestor.obtener_subcategorias(categoria)
        print(f"{i:2}. {categoria} ({len(subcategorias)} subcategorías)")

    print("=" * 50)
    return categorias_principales


def mostrar_subcategorias(gestor: GestorCategorias, categoria_principal: str):
    """Muestra las subcategorías de una categoría principal"""
    subcategorias = gestor.obtener_subcategorias(categoria_principal)

    if not subcategorias:
        print(f"No hay subcategorías para '{categoria_principal}'")
        return

    print(f"\n🏷️ SUBCATEGORÍAS DE '{categoria_principal.upper()}'")
    print("=" * 60)

    # Mostrar en columnas
    columnas = 3
    filas = len(subcategorias) // columnas + (1 if len(subcategorias) % columnas else 0)

    for fila in range(filas):
        linea = ""
        for col in range(columnas):
            indice = fila + col * filas
            if indice < len(subcategorias):
                linea += f"{subcategorias[indice]:<20}"
        print(linea)

    print("=" * 60)


def obtener_categoria_con_sugerencias(
    gestor: GestorCategorias, prompt: str = "Categoría"
) -> str:
    """
    Obtiene una categoría del usuario con sugerencias inteligentes

    Args:
        gestor: Instancia del gestor de categorías
        prompt: Texto del prompt para el usuario

    Returns:
        str: Categoría validada seleccionada por el usuario
    """
    while True:
        print(f"\n💡 Escribe una categoría o 'ver' para ver todas las opciones")
        entrada = input(f"{prompt}: ").strip()

        if not entrada:
            print("❌ Por favor ingresa una categoría")
            continue

        if entrada.lower() == "ver":
            mostrar_menu_categorias(gestor)
            continue

        # Validar y sugerir
        es_valida, mensaje, sugerencias = gestor.validar_categoria(entrada)

        if es_valida:
            if sugerencias:  # Corrección de case
                return sugerencias[0]
            return entrada

        print(f"❌ {mensaje}")

        if sugerencias:
            print("💡 Sugerencias:")
            for i, sugerencia in enumerate(sugerencias, 1):
                print(f"   {i}. {sugerencia}")

            print("   0. Usar categoría original")

            try:
                opcion = int(
                    input("Elige una opción (0-{}): ".format(len(sugerencias)))
                )
                if 0 <= opcion <= len(sugerencias):
                    if opcion == 0:
                        return entrada
                    else:
                        return sugerencias[opcion - 1]
                else:
                    print("❌ Opción inválida")
            except ValueError:
                print("❌ Por favor ingresa un número válido")


def mostrar_estadisticas_categorias(gestor: GestorCategorias, productos):
    """Muestra estadísticas de uso de categorías"""
    stats = gestor.obtener_estadisticas_categorias(productos)

    print(f"\n📊 ESTADÍSTICAS DE CATEGORÍAS")
    print("=" * 50)
    print(f"📦 Total de productos: {stats['total_productos']}")
    print(f"🏷️ Categorías en uso: {stats['categorias_unicas']}")
    print(f"📋 Categorías disponibles: {stats['categorias_disponibles']}")
    print(f"📈 Cobertura: {stats['cobertura_porcentaje']}%")

    if stats["mas_usadas"]:
        print(f"\n🔥 CATEGORÍAS MÁS USADAS:")
        for categoria, cantidad in stats["mas_usadas"]:
            print(f"   • {categoria}: {cantidad} productos")

    if len(stats["sin_usar"]) <= 10:  # Solo mostrar si no son muchas
        print(f"\n💤 CATEGORÍAS SIN USAR:")
        for categoria in stats["sin_usar"][:10]:
            print(f"   • {categoria}")
        if len(stats["sin_usar"]) > 10:
            print(f"   ... y {len(stats['sin_usar']) - 10} más")

    print("=" * 50)
