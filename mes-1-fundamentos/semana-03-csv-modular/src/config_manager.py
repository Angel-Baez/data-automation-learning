#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 Config Manager - Gestión de Configuración y Variables de Entorno

Este módulo maneja toda la configuración del sistema de procesamiento CSV,
incluyendo variables de entorno, validación de configuración y carga
de archivos de configuración JSON.

Autor: Angel Baez
Fecha: Octubre 2025
Proyecto: Data + Automation Engineer Journey - Semana 3
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, field
from dotenv import load_dotenv


@dataclass
class ProcessingConfig:
    """Configuración de procesamiento de datos"""

    max_file_size_mb: int = 100
    batch_size: int = 1000
    default_encoding: str = "utf-8"
    default_delimiter: str = ","
    cpu_cores: int = 0
    memory_limit_gb: float = 2.0


@dataclass
class PathConfig:
    """Configuración de rutas de archivos"""

    input_directory: Path = field(default_factory=lambda: Path("data/input"))
    output_directory: Path = field(default_factory=lambda: Path("data/output"))
    temp_directory: Path = field(default_factory=lambda: Path("data/temp"))
    log_directory: Path = field(default_factory=lambda: Path("logs"))

    def __post_init__(self):
        """Convierte strings a Path objects si es necesario"""
        for field_name, field_value in self.__dict__.items():
            if isinstance(field_value, str):
                setattr(self, field_name, Path(field_value))


@dataclass
class ValidationConfig:
    """Configuración de validación de datos"""

    max_validation_errors: int = 50
    strict_validation: bool = False
    min_quality_score: float = 0.8
    max_missing_percentage: float = 10.0
    max_duplicate_percentage: float = 5.0


@dataclass
class LoggingConfig:
    """Configuración del sistema de logging"""

    log_level: str = "INFO"
    log_file_pattern: str = "csv_processor_%Y%m%d.log"
    log_max_size_mb: int = 10
    log_backup_count: int = 5
    console_logging: bool = True


@dataclass
class NotificationConfig:
    """Configuración de notificaciones"""

    enable_email_notifications: bool = False
    email_host: str = ""
    email_port: int = 587
    email_user: str = ""
    email_password: str = ""
    email_recipients: list = field(default_factory=list)
    enable_slack_notifications: bool = False
    slack_webhook_url: str = ""


class ConfigManager:
    """
    Gestor central de configuración del sistema

    Maneja la carga de variables de entorno, archivos de configuración JSON
    y proporciona acceso centralizado a toda la configuración del sistema.
    """

    def __init__(
        self,
        env_file: Optional[str] = None,
        config_dir: Optional[Union[str, Path]] = None,
    ):
        """
        Inicializa el gestor de configuración

        Args:
            env_file: Ruta al archivo .env (opcional)
            config_dir: Directorio de configuración (por defecto: config/)
        """
        self.logger = logging.getLogger(__name__)
        self.config_dir = Path(config_dir) if config_dir else Path("config")

        # Cargar variables de entorno
        self._load_environment_variables(env_file)

        # Inicializar configuraciones
        self.paths = self._load_path_config()
        self.processing = self._load_processing_config()
        self.validation = self._load_validation_config()
        self.logging_config = self._load_logging_config()
        self.notifications = self._load_notification_config()

        # Cargar reglas de procesamiento desde JSON
        self.processing_rules = self._load_processing_rules()

        # Validar configuración
        self._validate_configuration()

        self.logger.info("Configuración cargada exitosamente")

    def _load_environment_variables(self, env_file: Optional[str] = None) -> None:
        """Carga las variables de entorno"""
        try:
            if env_file:
                env_path = Path(env_file)
            else:
                # Buscar .env en el directorio actual o en config/
                env_path = Path(".env")
                if not env_path.exists():
                    env_path = self.config_dir / ".env"

            if env_path.exists():
                load_dotenv(env_path)
                self.logger.info(f"Variables de entorno cargadas desde: {env_path}")
            else:
                self.logger.warning(
                    "No se encontró archivo .env, usando valores por defecto"
                )

        except Exception as e:
            self.logger.error(f"Error al cargar variables de entorno: {e}")
            raise ConfigurationError(f"Error cargando variables de entorno: {e}")

    def _load_path_config(self) -> PathConfig:
        """Carga la configuración de rutas"""
        return PathConfig(
            input_directory=Path(os.getenv("INPUT_DIRECTORY", "data/input")),
            output_directory=Path(os.getenv("OUTPUT_DIRECTORY", "data/output")),
            temp_directory=Path(os.getenv("TEMP_DIRECTORY", "data/temp")),
            log_directory=Path(os.getenv("LOG_DIRECTORY", "logs")),
        )

    def _load_processing_config(self) -> ProcessingConfig:
        """Carga la configuración de procesamiento"""
        return ProcessingConfig(
            max_file_size_mb=int(os.getenv("MAX_FILE_SIZE_MB", "100")),
            batch_size=int(os.getenv("BATCH_SIZE", "1000")),
            default_encoding=os.getenv("DEFAULT_ENCODING", "utf-8"),
            default_delimiter=os.getenv("DEFAULT_DELIMITER", ","),
            cpu_cores=int(os.getenv("CPU_CORES", "0")),
            memory_limit_gb=float(os.getenv("MEMORY_LIMIT_GB", "2.0")),
        )

    def _load_validation_config(self) -> ValidationConfig:
        """Carga la configuración de validación"""
        return ValidationConfig(
            max_validation_errors=int(os.getenv("MAX_VALIDATION_ERRORS", "50")),
            strict_validation=os.getenv("STRICT_VALIDATION", "false").lower() == "true",
            min_quality_score=float(os.getenv("MIN_QUALITY_SCORE", "0.8")),
            max_missing_percentage=float(os.getenv("MAX_MISSING_PERCENTAGE", "10.0")),
            max_duplicate_percentage=float(
                os.getenv("MAX_DUPLICATE_PERCENTAGE", "5.0")
            ),
        )

    def _load_logging_config(self) -> LoggingConfig:
        """Carga la configuración de logging"""
        return LoggingConfig(
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            log_file_pattern=os.getenv("LOG_FILE_PATTERN", "csv_processor_%Y%m%d.log"),
            log_max_size_mb=int(os.getenv("LOG_MAX_SIZE_MB", "10")),
            log_backup_count=int(os.getenv("LOG_BACKUP_COUNT", "5")),
            console_logging=os.getenv("CONSOLE_LOGGING", "true").lower() == "true",
        )

    def _load_notification_config(self) -> NotificationConfig:
        """Carga la configuración de notificaciones"""
        email_recipients = os.getenv("EMAIL_RECIPIENTS", "")
        recipients_list = [
            email.strip() for email in email_recipients.split(",") if email.strip()
        ]

        return NotificationConfig(
            enable_email_notifications=os.getenv(
                "ENABLE_EMAIL_NOTIFICATIONS", "false"
            ).lower()
            == "true",
            email_host=os.getenv("EMAIL_HOST", ""),
            email_port=int(os.getenv("EMAIL_PORT", "587")),
            email_user=os.getenv("EMAIL_USER", ""),
            email_password=os.getenv("EMAIL_PASSWORD", ""),
            email_recipients=recipients_list,
            enable_slack_notifications=os.getenv(
                "ENABLE_SLACK_NOTIFICATIONS", "false"
            ).lower()
            == "true",
            slack_webhook_url=os.getenv("SLACK_WEBHOOK_URL", ""),
        )

    def _load_processing_rules(self) -> Dict[str, Any]:
        """Carga las reglas de procesamiento desde archivo JSON"""
        try:
            rules_file = self.config_dir / "processing_rules.json"
            if rules_file.exists():
                with open(rules_file, "r", encoding="utf-8") as f:
                    rules = json.load(f)
                self.logger.info(
                    f"Reglas de procesamiento cargadas desde: {rules_file}"
                )
                return rules
            else:
                self.logger.warning(
                    "No se encontró processing_rules.json, usando reglas por defecto"
                )
                return self._get_default_processing_rules()

        except json.JSONDecodeError as e:
            self.logger.error(f"Error al parsear processing_rules.json: {e}")
            return self._get_default_processing_rules()
        except Exception as e:
            self.logger.error(f"Error al cargar reglas de procesamiento: {e}")
            return self._get_default_processing_rules()

    def _get_default_processing_rules(self) -> Dict[str, Any]:
        """Retorna reglas de procesamiento por defecto"""
        return {
            "processing_rules": {
                "data_types": {"auto_detect": True},
                "cleaning_rules": {
                    "remove_duplicates": True,
                    "handle_missing_values": {"strategy": "smart"},
                },
                "validation_rules": {"min_rows": 1, "max_missing_percentage": 25},
            },
            "output_rules": {
                "formats": {"csv": {"separator": ",", "encoding": "utf-8"}}
            },
        }

    def _validate_configuration(self) -> None:
        """Valida que la configuración sea correcta"""
        try:
            # Validar directorios
            self._ensure_directories_exist()

            # Validar valores numéricos
            if self.processing.max_file_size_mb <= 0:
                raise ConfigurationError("MAX_FILE_SIZE_MB debe ser mayor a 0")

            if self.processing.batch_size <= 0:
                raise ConfigurationError("BATCH_SIZE debe ser mayor a 0")

            if not 0 <= self.validation.min_quality_score <= 1:
                raise ConfigurationError("MIN_QUALITY_SCORE debe estar entre 0 y 1")

            # Validar configuración de email si está habilitada
            if self.notifications.enable_email_notifications:
                if not self.notifications.email_host:
                    raise ConfigurationError(
                        "EMAIL_HOST requerido cuando email notifications está habilitado"
                    )
                if not self.notifications.email_user:
                    raise ConfigurationError(
                        "EMAIL_USER requerido cuando email notifications está habilitado"
                    )

            self.logger.info("Configuración validada exitosamente")

        except Exception as e:
            self.logger.error(f"Error en validación de configuración: {e}")
            raise

    def _ensure_directories_exist(self) -> None:
        """Asegura que los directorios necesarios existan"""
        directories = [
            self.paths.input_directory,
            self.paths.output_directory,
            self.paths.temp_directory,
            self.paths.log_directory,
        ]

        for directory in directories:
            try:
                directory.mkdir(parents=True, exist_ok=True)
                self.logger.debug(f"Directorio asegurado: {directory}")
            except Exception as e:
                raise ConfigurationError(
                    f"No se pudo crear directorio {directory}: {e}"
                )

    def get_config_summary(self) -> Dict[str, Any]:
        """Retorna un resumen de la configuración actual"""
        return {
            "paths": {
                "input_directory": str(self.paths.input_directory),
                "output_directory": str(self.paths.output_directory),
                "temp_directory": str(self.paths.temp_directory),
                "log_directory": str(self.paths.log_directory),
            },
            "processing": {
                "max_file_size_mb": self.processing.max_file_size_mb,
                "batch_size": self.processing.batch_size,
                "default_encoding": self.processing.default_encoding,
                "cpu_cores": self.processing.cpu_cores,
            },
            "validation": {
                "strict_validation": self.validation.strict_validation,
                "min_quality_score": self.validation.min_quality_score,
                "max_missing_percentage": self.validation.max_missing_percentage,
            },
            "logging": {
                "log_level": self.logging_config.log_level,
                "console_logging": self.logging_config.console_logging,
            },
            "notifications": {
                "email_enabled": self.notifications.enable_email_notifications,
                "slack_enabled": self.notifications.enable_slack_notifications,
            },
        }

    def update_config(self, section: str, key: str, value: Any) -> None:
        """
        Actualiza un valor de configuración dinámicamente

        Args:
            section: Sección de configuración (paths, processing, validation, etc.)
            key: Clave a actualizar
            value: Nuevo valor
        """
        try:
            config_section = getattr(self, section, None)
            if config_section is None:
                raise ValueError(f"Sección de configuración '{section}' no encontrada")

            if hasattr(config_section, key):
                old_value = getattr(config_section, key)
                setattr(config_section, key, value)
                self.logger.info(
                    f"Configuración actualizada: {section}.{key} = {value} (anterior: {old_value})"
                )
            else:
                raise ValueError(f"Clave '{key}' no encontrada en sección '{section}'")

        except Exception as e:
            self.logger.error(f"Error al actualizar configuración: {e}")
            raise


class ConfigurationError(Exception):
    """Excepción personalizada para errores de configuración"""

    pass


# === FUNCIONES DE UTILIDAD ===


def setup_logging(config_manager: ConfigManager) -> logging.Logger:
    """
    Configura el sistema de logging basado en la configuración

    Args:
        config_manager: Instancia del gestor de configuración

    Returns:
        Logger configurado
    """
    log_config = config_manager.logging_config
    log_dir = config_manager.paths.log_directory

    # Crear directorio de logs si no existe
    log_dir.mkdir(parents=True, exist_ok=True)

    # Configurar el logger principal
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_config.log_level.upper()))

    # Limpiar handlers existentes
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Configurar formato
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Handler para consola
    if log_config.console_logging:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, log_config.log_level.upper()))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # Handler para archivo con rotación
    from logging.handlers import RotatingFileHandler
    from datetime import datetime

    log_file = log_dir / datetime.now().strftime(log_config.log_file_pattern)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=log_config.log_max_size_mb * 1024 * 1024,
        backupCount=log_config.log_backup_count,
    )
    file_handler.setLevel(getattr(logging, log_config.log_level.upper()))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info("Sistema de logging configurado correctamente")
    return logger


if __name__ == "__main__":
    # Ejemplo de uso del ConfigManager
    try:
        config = ConfigManager()
        print("=== RESUMEN DE CONFIGURACIÓN ===")
        import pprint

        pprint.pprint(config.get_config_summary())

    except Exception as e:
        print(f"Error al inicializar configuración: {e}")
