#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests para el módulo CSVProcessor

Este archivo contiene pruebas unitarias para verificar la funcionalidad
del procesador de archivos CSV.

Autor: Angel Baez
Fecha: Octubre 2025
Proyecto: Data + Automation Engineer Journey - Semana 3
"""

import pytest
import tempfile
import pandas as pd
from pathlib import Path
import os
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.csv_processor import CSVProcessor, ProcessingStats, CSVMetadata
from src.config_manager import ConfigManager


class TestCSVProcessor:
    """Pruebas para la funcionalidad del CSVProcessor"""

    def test_init_with_config_manager(self):
        """Prueba inicialización con ConfigManager"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_manager = ConfigManager(config_dir=temp_dir)
            processor = CSVProcessor(config_manager)

            # Verificar que se inicialice correctamente con los atributos esperados
            assert processor is not None
            assert hasattr(processor, "config")
            assert hasattr(processor, "logger")
            assert hasattr(processor, "processing_rules")
            assert hasattr(processor, "output_rules")

    def test_process_file_basic(self, sample_csv_file):
        """Prueba procesamiento básico de archivo CSV"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_manager = ConfigManager(config_dir=temp_dir)
            processor = CSVProcessor(config_manager)

            output_path = Path(temp_dir) / "output.csv"

            # Procesar archivo
            result_df, stats, metadata = processor.process_file(
                input_path=sample_csv_file, output_path=output_path, profile="default"
            )

            # Verificar resultados
            assert isinstance(result_df, pd.DataFrame)
            assert isinstance(stats, ProcessingStats)
            assert isinstance(metadata, CSVMetadata)
            assert output_path.exists()

    def test_process_file_without_output(self, sample_csv_file):
        """Prueba procesamiento sin archivo de salida"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_manager = ConfigManager(config_dir=temp_dir)
            processor = CSVProcessor(config_manager)

            # Procesar archivo sin salida
            result_df, stats, metadata = processor.process_file(
                input_path=sample_csv_file, profile="default"
            )

            # Verificar resultados
            assert isinstance(result_df, pd.DataFrame)
            assert isinstance(stats, ProcessingStats)
            assert isinstance(metadata, CSVMetadata)

    def test_processing_stats_attributes(self, sample_csv_file):
        """Prueba atributos de ProcessingStats"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_manager = ConfigManager(config_dir=temp_dir)
            processor = CSVProcessor(config_manager)

            result_df, stats, metadata = processor.process_file(
                input_path=sample_csv_file, profile="default"
            )

            # Verificar atributos
            assert hasattr(stats, "original_rows")
            assert hasattr(stats, "final_rows")
            assert hasattr(stats, "original_columns")
            assert hasattr(stats, "final_columns")
            assert hasattr(stats, "processing_time_seconds")
            assert hasattr(stats, "quality_score")

            # Verificar tipos
            assert isinstance(stats.original_rows, int)
            assert isinstance(stats.final_rows, int)
            assert isinstance(stats.processing_time_seconds, float)
            assert isinstance(stats.quality_score, float)

    def test_csv_metadata_attributes(self, sample_csv_file):
        """Prueba atributos de CSVMetadata"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_manager = ConfigManager(config_dir=temp_dir)
            processor = CSVProcessor(config_manager)

            result_df, stats, metadata = processor.process_file(
                input_path=sample_csv_file, profile="default"
            )

            # Verificar atributos
            assert hasattr(metadata, "filename")
            assert hasattr(metadata, "file_size_mb")
            assert hasattr(metadata, "encoding")
            assert hasattr(metadata, "delimiter")
            assert hasattr(metadata, "column_names")
            assert hasattr(metadata, "data_types")

            # Verificar tipos
            assert isinstance(metadata.filename, str)
            assert isinstance(metadata.file_size_mb, float)
            assert isinstance(metadata.encoding, str)
            assert isinstance(metadata.delimiter, str)
            assert isinstance(metadata.column_names, list)
            assert isinstance(metadata.data_types, dict)

    def test_get_processing_summary(self, sample_csv_file):
        """Prueba generación de resumen de procesamiento"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_manager = ConfigManager(config_dir=temp_dir)
            processor = CSVProcessor(config_manager)

            result_df, stats, metadata = processor.process_file(
                input_path=sample_csv_file, profile="default"
            )

            # Obtener resumen
            summary = processor.get_processing_summary(stats, metadata)

            # Verificar que es string y no vacío
            assert isinstance(summary, str)
            assert len(summary) > 0


class TestProcessingStats:
    """Pruebas específicas para ProcessingStats"""

    def test_processing_stats_creation(self):
        """Prueba creación de ProcessingStats"""
        stats = ProcessingStats()

        # Verificar valores por defecto
        assert stats.original_rows == 0
        assert stats.final_rows == 0
        assert stats.original_columns == 0
        assert stats.final_columns == 0
        assert stats.duplicates_removed == 0
        assert stats.missing_values_filled == 0
        assert stats.invalid_rows_removed == 0
        assert stats.processing_time_seconds == 0.0
        assert stats.memory_usage_mb == 0.0
        assert stats.quality_score == 0.0

    def test_processing_stats_to_dict(self):
        """Prueba conversión de ProcessingStats a diccionario"""
        stats = ProcessingStats(
            original_rows=100,
            final_rows=95,
            original_columns=5,
            final_columns=5,
            duplicates_removed=3,
            processing_time_seconds=1.5,
            quality_score=0.95,
        )

        stats_dict = stats.to_dict()

        # Verificar que es diccionario
        assert isinstance(stats_dict, dict)

        # Verificar claves importantes
        assert "original_rows" in stats_dict
        assert "final_rows" in stats_dict
        assert "processing_time_seconds" in stats_dict
        assert "quality_score" in stats_dict

        # Verificar valores
        assert stats_dict["original_rows"] == 100
        assert stats_dict["final_rows"] == 95
        assert stats_dict["duplicates_removed"] == 3


class TestCSVMetadata:
    """Pruebas específicas para CSVMetadata"""

    def test_csv_metadata_creation(self):
        """Prueba creación de CSVMetadata"""
        metadata = CSVMetadata()

        # Verificar valores por defecto
        assert metadata.filename == ""
        assert metadata.file_size_mb == 0.0
        assert metadata.encoding == "utf-8"
        assert metadata.delimiter == ","
        assert metadata.has_header == True
        assert isinstance(metadata.column_names, list)
        assert isinstance(metadata.data_types, dict)

    def test_csv_metadata_to_dict(self):
        """Prueba conversión de CSVMetadata a diccionario"""
        metadata = CSVMetadata(
            filename="test.csv",
            file_size_mb=1.5,
            encoding="utf-8",
            delimiter=",",
            column_names=["col1", "col2", "col3"],
            data_types={"col1": "int64", "col2": "object", "col3": "float64"},
        )

        metadata_dict = metadata.to_dict()

        # Verificar que es diccionario
        assert isinstance(metadata_dict, dict)

        # Verificar claves importantes
        assert "filename" in metadata_dict
        assert "file_size_mb" in metadata_dict
        assert "encoding" in metadata_dict
        assert "delimiter" in metadata_dict
        assert "column_names" in metadata_dict
        assert "data_types" in metadata_dict


@pytest.fixture
def sample_csv_file():
    """Fixture para crear un archivo CSV de ejemplo"""
    # Crear datos de ejemplo
    data = {
        "id": [1, 2, 3, 4, 5],
        "nombre": ["Ana", "Juan", "María", "Pedro", "Carmen"],
        "edad": [25, 30, 35, 40, 45],
        "salario": [30000.0, 45000.0, 50000.0, 60000.0, 55000.0],
        "activo": [True, True, False, True, True],
    }

    df = pd.DataFrame(data)

    # Crear archivo temporal
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        df.to_csv(f.name, index=False)
        csv_file = f.name

    yield csv_file

    # Cleanup
    if os.path.exists(csv_file):
        os.unlink(csv_file)


@pytest.fixture
def sample_csv_with_issues():
    """Fixture para crear un archivo CSV con problemas"""
    # Crear datos con problemas
    data = {
        "id": [1, 2, 2, 4, None],  # Duplicado y valor nulo
        "nombre": ["Ana", "Juan", "", "Pedro", "Carmen"],  # Valor vacío
        "edad": [25, 30, -5, 40, 150],  # Valores fuera de rango
        "email": [
            "ana@test.com",
            "juan@test",
            "maria@test.com",
            "pedro@test.com",
            "",
        ],  # Email inválido
        "salario": [30000.0, 45000.0, 50000.0, None, 55000.0],  # Valor nulo
    }

    df = pd.DataFrame(data)

    # Crear archivo temporal
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        df.to_csv(f.name, index=False)
        csv_file = f.name

    yield csv_file

    # Cleanup
    if os.path.exists(csv_file):
        os.unlink(csv_file)
