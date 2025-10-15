"""
📊 CSV Processor - Semana 3
Sistema modular de procesamiento de archivos CSV con variables de entorno

Este paquete proporciona un sistema completo para procesar archivos CSV
con configuración externa, validación de datos y logging estructurado.

Módulos:
    - main: Punto de entrada principal de la aplicación
    - csv_processor: Lógica core de procesamiento de CSV
    - data_validator: Validación de esquemas y calidad de datos
    - config_manager: Gestión de configuración y variables de entorno
    - utils: Utilidades y funciones auxiliares

Autor: Angel Baez
Fecha: Octubre 2025
Proyecto: Data + Automation Engineer Journey - Semana 3
"""

__version__ = "1.0.0"
__author__ = "Angel Baez"
__email__ = "angel@example.com"

# Importaciones principales del paquete
from .config_manager import ConfigManager
from .csv_processor import CSVProcessor
from .data_validator import DataValidator

__all__ = ["ConfigManager", "CSVProcessor", "DataValidator"]
