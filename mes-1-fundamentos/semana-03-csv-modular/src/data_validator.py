#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
✅ Data Validator - Validación de Datos para Sistema CSV

Este módulo proporciona capacidades completas de validación de datos incluyendo:
- Validación de esquemas con tipos de datos configurables
- Reglas de validación personalizadas para calidad de datos
- Verificación de rangos de valores y validación de patrones
- Validación estadística y detección de valores atípicos
- Framework de validación extensible

Autor: Angel Baez
Fecha: Octubre 2025
Proyecto: Data + Automation Engineer Journey - Semana 3
Versión: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable, Union, Tuple
from enum import Enum
import pandas as pd
import numpy as np
import re
import logging
from pathlib import Path
import json
from datetime import datetime


def _safe_float_conversion(value: Any, default: float = 0.0) -> float:
    """
    Convertir valor a float de forma segura, manejando tipos escalares complejos de pandas

    Args:
        value: Valor a convertir
        default: Valor por defecto si la conversión falla

    Returns:
        Valor convertido a float o valor por defecto
    """
    if value is None or pd.isna(value):
        return default

    try:
        # Intentar conversión directa
        if isinstance(value, (int, float)):
            return float(value)

        # Manejar tipos de numpy/pandas
        if hasattr(value, "item"):
            # Para escalares de numpy/pandas, usar .item() para extraer el valor Python nativo
            return float(value.item())

        # Conversión estándar
        return float(value)

    except (TypeError, ValueError, AttributeError, OverflowError):
        return default


class ValidationLevel(Enum):
    """Niveles de severidad de validación"""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class ValidationType(Enum):
    """Tipos de verificaciones de validación"""

    TYPE_CHECK = "type_check"
    RANGE_CHECK = "range_check"
    PATTERN_CHECK = "pattern_check"
    CUSTOM_RULE = "custom_rule"
    NULL_CHECK = "null_check"
    UNIQUE_CHECK = "unique_check"
    STATISTICAL = "statistical"


@dataclass
class ValidationRule:
    """Representa una regla de validación individual"""

    name: str
    description: str
    validation_type: ValidationType
    level: ValidationLevel
    column: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    custom_function: Optional[Callable] = None


@dataclass
class ValidationResult:
    """Resultado de una verificación de validación"""

    rule_name: str
    validation_type: ValidationType
    level: ValidationLevel
    column: Optional[str]
    passed: bool
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    affected_rows: List[int] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ValidationReport:
    """Reporte completo de validación"""

    total_rules: int
    passed_rules: int
    failed_rules: int
    warnings: int
    errors: int
    results: List[ValidationResult]
    summary: Dict[str, Any]
    execution_time: float
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def success_rate(self) -> float:
        """Calcula la tasa de éxito de validación"""
        if self.total_rules == 0:
            return 100.0
        return (self.passed_rules / self.total_rules) * 100

    @property
    def is_valid(self) -> bool:
        """Verifica si los datos pasaron todas las validaciones de nivel error"""
        return self.errors == 0


class DataValidator:
    """
    Sistema completo de validación de datos para archivos CSV

    Características:
    - Validación de esquemas con verificación de tipos
    - Reglas de validación personalizadas
    - Validación estadística
    - Coincidencia de patrones
    - Validación de valores nulos
    - Restricciones de unicidad
    - Validaciones de rango
    """

    def __init__(self, config_manager=None):
        """
        Inicializa el DataValidator

        Args:
            config_manager: Instancia del gestor de configuración
        """
        self.config_manager = config_manager
        self.logger = logging.getLogger(__name__)
        self.validation_rules: List[ValidationRule] = []
        self.schema: Dict[str, str] = {}
        self._custom_validators: Dict[str, Callable] = {}

        # Cargar reglas de validación por defecto si hay configuración disponible
        if config_manager:
            self._load_validation_config()

    def _load_validation_config(self):
        """Carga la configuración de validación desde el gestor de configuración"""
        try:
            if self.config_manager is not None and hasattr(
                self.config_manager, "get_validation_config"
            ):
                validation_config = self.config_manager.get_validation_config()

                # Cargar esquema si está definido
                if (
                    hasattr(validation_config, "schema_file")
                    and validation_config.schema_file
                ):
                    schema_path = Path(validation_config.schema_file)
                    if schema_path.exists():
                        with open(schema_path, "r") as f:
                            schema_data = json.load(f)
                            self.schema = schema_data.get("schema", {})
                            self._load_rules_from_config(schema_data.get("rules", []))

                self.logger.info("Configuración de validación cargada exitosamente")
            else:
                self.logger.warning(
                    "config_manager es None o no tiene el método get_validation_config"
                )

        except Exception as e:
            self.logger.warning(
                f"No se pudo cargar la configuración de validación: {e}"
            )

    def _load_rules_from_config(self, rules_config: List[Dict]):
        """Carga reglas de validación desde la configuración"""
        for rule_config in rules_config:
            try:
                rule = ValidationRule(
                    name=rule_config["name"],
                    description=rule_config["description"],
                    validation_type=ValidationType(rule_config["type"]),
                    level=ValidationLevel(rule_config["level"]),
                    column=rule_config.get("column"),
                    parameters=rule_config.get("parameters", {}),
                )
                self.validation_rules.append(rule)
            except Exception as e:
                self.logger.error(
                    f"Error cargando regla de validación {rule_config.get('name', 'unknown')}: {e}"
                )

    def set_schema(self, schema: Dict[str, str]):
        """
        Establece el esquema de datos esperado

        Args:
            schema: Diccionario que mapea nombres de columnas a tipos de datos esperados
        """
        self.schema = schema
        self.logger.info(f"Esquema configurado con {len(schema)} columnas")

    def add_validation_rule(self, rule: ValidationRule):
        """
        Agrega una regla de validación personalizada

        Args:
            rule: Instancia de ValidationRule
        """
        self.validation_rules.append(rule)
        self.logger.info(f"Regla de validación agregada: {rule.name}")

    def add_custom_validator(self, name: str, validator_func: Callable):
        """
        Agrega una función validadora personalizada

        Args:
            name: Nombre del validador personalizado
            validator_func: Función que toma (value, **kwargs) y devuelve bool
        """
        self._custom_validators[name] = validator_func
        self.logger.info(f"Validador personalizado agregado: {name}")

    def validate_dataframe(self, df: pd.DataFrame) -> ValidationReport:
        """
        Valida un DataFrame de pandas

        Args:
            df: DataFrame a validar

        Returns:
            ValidationReport con los resultados de validación
        """
        start_time = datetime.now()
        results: List[ValidationResult] = []

        self.logger.info(
            f"Iniciando validación de DataFrame con {len(df)} filas y {len(df.columns)} columnas"
        )

        # Ejecutar todas las reglas de validación
        for rule in self.validation_rules:
            try:
                result = self._execute_validation_rule(df, rule)
                results.append(result)
            except Exception as e:
                # Crear resultado de error para validación fallida
                error_result = ValidationResult(
                    rule_name=rule.name,
                    validation_type=rule.validation_type,
                    level=ValidationLevel.ERROR,
                    column=rule.column,
                    passed=False,
                    message=f"Fallo en la ejecución de regla de validación: {e}",
                    details={"error": str(e)},
                )
                results.append(error_result)
                self.logger.error(
                    f"La regla de validación {rule.name} falló al ejecutarse: {e}"
                )

        # Agregar validación automática de esquema si está configurado
        if self.schema:
            schema_results = self._validate_schema(df)
            results.extend(schema_results)

        # Calcular estadísticas de resumen
        total_rules = len(results)
        passed_rules = sum(1 for r in results if r.passed)
        failed_rules = total_rules - passed_rules
        warnings = sum(
            1 for r in results if not r.passed and r.level == ValidationLevel.WARNING
        )
        errors = sum(
            1 for r in results if not r.passed and r.level == ValidationLevel.ERROR
        )

        execution_time = (datetime.now() - start_time).total_seconds()

        # Crear resumen
        summary = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "success_rate": (
                (passed_rules / total_rules * 100) if total_rules > 0 else 100.0
            ),
            "execution_time_seconds": execution_time,
            "validation_summary": {
                "passed": passed_rules,
                "failed": failed_rules,
                "warnings": warnings,
                "errors": errors,
            },
        }

        report = ValidationReport(
            total_rules=total_rules,
            passed_rules=passed_rules,
            failed_rules=failed_rules,
            warnings=warnings,
            errors=errors,
            results=results,
            summary=summary,
            execution_time=execution_time,
        )

        self.logger.info(
            f"Validación completada: {passed_rules}/{total_rules} reglas pasaron"
        )
        return report

    def _execute_validation_rule(
        self, df: pd.DataFrame, rule: ValidationRule
    ) -> ValidationResult:
        """Ejecuta una sola regla de validación"""

        if rule.validation_type == ValidationType.TYPE_CHECK:
            return self._validate_type(df, rule)
        elif rule.validation_type == ValidationType.RANGE_CHECK:
            return self._validate_range(df, rule)
        elif rule.validation_type == ValidationType.PATTERN_CHECK:
            return self._validate_pattern(df, rule)
        elif rule.validation_type == ValidationType.NULL_CHECK:
            return self._validate_null(df, rule)
        elif rule.validation_type == ValidationType.UNIQUE_CHECK:
            return self._validate_unique(df, rule)
        elif rule.validation_type == ValidationType.STATISTICAL:
            return self._validate_statistical(df, rule)
        elif rule.validation_type == ValidationType.CUSTOM_RULE:
            return self._validate_custom(df, rule)
        else:
            return ValidationResult(
                rule_name=rule.name,
                validation_type=rule.validation_type,
                level=rule.level,
                column=rule.column,
                passed=False,
                message=f"Tipo de validación desconocido: {rule.validation_type}",
            )

    def _validate_schema(self, df: pd.DataFrame) -> List[ValidationResult]:
        """Valida DataFrame contra el esquema definido"""
        results = []

        for column, expected_type in self.schema.items():
            if column not in df.columns:
                result = ValidationResult(
                    rule_name=f"schema_check_{column}",
                    validation_type=ValidationType.TYPE_CHECK,
                    level=ValidationLevel.ERROR,
                    column=column,
                    passed=False,
                    message=f"La columna requerida '{column}' falta en el conjunto de datos",
                )
                results.append(result)
                continue

            # Verificar compatibilidad de tipos de datos
            actual_type = str(df[column].dtype)
            compatible = self._check_type_compatibility(actual_type, expected_type)

            result = ValidationResult(
                rule_name=f"schema_type_{column}",
                validation_type=ValidationType.TYPE_CHECK,
                level=(
                    ValidationLevel.WARNING if not compatible else ValidationLevel.INFO
                ),
                column=column,
                passed=compatible,
                message=f"Verificación de tipo columna '{column}': esperado {expected_type}, obtenido {actual_type}",
                details={"expected_type": expected_type, "actual_type": actual_type},
            )
            results.append(result)

        return results

    def _validate_type(
        self, df: pd.DataFrame, rule: ValidationRule
    ) -> ValidationResult:
        """Valida tipos de datos"""
        column = rule.column
        expected_type = rule.parameters.get("type")

        if column not in df.columns:
            return ValidationResult(
                rule_name=rule.name,
                validation_type=rule.validation_type,
                level=rule.level,
                column=column,
                passed=False,
                message=f"Columna '{column}' no encontrada",
            )

        actual_type = str(df[column].dtype)
        if expected_type is None:
            compatible = False
        else:
            compatible = self._check_type_compatibility(actual_type, expected_type)

        return ValidationResult(
            rule_name=rule.name,
            validation_type=rule.validation_type,
            level=rule.level,
            column=column,
            passed=compatible,
            message=f"Validación de tipo para '{column}': {'pasó' if compatible else 'falló'}",
            details={"expected": expected_type, "actual": actual_type},
        )

    def _validate_range(
        self, df: pd.DataFrame, rule: ValidationRule
    ) -> ValidationResult:
        """Valida rangos de valores"""
        column = rule.column
        min_val = rule.parameters.get("min")
        max_val = rule.parameters.get("max")

        if column not in df.columns:
            return ValidationResult(
                rule_name=rule.name,
                validation_type=rule.validation_type,
                level=rule.level,
                column=column,
                passed=False,
                message=f"Column '{column}' not found",
            )

        # Verificar datos numéricos
        if not pd.api.types.is_numeric_dtype(df[column]):
            return ValidationResult(
                rule_name=rule.name,
                validation_type=rule.validation_type,
                level=rule.level,
                column=column,
                passed=False,
                message=f"La validación de rango requiere datos numéricos, obtenido {df[column].dtype}",
            )

        violations = []
        if min_val is not None:
            violations.extend(df[df[column] < min_val].index.tolist())
        if max_val is not None:
            violations.extend(df[df[column] > max_val].index.tolist())

        violations = list(set(violations))  # Eliminar duplicados
        passed = len(violations) == 0

        return ValidationResult(
            rule_name=rule.name,
            validation_type=rule.validation_type,
            level=rule.level,
            column=column,
            passed=passed,
            message=f"Validación de rango para '{column}': {len(violations)} violaciones encontradas",
            details={"min": min_val, "max": max_val, "violations": len(violations)},
            affected_rows=violations,
        )

    def _validate_pattern(
        self, df: pd.DataFrame, rule: ValidationRule
    ) -> ValidationResult:
        """Valida patrones de datos usando regex"""
        column = rule.column
        pattern = rule.parameters.get("pattern")

        if column not in df.columns:
            return ValidationResult(
                rule_name=rule.name,
                validation_type=rule.validation_type,
                level=rule.level,
                column=column,
                passed=False,
                message=f"Column '{column}' not found",
            )

        if not pattern:
            return ValidationResult(
                rule_name=rule.name,
                validation_type=rule.validation_type,
                level=rule.level,
                column=column,
                passed=False,
                message="El parámetro pattern es requerido",
            )

        try:
            # Convertir a string y verificar patrón
            str_series = df[column].astype(str)
            matches = str_series.str.match(pattern, na=False)
            violations = df[~matches].index.tolist()
            passed = len(violations) == 0

            return ValidationResult(
                rule_name=rule.name,
                validation_type=rule.validation_type,
                level=rule.level,
                column=column,
                passed=passed,
                message=f"Validación de patrón para '{column}': {len(violations)} violaciones encontradas",
                details={"pattern": pattern, "violations": len(violations)},
                affected_rows=violations,
            )
        except Exception as e:
            return ValidationResult(
                rule_name=rule.name,
                validation_type=rule.validation_type,
                level=rule.level,
                column=column,
                passed=False,
                message=f"La validación de patrón falló: {e}",
            )

    def _validate_null(
        self, df: pd.DataFrame, rule: ValidationRule
    ) -> ValidationResult:
        """Valida valores nulos"""
        column = rule.column
        allow_null = rule.parameters.get("allow_null", True)
        max_null_percentage = rule.parameters.get("max_null_percentage", 100)

        if column not in df.columns:
            return ValidationResult(
                rule_name=rule.name,
                validation_type=rule.validation_type,
                level=rule.level,
                column=column,
                passed=False,
                message=f"Column '{column}' not found",
            )

        null_count = df[column].isnull().sum()
        null_percentage = (null_count / len(df)) * 100

        if not allow_null and null_count > 0:
            return ValidationResult(
                rule_name=rule.name,
                validation_type=rule.validation_type,
                level=rule.level,
                column=column,
                passed=False,
                message=f"Valores nulos no permitidos en '{column}', encontrados {null_count} nulos",
                details={"null_count": null_count, "null_percentage": null_percentage},
            )

        if null_percentage > max_null_percentage:
            return ValidationResult(
                rule_name=rule.name,
                validation_type=rule.validation_type,
                level=rule.level,
                column=column,
                passed=False,
                message=f"Demasiados valores nulos en '{column}': {null_percentage:.2f}% > {max_null_percentage}%",
                details={"null_count": null_count, "null_percentage": null_percentage},
            )

        return ValidationResult(
            rule_name=rule.name,
            validation_type=rule.validation_type,
            level=rule.level,
            column=column,
            passed=True,
            message=f"Validación de nulos pasó para '{column}'",
            details={"null_count": null_count, "null_percentage": null_percentage},
        )

    def _validate_unique(
        self, df: pd.DataFrame, rule: ValidationRule
    ) -> ValidationResult:
        """Valida restricciones de unicidad"""
        column = rule.column

        if column not in df.columns:
            return ValidationResult(
                rule_name=rule.name,
                validation_type=rule.validation_type,
                level=rule.level,
                column=column,
                passed=False,
                message=f"Column '{column}' not found",
            )

        duplicate_count = df[column].duplicated().sum()
        passed = duplicate_count == 0

        return ValidationResult(
            rule_name=rule.name,
            validation_type=rule.validation_type,
            level=rule.level,
            column=column,
            passed=passed,
            message=f"Validación de unicidad para '{column}': {duplicate_count} duplicados encontrados",
            details={
                "duplicate_count": duplicate_count,
                "unique_count": df[column].nunique(),
            },
        )

    def _validate_statistical(
        self, df: pd.DataFrame, rule: ValidationRule
    ) -> ValidationResult:
        """Valida propiedades estadísticas (outliers, distribución)"""
        column = rule.column
        check_type = rule.parameters.get("check_type", "outliers")

        if column not in df.columns:
            return ValidationResult(
                rule_name=rule.name,
                validation_type=rule.validation_type,
                level=rule.level,
                column=column,
                passed=False,
                message=f"Column '{column}' not found",
            )

        if not pd.api.types.is_numeric_dtype(df[column]):
            return ValidationResult(
                rule_name=rule.name,
                validation_type=rule.validation_type,
                level=rule.level,
                column=column,
                passed=False,
                message=f"La validación estadística requiere datos numéricos, obtenido {df[column].dtype}",
            )

        if check_type == "outliers":
            return self._check_outliers(df, rule)
        elif check_type == "distribution":
            return self._check_distribution(df, rule)
        else:
            return ValidationResult(
                rule_name=rule.name,
                validation_type=rule.validation_type,
                level=rule.level,
                column=column,
                passed=False,
                message=f"Tipo de verificación estadística desconocido: {check_type}",
            )

    def _check_outliers(
        self, df: pd.DataFrame, rule: ValidationRule
    ) -> ValidationResult:
        """Verifica outliers usando método IQR"""
        column = rule.column
        method = rule.parameters.get("method", "iqr")
        threshold = rule.parameters.get("threshold", 1.5)

        if method == "iqr":
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR

            outliers = df[
                (df[column] < lower_bound) | (df[column] > upper_bound)
            ].index.tolist()
        else:
            # Método Z-score
            z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
            outliers = df[z_scores > threshold].index.tolist()

        outlier_percentage = (len(outliers) / len(df)) * 100
        max_outlier_percentage = rule.parameters.get("max_outlier_percentage", 5.0)

        passed = outlier_percentage <= max_outlier_percentage

        return ValidationResult(
            rule_name=rule.name,
            validation_type=rule.validation_type,
            level=rule.level,
            column=column,
            passed=passed,
            message=f"Verificación de valores atípicos para '{column}': {len(outliers)} outliers ({outlier_percentage:.2f}%)",
            details={
                "outlier_count": len(outliers),
                "outlier_percentage": outlier_percentage,
                "method": method,
                "threshold": threshold,
            },
            affected_rows=outliers,
        )

    def _check_distribution(
        self, df: pd.DataFrame, rule: ValidationRule
    ) -> ValidationResult:
        """Verifica propiedades de distribución"""
        column = rule.column
        expected_distribution = rule.parameters.get("expected_distribution", "normal")

        # Verificaciones simples de distribución
        mean_val = _safe_float_conversion(df[column].mean())
        median_val = _safe_float_conversion(df[column].median())
        std_val = _safe_float_conversion(df[column].std())
        skewness = _safe_float_conversion(df[column].skew())

        details = {
            "mean": mean_val,
            "median": median_val,
            "std": std_val,
            "skewness": skewness,
            "expected_distribution": expected_distribution,
        }

        # Verificación básica de normalidad (simplificada)
        if expected_distribution == "normal":
            # Verificar si la asimetría está dentro de límites razonables
            try:
                passed = abs(skewness) < 2.0  # Umbral común para asimetría razonable
                message = f"Verificación de distribución para '{column}': asimetría = {skewness:.2f}"
            except (TypeError, ValueError):
                passed = False
                message = f"Verificación de distribución para '{column}': asimetría no es numérica ({skewness})"
        else:
            passed = True  # Para otras distribuciones, solo pasar por ahora
            message = f"Verificación de distribución para '{column}': estadísticas básicas calculadas"

        return ValidationResult(
            rule_name=rule.name,
            validation_type=rule.validation_type,
            level=rule.level,
            column=column,
            passed=passed,
            message=message,
            details=details,
        )

    def _validate_custom(
        self, df: pd.DataFrame, rule: ValidationRule
    ) -> ValidationResult:
        """Ejecuta función de validación personalizada"""
        custom_function = rule.custom_function
        function_name = rule.parameters.get("function_name")

        if custom_function:
            validator_func = custom_function
        elif function_name and function_name in self._custom_validators:
            validator_func = self._custom_validators[function_name]
        else:
            return ValidationResult(
                rule_name=rule.name,
                validation_type=rule.validation_type,
                level=rule.level,
                column=rule.column,
                passed=False,
                message="Función de validador personalizado no encontrada",
            )

        try:
            # Ejecutar validador personalizado
            if rule.column:
                if rule.column not in df.columns:
                    return ValidationResult(
                        rule_name=rule.name,
                        validation_type=rule.validation_type,
                        level=rule.level,
                        column=rule.column,
                        passed=False,
                        message=f"Column '{rule.column}' not found",
                    )
                result = validator_func(df[rule.column], **rule.parameters)
            else:
                result = validator_func(df, **rule.parameters)

            if isinstance(result, bool):
                passed = result
                message = f"Validación personalizada {'pasó' if result else 'falló'}"
                details = {}
            elif isinstance(result, dict):
                passed = result.get("passed", False)
                message = result.get("message", "Validación personalizada ejecutada")
                details = result.get("details", {})
            else:
                passed = False
                message = f"Tipo de retorno del validador personalizado inválido: {type(result)}"
                details = {}

            return ValidationResult(
                rule_name=rule.name,
                validation_type=rule.validation_type,
                level=rule.level,
                column=rule.column,
                passed=passed,
                message=message,
                details=details,
            )

        except Exception as e:
            return ValidationResult(
                rule_name=rule.name,
                validation_type=rule.validation_type,
                level=rule.level,
                column=rule.column,
                passed=False,
                message=f"Error en validación personalizada: {e}",
                details={"error": str(e)},
            )

    def _check_type_compatibility(self, actual_type: str, expected_type: str) -> bool:
        """Verifica si el tipo de dato actual es compatible con el tipo esperado"""
        type_mapping = {
            "int": ["int64", "int32", "int16", "int8"],
            "integer": ["int64", "int32", "int16", "int8"],
            "float": ["float64", "float32"],
            "number": ["int64", "int32", "int16", "int8", "float64", "float32"],
            "string": ["object", "string"],
            "text": ["object", "string"],
            "datetime": ["datetime64[ns]", "datetime64"],
            "bool": ["bool"],
            "boolean": ["bool"],
        }

        expected_lower = expected_type.lower()
        if expected_lower in type_mapping:
            return actual_type in type_mapping[expected_lower]

        # Coincidencia directa
        return actual_type.lower() == expected_lower

    def export_report(
        self,
        report: ValidationReport,
        output_path: Union[str, Path],
        format_type: str = "json",
    ):
        """
        Exporta el reporte de validación a archivo

        Args:
            report: ValidationReport a exportar
            output_path: Ruta del archivo de salida
            format_type: Formato de exportación ('json', 'csv', 'html')
        """
        try:
            output_path = Path(output_path)

            if format_type.lower() == "json":
                self._export_json_report(report, output_path)
            elif format_type.lower() == "csv":
                self._export_csv_report(report, output_path)
            elif format_type.lower() == "html":
                self._export_html_report(report, output_path)
            else:
                raise ValueError(f"Formato de exportación no soportado: {format_type}")

            self.logger.info(f"Reporte de validación exportado a {output_path}")

        except Exception as e:
            self.logger.error(f"Error exportando reporte de validación: {e}")
            raise

    def _export_json_report(self, report: ValidationReport, output_path: Path):
        """Exporta reporte como JSON"""
        report_dict = {
            "metadata": {
                "timestamp": report.timestamp.isoformat(),
                "execution_time": report.execution_time,
                "total_rules": report.total_rules,
                "success_rate": report.success_rate,
                "is_valid": report.is_valid,
            },
            "summary": report.summary,
            "results": [
                {
                    "rule_name": result.rule_name,
                    "validation_type": result.validation_type.value,
                    "level": result.level.value,
                    "column": result.column,
                    "passed": result.passed,
                    "message": result.message,
                    "details": result.details,
                    "affected_rows_count": len(result.affected_rows),
                    "timestamp": result.timestamp.isoformat(),
                }
                for result in report.results
            ],
        }

        with open(output_path, "w") as f:
            json.dump(report_dict, f, indent=2, default=str)

    def _export_csv_report(self, report: ValidationReport, output_path: Path):
        """Exporta reporte como CSV"""
        rows = []
        for result in report.results:
            rows.append(
                {
                    "rule_name": result.rule_name,
                    "validation_type": result.validation_type.value,
                    "level": result.level.value,
                    "column": result.column,
                    "passed": result.passed,
                    "message": result.message,
                    "affected_rows_count": len(result.affected_rows),
                    "timestamp": result.timestamp.isoformat(),
                }
            )

        df_results = pd.DataFrame(rows)
        df_results.to_csv(output_path, index=False)

    def _export_html_report(self, report: ValidationReport, output_path: Path):
        """Exporta reporte como HTML"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Data Validation Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .summary {{ background-color: #f0f0f0; padding: 10px; margin: 10px 0; }}
                .passed {{ color: green; }}
                .failed {{ color: red; }}
                .warning {{ color: orange; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>Data Validation Report</h1>
            <div class="summary">
                <h2>Summary</h2>
                <p><strong>Timestamp:</strong> {report.timestamp}</p>
                <p><strong>Total Rules:</strong> {report.total_rules}</p>
                <p><strong>Success Rate:</strong> {report.success_rate:.2f}%</p>
                <p><strong>Is Valid:</strong> {report.is_valid}</p>
                <p><strong>Execution Time:</strong> {report.execution_time:.2f}s</p>
            </div>
            
            <h2>Validation Results</h2>
            <table>
                <tr>
                    <th>Rule Name</th>
                    <th>Type</th>
                    <th>Level</th>
                    <th>Column</th>
                    <th>Status</th>
                    <th>Message</th>
                </tr>
        """

        for result in report.results:
            status_class = (
                "passed"
                if result.passed
                else (
                    "warning" if result.level == ValidationLevel.WARNING else "failed"
                )
            )
            status_text = "PASSED" if result.passed else "FAILED"

            html_content += f"""
                <tr>
                    <td>{result.rule_name}</td>
                    <td>{result.validation_type.value}</td>
                    <td>{result.level.value}</td>
                    <td>{result.column or 'N/A'}</td>
                    <td class="{status_class}">{status_text}</td>
                    <td>{result.message}</td>
                </tr>
            """

        html_content += """
            </table>
        </body>
        </html>
        """

        with open(output_path, "w") as f:
            f.write(html_content)

    def create_standard_rules(self) -> List[ValidationRule]:
        """
        Crea un conjunto de reglas de validación estándar

        Returns:
            Lista de reglas de validación comunes
        """
        standard_rules = [
            # Verificaciones básicas de nulos
            ValidationRule(
                name="no_completely_empty_columns",
                description="Verificar que ninguna columna esté completamente vacía",
                validation_type=ValidationType.NULL_CHECK,
                level=ValidationLevel.ERROR,
                parameters={"max_null_percentage": 99.9},
            ),
            # La columna ID debe ser única
            ValidationRule(
                name="id_uniqueness",
                description="Las columnas ID deben ser únicas",
                validation_type=ValidationType.UNIQUE_CHECK,
                level=ValidationLevel.ERROR,
                column="id",
                parameters={},
            ),
            # Validación de patrón de email
            ValidationRule(
                name="email_format",
                description="Las direcciones de email deben tener formato válido",
                validation_type=ValidationType.PATTERN_CHECK,
                level=ValidationLevel.WARNING,
                column="email",
                parameters={
                    "pattern": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
                },
            ),
        ]

        return standard_rules

    def quick_validate(
        self, df: pd.DataFrame, rules: Optional[List[str]] = None
    ) -> ValidationReport:
        """
        Validación rápida con reglas estándar

        Args:
            df: DataFrame a validar
            rules: Lista de nombres de reglas a aplicar (predeterminado: todas las reglas estándar)

        Returns:
            ValidationReport
        """
        if not self.validation_rules:
            # Agregar reglas estándar si no existen
            standard_rules = self.create_standard_rules()
            for rule in standard_rules:
                self.add_validation_rule(rule)

        return self.validate_dataframe(df)
