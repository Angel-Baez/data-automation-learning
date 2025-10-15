#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests para el módulo ConfigManager

Este archivo contiene pruebas unitarias para verificar la funcionalidad
del sistema de gestión de configuración.

Autor: Angel Baez
Fecha: Octubre 2025
Proyecto: Data + Automation Engineer Journey - Semana 3
"""

import pytest
import tempfile
import json
from pathlib import Path
import os
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config_manager import (
    ConfigManager,
    ProcessingConfig,
    PathConfig,
    ValidationConfig,
    LoggingConfig,
)


class TestConfigManager:
    """Prueba la funcionalidad del ConfigManager"""

    def test_init_with_default_config(self):
        """Prueba inicialización con configuración por defecto"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_manager = ConfigManager(config_dir=temp_dir)

            # Verificar que se inicializaron las configuraciones
            assert config_manager.processing is not None
            assert config_manager.paths is not None
            assert config_manager.validation is not None
            assert config_manager.logging_config is not None
            assert config_manager.notifications is not None
            assert config_manager.processing_rules is not None

    def test_init_with_env_file(self):
        """Prueba inicialización con archivo .env"""
        # Crear archivo .env temporal
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("CSV_MAX_FILE_SIZE_MB=50\n")
            f.write("CSV_DEFAULT_ENCODING=utf-8\n")
            env_file = f.name

        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                config_manager = ConfigManager(env_file=env_file, config_dir=temp_dir)

                # Verificar que las configuraciones están presentes
                assert config_manager.processing is not None
                assert isinstance(config_manager.processing, ProcessingConfig)
        finally:
            os.unlink(env_file)

    def test_processing_config_attributes(self):
        """Prueba atributos de ProcessingConfig"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_manager = ConfigManager(config_dir=temp_dir)
            processing_config = config_manager.processing

            # Verificar atributos por defecto
            assert hasattr(processing_config, "max_file_size_mb")
            assert hasattr(processing_config, "batch_size")
            assert hasattr(processing_config, "default_encoding")
            assert hasattr(processing_config, "default_delimiter")
            assert hasattr(processing_config, "cpu_cores")
            assert hasattr(processing_config, "memory_limit_gb")

            # Verificar valores por defecto
            assert processing_config.max_file_size_mb == 100
            assert processing_config.batch_size == 1000
            assert processing_config.default_encoding == "utf-8"
            assert processing_config.default_delimiter == ","

    def test_path_config_attributes(self):
        """Prueba atributos de PathConfig"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_manager = ConfigManager(config_dir=temp_dir)
            path_config = config_manager.paths

            # Verificar atributos
            assert hasattr(path_config, "input_directory")
            assert hasattr(path_config, "output_directory")
            assert hasattr(path_config, "temp_directory")
            assert hasattr(path_config, "log_directory")

            # Verificar que son objetos Path
            assert isinstance(path_config.input_directory, Path)
            assert isinstance(path_config.output_directory, Path)
            assert isinstance(path_config.temp_directory, Path)
            assert isinstance(path_config.log_directory, Path)

    def test_validation_config_attributes(self):
        """Prueba atributos de ValidationConfig"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_manager = ConfigManager(config_dir=temp_dir)
            validation_config = config_manager.validation

            # Verificar que es una instancia de ValidationConfig
            assert isinstance(validation_config, ValidationConfig)

    def test_logging_config_attributes(self):
        """Prueba atributos de LoggingConfig"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_manager = ConfigManager(config_dir=temp_dir)
            logging_config = config_manager.logging_config

            # Verificar que es una instancia de LoggingConfig
            assert isinstance(logging_config, LoggingConfig)

    def test_get_config_summary(self):
        """Prueba el método get_config_summary"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_manager = ConfigManager(config_dir=temp_dir)
            summary = config_manager.get_config_summary()

            # Verificar que es un diccionario
            assert isinstance(summary, dict)

            # Verificar que contiene las secciones principales
            assert "processing" in summary or "paths" in summary

    def test_update_config(self):
        """Prueba el método update_config"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_manager = ConfigManager(config_dir=temp_dir)

            # Obtener valor inicial
            initial_size = config_manager.processing.max_file_size_mb

            # Actualizar configuración
            config_manager.update_config("processing", "max_file_size_mb", 200)

            # Verificar que se actualizó
            assert config_manager.processing.max_file_size_mb == 200
            assert config_manager.processing.max_file_size_mb != initial_size

    def test_processing_rules_loaded(self):
        """Prueba que las reglas de procesamiento se cargan correctamente"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_manager = ConfigManager(config_dir=temp_dir)

            # Verificar que las reglas son un diccionario
            assert isinstance(config_manager.processing_rules, dict)

            # Verificar que tiene claves esperadas por defecto
            assert len(config_manager.processing_rules) > 0

    def test_directories_created(self):
        """Prueba que los directorios se crean correctamente"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_manager = ConfigManager(config_dir=temp_dir)

            # Los directorios se crean durante la inicialización
            assert config_manager.paths.input_directory.exists()
            assert config_manager.paths.output_directory.exists()
            assert config_manager.paths.temp_directory.exists()
            assert config_manager.paths.log_directory.exists()


class TestProcessingConfig:
    """Pruebas específicas para ProcessingConfig"""

    def test_processing_config_creation(self):
        """Prueba creación de ProcessingConfig"""
        config = ProcessingConfig()

        # Verificar valores por defecto
        assert config.max_file_size_mb == 100
        assert config.batch_size == 1000
        assert config.default_encoding == "utf-8"
        assert config.default_delimiter == ","
        assert config.cpu_cores == 0
        assert config.memory_limit_gb == 2.0


class TestPathConfig:
    """Pruebas específicas para PathConfig"""

    def test_path_config_creation(self):
        """Prueba creación de PathConfig"""
        config = PathConfig()

        # Verificar valores por defecto
        assert config.input_directory == Path("data/input")
        assert config.output_directory == Path("data/output")
        assert config.temp_directory == Path("data/temp")
        assert config.log_directory == Path("logs")

    def test_path_config_post_init(self):
        """Prueba el método __post_init__ de PathConfig"""
        # Crear con Path personalizada
        config = PathConfig()
        config.input_directory = Path("test/input")
        config.__post_init__()

        # Verificar que sigue siendo Path
        assert isinstance(config.input_directory, Path)
        assert str(config.input_directory) == "test/input"


class TestValidationConfig:
    """Pruebas específicas para ValidationConfig"""

    def test_validation_config_creation(self):
        """Prueba creación de ValidationConfig"""
        config = ValidationConfig()

        # Verificar que es una instancia válida
        assert isinstance(config, ValidationConfig)


class TestLoggingConfig:
    """Pruebas específicas para LoggingConfig"""

    def test_logging_config_creation(self):
        """Prueba creación de LoggingConfig"""
        config = LoggingConfig()

        # Verificar que es una instancia válida
        assert isinstance(config, LoggingConfig)


@pytest.fixture
def temp_env_file():
    """Fixture para crear archivo .env temporal"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
        f.write("CSV_MAX_FILE_SIZE_MB=75\n")
        f.write("CSV_DEFAULT_ENCODING=utf-8\n")
        f.write("CSV_BATCH_SIZE=2000\n")
        env_file = f.name

    yield env_file

    # Cleanup
    if os.path.exists(env_file):
        os.unlink(env_file)


@pytest.fixture
def temp_processing_rules_file():
    """Fixture para crear archivo de reglas de procesamiento temporal"""
    rules = {
        "data_cleaning": {
            "remove_empty_rows": True,
            "remove_empty_columns": True,
            "standardize_whitespace": True,
        },
        "data_validation": {"check_data_types": True, "validate_ranges": True},
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(rules, f, indent=2)
        rules_file = f.name

    yield rules_file

    # Cleanup
    if os.path.exists(rules_file):
        os.unlink(rules_file)
