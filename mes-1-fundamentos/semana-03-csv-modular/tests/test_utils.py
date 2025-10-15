#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests para el módulo Utils

Este archivo contiene pruebas unitarias para verificar la funcionalidad
de las utilidades del sistema.

Autor: Angel Baez
Fecha: Octubre 2025
Proyecto: Data + Automation Engineer Journey - Semana 3
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import tempfile
import os
import logging
import json
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import (
    setup_logging,
    ensure_directory,
    safe_file_operation,
    performance_monitor,
    timing_context,
    get_file_size_mb,
    clean_column_name,
    detect_delimiter,
    detect_encoding,
    validate_file_path,
    format_bytes,
    format_duration,
    safe_convert_to_numeric,
    clean_text_value,
    get_memory_usage_mb,
    create_backup_filename,
    load_json_safely,
    save_json_safely,
    ProgressTracker,
    ProcessingError,
    ValidationError,
    ConfigurationError,
)


class TestLoggingSetup:
    """Pruebas para la configuración de logging"""

    def test_setup_logging_default(self):
        """Prueba configuración básica de logging"""
        logger = setup_logging()

        assert isinstance(logger, logging.Logger)
        assert logger.level <= logging.INFO

    def test_setup_logging_with_level(self):
        """Prueba configuración con nivel específico"""
        logger = setup_logging(log_level="DEBUG")

        assert isinstance(logger, logging.Logger)
        assert logger.level <= logging.DEBUG


class TestPathUtilities:
    """Pruebas para utilidades de manejo de rutas"""

    def test_ensure_directory(self, temp_dir):
        """Prueba creación de directorios"""
        new_dir = Path(temp_dir) / "test_directory"
        result = ensure_directory(new_dir)

        assert isinstance(result, Path)
        assert result.exists()
        assert result.is_dir()

    def test_validate_file_path_existing(self, sample_csv_file):
        """Prueba validación de archivo existente"""
        result = validate_file_path(sample_csv_file)
        assert isinstance(result, Path)
        assert result.exists()

    def test_validate_file_path_nonexisting(self, temp_dir):
        """Prueba validación de archivo no existente"""
        invalid_path = Path(temp_dir) / "nonexistent.csv"

        with pytest.raises(FileNotFoundError):
            validate_file_path(invalid_path)

    def test_get_file_size_mb(self, sample_csv_file):
        """Prueba obtención del tamaño de archivo en MB"""
        size_mb = get_file_size_mb(sample_csv_file)

        assert isinstance(size_mb, float)
        assert size_mb > 0


class TestDataUtilities:
    """Pruebas para utilidades de manejo de datos"""

    def test_clean_column_name(self):
        """Prueba limpieza de nombres de columnas"""
        # Nombres con espacios y caracteres especiales
        assert "nombre_completo" in clean_column_name("Nombre Completo")
        assert "id" in clean_column_name("ID#")
        assert "fecha" in clean_column_name("Fecha/Hora")

    def test_detect_delimiter(self, sample_csv_file):
        """Prueba detección de delimitador CSV"""
        delimiter = detect_delimiter(sample_csv_file)

        assert isinstance(delimiter, str)
        assert delimiter in [",", ";", "\t", "|"]

    def test_detect_encoding(self, sample_csv_file):
        """Prueba detección de codificación"""
        encoding = detect_encoding(sample_csv_file)

        assert isinstance(encoding, str)
        assert encoding in ["utf-8", "latin-1", "ascii", "cp1252"]

    def test_safe_convert_to_numeric_valid(self):
        """Prueba conversión segura a numérico con valores válidos"""
        assert safe_convert_to_numeric("123") == 123
        assert safe_convert_to_numeric("123.45") == 123.45
        assert safe_convert_to_numeric(456) == 456

    def test_safe_convert_to_numeric_invalid(self):
        """Prueba conversión segura a numérico con valores inválidos"""
        assert safe_convert_to_numeric("abc", default=0) == 0
        assert safe_convert_to_numeric("", default=-1) == -1
        assert safe_convert_to_numeric(None, default=99) == 99

    def test_clean_text_value(self):
        """Prueba limpieza de valores de texto"""
        assert clean_text_value("  Hola Mundo  ") == "Hola Mundo"
        assert clean_text_value("") == ""
        assert clean_text_value(None) == ""
        assert clean_text_value(123) == "123"


class TestFormatUtilities:
    """Pruebas para utilidades de formateo"""

    def test_format_bytes(self):
        """Prueba formateo de bytes"""
        assert "B" in format_bytes(500)
        assert "KB" in format_bytes(1024)
        assert "MB" in format_bytes(1048576)
        assert "GB" in format_bytes(1073741824)

    def test_format_duration(self):
        """Prueba formateo de duración"""
        # Segundos
        result_seconds = format_duration(30)
        assert isinstance(result_seconds, str)
        assert "s" in result_seconds

        # Minutos
        result_minutes = format_duration(65)
        assert isinstance(result_minutes, str)

        # Horas
        result_hours = format_duration(3661)
        assert isinstance(result_hours, str)


class TestPerformanceUtilities:
    """Pruebas para utilidades de rendimiento"""

    def test_performance_monitor_decorator(self):
        """Prueba el decorador de monitoreo de rendimiento"""

        @performance_monitor
        def test_function():
            import time

            time.sleep(0.01)  # Pausa muy corta
            return "done"

        result = test_function()
        assert result == "done"

    def test_timing_context_manager(self):
        """Prueba el context manager de timing"""
        with timing_context("test_operation"):
            import time

            time.sleep(0.01)  # Pausa muy corta

    def test_get_memory_usage_mb(self):
        """Prueba obtención de uso de memoria"""
        memory_mb = get_memory_usage_mb()

        assert isinstance(memory_mb, float)
        assert memory_mb > 0


class TestFileUtilities:
    """Pruebas para utilidades de archivos"""

    def test_create_backup_filename(self, sample_csv_file):
        """Prueba creación de nombre de backup"""
        backup_path = create_backup_filename(sample_csv_file)

        assert isinstance(backup_path, Path)
        assert backup_path.suffix == sample_csv_file.suffix
        assert "backup" in backup_path.name or "_" in backup_path.name

    def test_load_json_safely_valid(self, temp_dir):
        """Prueba carga segura de JSON válido"""
        json_file = Path(temp_dir) / "test.json"
        test_data = {"key": "value", "number": 42}

        # Crear archivo JSON
        with open(json_file, "w") as f:
            json.dump(test_data, f)

        loaded_data = load_json_safely(json_file)
        assert loaded_data == test_data

    def test_load_json_safely_invalid(self, temp_dir):
        """Prueba carga segura de JSON inválido"""
        invalid_json_file = Path(temp_dir) / "invalid.json"

        # Crear archivo JSON inválido
        with open(invalid_json_file, "w") as f:
            f.write("invalid json content")

        default_value = {"default": True}
        loaded_data = load_json_safely(invalid_json_file, default=default_value)
        assert loaded_data == default_value

    def test_save_json_safely(self, temp_dir):
        """Prueba guardado seguro de JSON"""
        json_file = Path(temp_dir) / "output.json"
        test_data = {"key": "value", "list": [1, 2, 3]}

        result = save_json_safely(test_data, json_file, create_backup=False)

        assert result == True
        assert json_file.exists()

        # Verificar contenido
        loaded_data = load_json_safely(json_file)
        assert loaded_data == test_data


class TestProgressTracker:
    """Pruebas para la funcionalidad del ProgressTracker"""

    def test_progress_tracker_init(self):
        """Prueba inicialización del ProgressTracker"""
        tracker = ProgressTracker(total_steps=100)

        assert tracker.total_steps == 100
        assert tracker.current_step == 0
        assert tracker.description == "Procesando"

    def test_progress_tracker_init_with_description(self):
        """Prueba inicialización con descripción personalizada"""
        tracker = ProgressTracker(total_steps=50, description="Processing files")

        assert tracker.total_steps == 50
        assert tracker.current_step == 0
        assert tracker.description == "Processing files"

    def test_progress_tracker_update(self):
        """Prueba actualización de progreso"""
        tracker = ProgressTracker(total_steps=10)

        tracker.update(3)
        assert tracker.current_step == 3

        tracker.update(2)
        assert tracker.current_step == 5

    def test_progress_tracker_update_with_message(self):
        """Prueba actualización con mensaje"""
        tracker = ProgressTracker(total_steps=5)

        # La función update registra el progreso pero no devuelve nada
        tracker.update(1, "Procesando archivo 1")
        assert tracker.current_step == 1

    def test_progress_tracker_finish(self):
        """Prueba finalización del progreso"""
        tracker = ProgressTracker(total_steps=10)
        tracker.update(5)

        # La función finish registra la finalización
        tracker.finish()

        # Verificar que no cambió el current_step
        assert tracker.current_step == 5


class TestCustomExceptions:
    """Pruebas para excepciones personalizadas"""

    def test_processing_error(self):
        """Prueba excepción ProcessingError"""
        with pytest.raises(ProcessingError):
            raise ProcessingError("Error de procesamiento")

    def test_validation_error(self):
        """Prueba excepción ValidationError"""
        with pytest.raises(ValidationError):
            raise ValidationError("Error de validación")

        # Verificar herencia
        with pytest.raises(ProcessingError):
            raise ValidationError("Error de validación")

    def test_configuration_error(self):
        """Prueba excepción ConfigurationError"""
        with pytest.raises(ConfigurationError):
            raise ConfigurationError("Error de configuración")

        # Verificar herencia
        with pytest.raises(ProcessingError):
            raise ConfigurationError("Error de configuración")


class TestSafeFileOperation:
    """Pruebas para operaciones seguras de archivos"""

    def test_safe_file_operation_success(self, temp_dir):
        """Prueba operación de archivo exitosa"""

        @safe_file_operation("test_write")
        def write_test_file():
            test_file = Path(temp_dir) / "test.txt"
            test_file.write_text("test content")
            return test_file

        result = write_test_file()
        assert isinstance(result, Path)
        assert result.exists()

    def test_safe_file_operation_failure(self):
        """Prueba operación de archivo fallida"""

        @safe_file_operation("test_fail")
        def failing_operation():
            raise PermissionError("No se puede escribir archivo")

        # La operación debería manejar la excepción y re-lanzarla
        with pytest.raises(PermissionError):
            failing_operation()


# Fixtures
@pytest.fixture
def temp_dir():
    """Fixture para crear directorio temporal"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def sample_csv_file(temp_dir):
    """Fixture para crear archivo CSV de ejemplo"""
    csv_path = Path(temp_dir) / "sample.csv"

    data = {
        "id": [1, 2, 3, 4, 5],
        "nombre": ["Ana", "Juan", "María", "Pedro", "Carmen"],
        "edad": [25, 30, 35, 40, 45],
        "salario": [30000.0, 45000.0, 50000.0, 60000.0, 55000.0],
    }

    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)

    return csv_path


@pytest.fixture
def sample_dataframe():
    """Fixture para crear DataFrame de ejemplo"""
    data = {
        "id": [1, 2, 3, 4, 5],
        "nombre": ["Ana", "Juan", "María", "Pedro", "Carmen"],
        "edad": [25, 30, 35, 40, 45],
        "salario": [30000.0, 45000.0, 50000.0, 60000.0, 55000.0],
    }
    return pd.DataFrame(data)
