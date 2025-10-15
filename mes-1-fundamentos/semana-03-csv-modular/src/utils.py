#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛠️ Módulo de Utilidades - Sistema    formatter = logging.Formatter(log_format, date_format)

    # Manejador de consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Manejador de archivo para logs generalessamiento CSV

Este módulo proporciona funciones utilitarias comunes incluyendo:
- Configuración de logging y registro
- Operaciones de archivos y gestión de rutas
- Conversiones de tipos de datos
- Monitoreo de rendimiento
- Utilidades de manejo de errores
- Helpers de procesamiento de strings y texto

Autor: Angel Baez
Fecha: Octubre 2025
Proyecto: Data + Automation Engineer Journey - Semana 3
Versión: 1.0.0
"""

import logging
import logging.config
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Union, List
import json
import time
from functools import wraps
from datetime import datetime
import pandas as pd
import numpy as np
import re
from contextlib import contextmanager


def setup_logging(
    config_path: Optional[str] = None,
    log_level: str = "INFO",
    log_dir: Optional[str] = None,
) -> logging.Logger:
    """
    Configura el sistema de logging con manejadores de archivo y consola

    Args:
        config_path: Ruta al archivo de configuración de logging
        log_level: Nivel de logging por defecto
        log_dir: Directorio para archivos de log

    Returns:
        Instancia de logger configurada
    """
    # Crear directorio de logs si se especifica
    if log_dir:
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
    else:
        log_path = Path("logs")
        log_path.mkdir(parents=True, exist_ok=True)

    # Intentar cargar archivo de configuración primero
    if config_path and Path(config_path).exists():
        try:
            with open(config_path, "r") as f:
                if config_path.endswith(".json"):
                    config = json.load(f)
                    logging.config.dictConfig(config)
                else:
                    # Asumir que es un archivo .conf
                    logging.config.fileConfig(config_path)

            logger = logging.getLogger(__name__)
            logger.info(
                f"Configuración de logging cargada desde archivo: {config_path}"
            )
            return logger

        except Exception as e:
            print(
                f"Advertencia: No se pudo cargar configuración de logging desde {config_path}: {e}"
            )
            print("Recurriendo a configuración por defecto")

    # Configuración de logging por defecto
    log_format = (
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
    )
    date_format = "%Y-%m-%d %H:%M:%S"

    # Configurar logger raíz
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Limpiar manejadores existentes
    logger.handlers.clear()

    # Crear formateadores
    formatter = logging.Formatter(log_format, date_format)

    # Manejador de consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Manejador de archivo para logs generales
    log_file = log_path / f"csv_processor_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Manejador de archivo de errores
    error_log_file = log_path / f"errors_{datetime.now().strftime('%Y%m%d')}.log"
    error_handler = logging.FileHandler(error_log_file, encoding="utf-8")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)

    # Obtener logger del módulo
    module_logger = logging.getLogger(__name__)
    module_logger.info("Configuración de logging por defecto establecida")

    return module_logger


def ensure_directory(path: Union[str, Path]) -> Path:
    """
    Asegurar que el directorio existe, crear si es necesario

    Args:
        path: Ruta del directorio

    Returns:
        Objeto Path
    """
    path_obj = Path(path)
    path_obj.mkdir(parents=True, exist_ok=True)
    return path_obj


def safe_file_operation(operation_name: str = "operacion_archivo"):
    """
    Decorador para operaciones de archivo seguras con manejo de errores

    Args:
        operation_name: Nombre de la operación para logging
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(__name__)
            try:
                logger.debug(f"Iniciando {operation_name}")
                result = func(*args, **kwargs)
                logger.debug(f"Completado exitosamente {operation_name}")
                return result
            except FileNotFoundError as e:
                logger.error(f"Archivo no encontrado durante {operation_name}: {e}")
                raise
            except PermissionError as e:
                logger.error(f"Permisos denegados durante {operation_name}: {e}")
                raise
            except Exception as e:
                logger.error(f"Error inesperado durante {operation_name}: {e}")
                raise

        return wrapper

    return decorator


def performance_monitor(func):
    """
    Decorador para monitorear el rendimiento de funciones
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(__name__)
        start_time = time.time()

        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(
                f"Función {func.__name__} ejecutada en {execution_time:.4f} segundos"
            )
            return result

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(
                f"Función {func.__name__} falló después de {execution_time:.4f} segundos: {e}"
            )
            raise

    return wrapper


@contextmanager
def timing_context(operation_name: str):
    """
    Gestor de contexto para cronometrar operaciones

    Args:
        operation_name: Nombre de la operación que se cronometra
    """
    logger = logging.getLogger(__name__)
    start_time = time.time()
    logger.debug(f"Iniciando {operation_name}")

    try:
        yield
    finally:
        execution_time = time.time() - start_time
        logger.info(f"{operation_name} completado en {execution_time:.4f} segundos")


def get_file_size_mb(file_path: Union[str, Path]) -> float:
    """
    Obtener el tamaño del archivo en megabytes

    Args:
        file_path: Ruta al archivo

    Returns:
        Tamaño del archivo en MB
    """
    path = Path(file_path)
    if path.exists():
        return path.stat().st_size / (1024 * 1024)
    return 0.0


def clean_column_name(name: str) -> str:
    """
    Limpiar y estandarizar nombres de columnas

    Args:
        name: Nombre original de la columna

    Returns:
        Nombre de columna limpio
    """
    # Convertir a minúsculas
    clean_name = str(name).lower().strip()

    # Reemplazar espacios y caracteres especiales con guiones bajos
    clean_name = re.sub(r"[^\w\s]", "_", clean_name)
    clean_name = re.sub(r"\s+", "_", clean_name)

    # Remover múltiples guiones bajos consecutivos
    clean_name = re.sub(r"_+", "_", clean_name)

    # Remover guiones bajos al inicio y final
    clean_name = clean_name.strip("_")

    # Asegurar que no comience con un número
    if clean_name and clean_name[0].isdigit():
        clean_name = f"col_{clean_name}"

    # Manejar nombres vacíos
    if not clean_name:
        clean_name = "columna_sin_nombre"

    return clean_name


def detect_delimiter(file_path: Union[str, Path], sample_size: int = 1024) -> str:
    """
    Detectar delimitador CSV desde una muestra del archivo

    Args:
        file_path: Ruta al archivo CSV
        sample_size: Número de caracteres a muestrear

    Returns:
        Carácter delimitador detectado
    """
    import csv

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {file_path}")

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        sample = f.read(sample_size)

    try:
        # Usar csv.Sniffer para detectar delimitador
        sniffer = csv.Sniffer()
        delimiter = sniffer.sniff(sample).delimiter
        return delimiter
    except Exception:
        # Respaldo a detección manual
        delimiters = [",", ";", "\t", "|"]
        delimiter_counts = {}

        for delimiter in delimiters:
            delimiter_counts[delimiter] = sample.count(delimiter)

        # Retornar delimitador con mayor conteo
        if delimiter_counts:
            best_delimiter = max(delimiter_counts, key=lambda x: delimiter_counts[x])
            return best_delimiter if delimiter_counts[best_delimiter] > 0 else ","
        return ","


def detect_encoding(file_path: Union[str, Path], sample_size: int = 10240) -> str:
    """
    Detectar codificación del archivo

    Args:
        file_path: Ruta al archivo
        sample_size: Número de bytes a muestrear

    Returns:
        Codificación detectada
    """
    try:
        import chardet

        path = Path(file_path)
        with open(path, "rb") as f:
            sample = f.read(sample_size)

        result = chardet.detect(sample)
        encoding = result.get("encoding", "utf-8")
        confidence = result.get("confidence", 0)

        logger = logging.getLogger(__name__)
        logger.debug(
            f"Codificación detectada: {encoding} (confianza: {confidence:.2f})"
        )

        # Respaldo a utf-8 si la confianza es muy baja o encoding es None
        if confidence < 0.7 or encoding is None:
            logger.warning(
                f"Confianza baja ({confidence:.2f}) para codificación {encoding}, usando utf-8"
            )
            return "utf-8"

        return str(encoding)

    except ImportError:
        logger = logging.getLogger(__name__)
        logger.warning("chardet no disponible, usando codificación utf-8")
        return "utf-8"
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error detectando codificación: {e}, usando utf-8")
        return "utf-8"


def validate_file_path(file_path: Union[str, Path], must_exist: bool = True) -> Path:
    """
    Validar y normalizar ruta de archivo

    Args:
        file_path: Ruta de archivo a validar
        must_exist: Si el archivo debe existir

    Returns:
        Objeto Path validado
    """
    path = Path(file_path)

    if must_exist and not path.exists():
        raise FileNotFoundError(f"El archivo no existe: {file_path}")

    if must_exist and not path.is_file():
        raise ValueError(f"La ruta no es un archivo: {file_path}")

    return path.resolve()


def format_bytes(bytes_value: int) -> str:
    """
    Formatear bytes en cadena legible por humanos

    Args:
        bytes_value: Número de bytes

    Returns:
        Cadena formateada (ej., "1.5 MB")
    """
    value = float(bytes_value)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if value < 1024.0:
            return f"{value:.1f} {unit}"
        value /= 1024.0
    return f"{value:.1f} PB"


def format_duration(seconds: float) -> str:
    """
    Formatear duración en segundos a cadena legible por humanos

    Args:
        seconds: Duración en segundos

    Returns:
        Cadena formateada (ej., "2m 30s")
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.0f}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


def safe_convert_to_numeric(value: Any, default: Any = None) -> Union[int, float, Any]:
    """
    Convertir valor a tipo numérico de forma segura

    Args:
        value: Valor a convertir
        default: Valor por defecto si la conversión falla

    Returns:
        Valor numérico convertido o valor por defecto
    """
    if pd.isna(value) or value is None:
        return default

    try:
        # Intentar entero primero
        if isinstance(value, str):
            # Remover formato común
            clean_value = str(value).replace(",", "").replace(" ", "").strip()
            if clean_value == "":
                return default

            # Verificar si es un porcentaje
            if clean_value.endswith("%"):
                return float(clean_value[:-1]) / 100

            # Intentar convertir
            if "." in clean_value:
                return float(clean_value)
            else:
                return int(clean_value)
        else:
            # Conversión directa para no-strings
            return float(value) if "." in str(value) else int(value)

    except (ValueError, TypeError):
        return default


def clean_text_value(value: Any) -> str:
    """
    Limpiar y normalizar valores de texto

    Args:
        value: Valor de texto a limpiar

    Returns:
        Texto limpio
    """
    if pd.isna(value) or value is None:
        return ""

    text = str(value).strip()

    # Remover espacios extra
    text = re.sub(r"\s+", " ", text)

    # Remover caracteres no imprimibles
    text = "".join(char for char in text if char.isprintable() or char.isspace())

    return text


def get_memory_usage_mb() -> float:
    """
    Obtener uso actual de memoria en MB

    Returns:
        Uso de memoria en MB
    """
    try:
        import psutil

        process = psutil.Process()
        return process.memory_info().rss / (1024 * 1024)
    except ImportError:
        return 0.0


def create_backup_filename(original_path: Union[str, Path]) -> Path:
    """
    Crear nombre de archivo de respaldo con marca de tiempo

    Args:
        original_path: Ruta del archivo original

    Returns:
        Ruta del archivo de respaldo
    """
    path = Path(original_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    backup_name = f"{path.stem}_backup_{timestamp}{path.suffix}"
    return path.parent / backup_name


def load_json_safely(file_path: Union[str, Path], default: Any = None) -> Any:
    """
    Cargar archivo JSON de forma segura con manejo de errores

    Args:
        file_path: Ruta al archivo JSON
        default: Valor por defecto si la carga falla

    Returns:
        Datos JSON cargados o valor por defecto
    """
    logger = logging.getLogger(__name__)
    path = Path(file_path)

    if not path.exists():
        logger.warning(f"Archivo JSON no encontrado: {file_path}")
        return default

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"JSON inválido en archivo {file_path}: {e}")
        return default
    except Exception as e:
        logger.error(f"Error cargando archivo JSON {file_path}: {e}")
        return default


def save_json_safely(
    data: Any, file_path: Union[str, Path], create_backup: bool = True
) -> bool:
    """
    Guardar datos a archivo JSON de forma segura

    Args:
        data: Datos a guardar
        file_path: Ruta del archivo de salida
        create_backup: Si crear respaldo si el archivo existe

    Returns:
        Estado de éxito
    """
    logger = logging.getLogger(__name__)
    path = Path(file_path)

    try:
        # Crear respaldo si se solicita y el archivo existe
        if create_backup and path.exists():
            backup_path = create_backup_filename(path)
            path.rename(backup_path)
            logger.info(f"Respaldo creado: {backup_path}")

        # Asegurar que el directorio existe
        path.parent.mkdir(parents=True, exist_ok=True)

        # Guardar JSON
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)

        logger.debug(f"Datos JSON guardados en: {path}")
        return True

    except Exception as e:
        logger.error(f"Error guardando JSON en {file_path}: {e}")
        return False


class ProgressTracker:
    """
    Utilidad simple para seguimiento de progreso
    """

    def __init__(self, total_steps: int, description: str = "Procesando"):
        self.total_steps = total_steps
        self.current_step = 0
        self.description = description
        self.start_time = time.time()
        self.logger = logging.getLogger(__name__)

    def update(self, step: int = 1, message: str = ""):
        """Actualizar progreso"""
        self.current_step += step
        percentage = (self.current_step / self.total_steps) * 100

        elapsed_time = time.time() - self.start_time

        if self.current_step > 0:
            eta_seconds = (elapsed_time / self.current_step) * (
                self.total_steps - self.current_step
            )
            eta_str = format_duration(eta_seconds)
        else:
            eta_str = "Desconocido"

        progress_msg = f"{self.description}: {self.current_step}/{self.total_steps} ({percentage:.1f}%) - ETA: {eta_str}"
        if message:
            progress_msg += f" - {message}"

        self.logger.info(progress_msg)

    def finish(self):
        """Marcar progreso como completo"""
        elapsed_time = time.time() - self.start_time
        self.logger.info(
            f"{self.description} completado en {format_duration(elapsed_time)}"
        )


def get_dataframe_info(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Obtener información completa sobre un DataFrame

    Args:
        df: DataFrame a analizar

    Returns:
        Diccionario con información del DataFrame
    """
    info = {
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "dtypes": df.dtypes.to_dict(),
        "memory_usage_mb": df.memory_usage(deep=True).sum() / (1024 * 1024),
        "null_counts": df.isnull().sum().to_dict(),
        "null_percentages": (df.isnull().sum() / len(df) * 100).to_dict(),
    }

    # Agregar estadísticas de columnas numéricas
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        info["numeric_summary"] = df[numeric_cols].describe().to_dict()

    return info


def validate_dataframe_not_empty(df: pd.DataFrame, min_rows: int = 1) -> bool:
    """
    Validar que el DataFrame no esté vacío y tenga filas mínimas

    Args:
        df: DataFrame a validar
        min_rows: Filas mínimas requeridas

    Returns:
        True si es válido, lanza excepción en caso contrario
    """
    if df is None:
        raise ValueError("DataFrame es None")

    if df.empty:
        raise ValueError("DataFrame está vacío")

    if len(df) < min_rows:
        raise ValueError(
            f"DataFrame tiene {len(df)} filas, mínimo requerido: {min_rows}"
        )

    if len(df.columns) == 0:
        raise ValueError("DataFrame no tiene columnas")

    return True


# Utilidades de manejo de errores
class ProcessingError(Exception):
    """Excepción personalizada para errores de procesamiento"""

    pass


class ValidationError(ProcessingError):
    """Excepción personalizada para errores de validación"""

    pass


class ConfigurationError(ProcessingError):
    """Excepción personalizada para errores de configuración"""

    pass


def handle_processing_error(error: Exception, context: str = "") -> str:
    """
    Manejar errores de procesamiento con logging

    Args:
        error: Excepción que ocurrió
        context: Información adicional de contexto

    Returns:
        Mensaje de error formateado
    """
    logger = logging.getLogger(__name__)

    error_msg = f"Error de procesamiento"
    if context:
        error_msg += f" en {context}"
    error_msg += f": {str(error)}"

    if isinstance(error, (FileNotFoundError, PermissionError)):
        logger.error(error_msg)
    elif isinstance(error, (ValidationError, ConfigurationError)):
        logger.warning(error_msg)
    else:
        logger.error(f"Inesperado {error_msg}", exc_info=True)

    return error_msg


# Inicialización del módulo
def initialize_utils(
    log_level: str = "INFO", log_dir: Optional[str] = None
) -> logging.Logger:
    """
    Inicializar módulo de utilidades con logging

    Args:
        log_level: Nivel de logging
        log_dir: Directorio para archivos de log

    Returns:
        Logger configurado
    """
    return setup_logging(log_level=log_level, log_dir=log_dir)


if __name__ == "__main__":
    # Pruebas de utilidades
    logger = initialize_utils("DEBUG")
    logger.info("Módulo de utilidades cargado exitosamente")

    # Probar algunas utilidades
    print(f"Prueba formato tamaño archivo: {format_bytes(1536000)}")
    print(f"Prueba formato duración: {format_duration(125.7)}")
    print(
        f"Prueba limpieza nombre columna: {clean_column_name('Nombre Usuario (Primero)!')}"
    )
