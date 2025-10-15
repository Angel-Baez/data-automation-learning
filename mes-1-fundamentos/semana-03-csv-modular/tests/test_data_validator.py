#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests para el módulo DataValidator

Este archivo contiene pruebas unitarias para verificar la funcionalidad
del sistema de validación de datos.

Autor: Angel Baez
Fecha: Octubre 2025
Proyecto: Data + Automation Engineer Journey - Semana 3
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_validator import (
    DataValidator,
    ValidationRule,
    ValidationResult,
    ValidationReport,
    ValidationLevel,
    ValidationType,
)


class TestDataValidator:
    """Pruebas para la funcionalidad del DataValidator"""

    def test_init_without_config(self):
        """Prueba inicialización sin ConfigManager"""
        validator = DataValidator()

        assert validator.config_manager is None
        assert isinstance(validator.validation_rules, list)
        assert isinstance(validator.schema, dict)
        assert len(validator.validation_rules) == 0

    def test_set_schema(self):
        """Prueba configuración de esquema"""
        validator = DataValidator()
        schema = {"id": "int", "nombre": "string", "edad": "int", "salario": "float"}

        validator.set_schema(schema)

        assert validator.schema == schema

    def test_add_validation_rule(self):
        """Prueba agregar regla de validación"""
        validator = DataValidator()

        rule = ValidationRule(
            name="test_rule",
            description="Regla de prueba",
            validation_type=ValidationType.TYPE_CHECK,
            level=ValidationLevel.ERROR,
            column="edad",
            parameters={"type": "int"},
        )

        validator.add_validation_rule(rule)

        assert len(validator.validation_rules) == 1
        assert validator.validation_rules[0].name == "test_rule"

    def test_validate_dataframe_empty_rules(self, sample_dataframe):
        """Prueba validación con DataFrame y sin reglas"""
        validator = DataValidator()

        report = validator.validate_dataframe(sample_dataframe)

        assert isinstance(report, ValidationReport)
        assert report.total_rules >= 0
        assert report.is_valid == True  # Sin reglas, todo es válido

    def test_validate_dataframe_with_schema(self, sample_dataframe):
        """Prueba validación con esquema"""
        validator = DataValidator()

        # Configurar esquema
        schema = {"id": "int", "nombre": "string", "edad": "int", "salario": "float"}
        validator.set_schema(schema)

        report = validator.validate_dataframe(sample_dataframe)

        assert isinstance(report, ValidationReport)
        assert report.total_rules > 0

    def test_validate_dataframe_with_rules(self, sample_dataframe):
        """Prueba validación con reglas personalizadas"""
        validator = DataValidator()

        # Agregar regla de rango para edad
        age_rule = ValidationRule(
            name="age_range",
            description="Edad debe estar entre 18 y 65",
            validation_type=ValidationType.RANGE_CHECK,
            level=ValidationLevel.WARNING,
            column="edad",
            parameters={"min": 18, "max": 65},
        )

        validator.add_validation_rule(age_rule)

        report = validator.validate_dataframe(sample_dataframe)

        assert isinstance(report, ValidationReport)
        assert report.total_rules == 1

    def test_quick_validate(self, sample_dataframe):
        """Prueba validación rápida con reglas estándar"""
        validator = DataValidator()

        report = validator.quick_validate(sample_dataframe)

        assert isinstance(report, ValidationReport)
        assert report.total_rules > 0  # Debe tener reglas estándar

    def test_create_standard_rules(self):
        """Prueba creación de reglas estándar"""
        validator = DataValidator()

        standard_rules = validator.create_standard_rules()

        assert isinstance(standard_rules, list)
        assert len(standard_rules) > 0

        # Verificar que todas son ValidationRule
        for rule in standard_rules:
            assert isinstance(rule, ValidationRule)

    def test_add_custom_validator(self, sample_dataframe):
        """Prueba agregar validador personalizado"""
        validator = DataValidator()

        # Definir validador personalizado
        def validate_positive_salary(value, **kwargs):
            return (value > 0).all() if hasattr(value, "all") else value > 0

        validator.add_custom_validator("positive_salary", validate_positive_salary)

        # Crear regla que use el validador personalizado
        custom_rule = ValidationRule(
            name="salary_positive",
            description="Salario debe ser positivo",
            validation_type=ValidationType.CUSTOM_RULE,
            level=ValidationLevel.ERROR,
            column="salario",
            parameters={"function_name": "positive_salary"},
        )

        validator.add_validation_rule(custom_rule)

        report = validator.validate_dataframe(sample_dataframe)

        assert isinstance(report, ValidationReport)


class TestValidationRule:
    """Pruebas específicas para ValidationRule"""

    def test_validation_rule_creation(self):
        """Prueba creación de ValidationRule"""
        rule = ValidationRule(
            name="test_rule",
            description="Regla de prueba",
            validation_type=ValidationType.TYPE_CHECK,
            level=ValidationLevel.ERROR,
            column="test_column",
            parameters={"type": "string"},
        )

        assert rule.name == "test_rule"
        assert rule.description == "Regla de prueba"
        assert rule.validation_type == ValidationType.TYPE_CHECK
        assert rule.level == ValidationLevel.ERROR
        assert rule.column == "test_column"
        assert rule.parameters == {"type": "string"}


class TestValidationResult:
    """Pruebas específicas para ValidationResult"""

    def test_validation_result_creation(self):
        """Prueba creación de ValidationResult"""
        result = ValidationResult(
            rule_name="test_rule",
            validation_type=ValidationType.TYPE_CHECK,
            level=ValidationLevel.ERROR,
            column="test_column",
            passed=True,
            message="Validación exitosa",
        )

        assert result.rule_name == "test_rule"
        assert result.validation_type == ValidationType.TYPE_CHECK
        assert result.level == ValidationLevel.ERROR
        assert result.column == "test_column"
        assert result.passed == True
        assert result.message == "Validación exitosa"
        assert isinstance(result.details, dict)
        assert isinstance(result.affected_rows, list)


class TestValidationReport:
    """Pruebas específicas para ValidationReport"""

    def test_validation_report_creation(self):
        """Prueba creación de ValidationReport"""
        results = [
            ValidationResult(
                rule_name="rule1",
                validation_type=ValidationType.TYPE_CHECK,
                level=ValidationLevel.ERROR,
                column="col1",
                passed=True,
                message="OK",
            ),
            ValidationResult(
                rule_name="rule2",
                validation_type=ValidationType.RANGE_CHECK,
                level=ValidationLevel.WARNING,
                column="col2",
                passed=False,
                message="Warning",
            ),
        ]

        report = ValidationReport(
            total_rules=2,
            passed_rules=1,
            failed_rules=1,
            warnings=1,
            errors=0,
            results=results,
            summary={"test": "summary"},
            execution_time=1.5,
        )

        assert report.total_rules == 2
        assert report.passed_rules == 1
        assert report.failed_rules == 1
        assert report.warnings == 1
        assert report.errors == 0
        assert len(report.results) == 2
        assert report.execution_time == 1.5

    def test_validation_report_success_rate(self):
        """Prueba cálculo de tasa de éxito"""
        report = ValidationReport(
            total_rules=4,
            passed_rules=3,
            failed_rules=1,
            warnings=0,
            errors=1,
            results=[],
            summary={},
            execution_time=1.0,
        )

        assert report.success_rate == 75.0

    def test_validation_report_is_valid(self):
        """Prueba propiedad is_valid"""
        # Reporte sin errores
        report_valid = ValidationReport(
            total_rules=2,
            passed_rules=1,
            failed_rules=1,
            warnings=1,
            errors=0,
            results=[],
            summary={},
            execution_time=1.0,
        )

        assert report_valid.is_valid == True

        # Reporte con errores
        report_invalid = ValidationReport(
            total_rules=2,
            passed_rules=1,
            failed_rules=1,
            warnings=0,
            errors=1,
            results=[],
            summary={},
            execution_time=1.0,
        )

        assert report_invalid.is_valid == False


class TestValidationTypes:
    """Pruebas específicas para diferentes tipos de validación"""

    def test_type_validation(self, sample_dataframe):
        """Prueba validación de tipos"""
        validator = DataValidator()

        # Regla de tipo para columna id (debe ser int)
        type_rule = ValidationRule(
            name="id_type",
            description="ID debe ser entero",
            validation_type=ValidationType.TYPE_CHECK,
            level=ValidationLevel.ERROR,
            column="id",
            parameters={"type": "int"},
        )

        validator.add_validation_rule(type_rule)
        report = validator.validate_dataframe(sample_dataframe)

        assert len(report.results) == 1

    def test_range_validation(self, sample_dataframe):
        """Prueba validación de rangos"""
        validator = DataValidator()

        # Regla de rango para edad
        range_rule = ValidationRule(
            name="age_range",
            description="Edad debe estar entre 0 y 100",
            validation_type=ValidationType.RANGE_CHECK,
            level=ValidationLevel.WARNING,
            column="edad",
            parameters={"min": 0, "max": 100},
        )

        validator.add_validation_rule(range_rule)
        report = validator.validate_dataframe(sample_dataframe)

        assert len(report.results) == 1

    def test_null_validation(self, sample_dataframe_with_nulls):
        """Prueba validación de valores nulos"""
        validator = DataValidator()

        # Regla de nulos para columna nombre
        null_rule = ValidationRule(
            name="name_not_null",
            description="Nombre no puede ser nulo",
            validation_type=ValidationType.NULL_CHECK,
            level=ValidationLevel.ERROR,
            column="nombre",
            parameters={"allow_null": False},
        )

        validator.add_validation_rule(null_rule)
        report = validator.validate_dataframe(sample_dataframe_with_nulls)

        assert len(report.results) == 1

    def test_unique_validation(self, sample_dataframe_with_duplicates):
        """Prueba validación de unicidad"""
        validator = DataValidator()

        # Regla de unicidad para ID
        unique_rule = ValidationRule(
            name="id_unique",
            description="ID debe ser único",
            validation_type=ValidationType.UNIQUE_CHECK,
            level=ValidationLevel.ERROR,
            column="id",
            parameters={},
        )

        validator.add_validation_rule(unique_rule)
        report = validator.validate_dataframe(sample_dataframe_with_duplicates)

        assert len(report.results) == 1


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


@pytest.fixture
def sample_dataframe_with_nulls():
    """Fixture para crear DataFrame con valores nulos"""
    data = {
        "id": [1, 2, 3, 4, 5],
        "nombre": ["Ana", None, "María", "Pedro", "Carmen"],
        "edad": [25, 30, None, 40, 45],
        "salario": [30000.0, 45000.0, 50000.0, None, 55000.0],
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_dataframe_with_duplicates():
    """Fixture para crear DataFrame con duplicados"""
    data = {
        "id": [1, 2, 2, 4, 5],  # ID duplicado
        "nombre": ["Ana", "Juan", "María", "Pedro", "Carmen"],
        "edad": [25, 30, 35, 40, 45],
        "salario": [30000.0, 45000.0, 50000.0, 60000.0, 55000.0],
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_dataframe_with_issues():
    """Fixture para crear DataFrame con múltiples problemas"""
    data = {
        "id": [1, 2, 2, None, 5],  # Duplicado y nulo
        "nombre": ["Ana", "", "María", "Pedro", None],  # Vacío y nulo
        "edad": [25, -5, 35, 150, 45],  # Valores fuera de rango
        "email": [
            "ana@test.com",
            "invalid-email",
            "maria@test.com",
            "pedro@",
            "",
        ],  # Emails inválidos
        "salario": [30000.0, 45000.0, -1000.0, 60000.0, None],  # Negativo y nulo
    }
    return pd.DataFrame(data)
