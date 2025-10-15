#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 CSV Processor - Procesamiento Avanzado de Archivos CSV

Este módulo maneja todo el procesamiento de archivos CSV, incluyendo:
- Detección automática de encoding y delimitadores
- Limpieza y transformación de datos
- Procesamiento por lotes para archivos grandes
- Generación de reportes de calidad

Autor: Angel Baez
Fecha: Octubre 2025
Proyecto: Data + Automation Engineer Journey - Semana 3
"""

import logging
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple, Any
from datetime import datetime
import chardet
import csv
import io
import json
from dataclasses import dataclass, field

from .config_manager import ConfigManager


def convert_numpy_types(obj):
    """Convierte tipos numpy a tipos nativos de Python para serialización JSON"""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_numpy_types(item) for item in obj]
    else:
        return obj


@dataclass
class ProcessingStats:
    """Estadísticas del procesamiento de datos"""

    original_rows: int = 0
    final_rows: int = 0
    original_columns: int = 0
    final_columns: int = 0
    duplicates_removed: int = 0
    missing_values_filled: int = 0
    invalid_rows_removed: int = 0
    processing_time_seconds: float = 0.0
    memory_usage_mb: float = 0.0
    quality_score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convierte las estadísticas a diccionario"""
        return {
            "original_rows": self.original_rows,
            "final_rows": self.final_rows,
            "rows_removed": self.original_rows - self.final_rows,
            "original_columns": self.original_columns,
            "final_columns": self.final_columns,
            "duplicates_removed": self.duplicates_removed,
            "missing_values_filled": self.missing_values_filled,
            "invalid_rows_removed": self.invalid_rows_removed,
            "processing_time_seconds": round(self.processing_time_seconds, 2),
            "memory_usage_mb": round(self.memory_usage_mb, 2),
            "quality_score": round(self.quality_score, 4),
            "data_reduction_percentage": (
                round(
                    ((self.original_rows - self.final_rows) / self.original_rows * 100),
                    2,
                )
                if self.original_rows > 0
                else 0
            ),
        }


@dataclass
class CSVMetadata:
    """Metadatos del archivo CSV procesado"""

    filename: str = ""
    file_size_mb: float = 0.0
    encoding: str = "utf-8"
    delimiter: str = ","
    detected_encoding: str = ""
    detected_delimiter: str = ""
    has_header: bool = True
    column_names: List[str] = field(default_factory=list)
    data_types: Dict[str, str] = field(default_factory=dict)
    processing_timestamp: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convierte los metadatos a diccionario"""
        return {
            "filename": self.filename,
            "file_size_mb": round(self.file_size_mb, 2),
            "encoding": self.encoding,
            "delimiter": self.delimiter,
            "detected_encoding": self.detected_encoding,
            "detected_delimiter": self.detected_delimiter,
            "has_header": self.has_header,
            "column_names": self.column_names,
            "data_types": self.data_types,
            "processing_timestamp": self.processing_timestamp,
        }


class CSVProcessor:
    """
    Procesador avanzado de archivos CSV

    Proporciona funcionalidades completas para el procesamiento de archivos CSV,
    incluyendo detección automática, limpieza, transformación y validación.
    """

    def __init__(self, config_manager: ConfigManager):
        """
        Inicializa el procesador CSV

        Args:
            config_manager: Instancia del gestor de configuración
        """
        self.config = config_manager
        self.logger = logging.getLogger(__name__)
        self.processing_rules = config_manager.processing_rules.get(
            "processing_rules", {}
        )
        self.output_rules = config_manager.processing_rules.get("output_rules", {})

        self.logger.info("CSVProcessor inicializado correctamente")

    def process_file(
        self,
        input_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None,
        profile: str = "default",
    ) -> Tuple[pd.DataFrame, ProcessingStats, CSVMetadata]:
        """
        Procesa un archivo CSV completo

        Args:
            input_path: Ruta del archivo CSV de entrada
            output_path: Ruta del archivo de salida (opcional)
            profile: Perfil de procesamiento a usar

        Returns:
            Tuple con el DataFrame procesado, estadísticas y metadatos
        """
        start_time = datetime.now()
        input_path = Path(input_path)

        self.logger.info(f"Iniciando procesamiento de: {input_path}")

        # Validar archivo de entrada
        self._validate_input_file(input_path)

        # Detectar características del archivo
        metadata = self._analyze_file(input_path)

        # Cargar datos
        df_original = self._load_csv(input_path, metadata)

        # Inicializar estadísticas
        stats = ProcessingStats(
            original_rows=len(df_original), original_columns=len(df_original.columns)
        )

        # Aplicar reglas de procesamiento según perfil
        df_processed = self._apply_processing_pipeline(df_original, stats, profile)

        # Calcular estadísticas finales
        stats.final_rows = len(df_processed)
        stats.final_columns = len(df_processed.columns)
        stats.processing_time_seconds = (datetime.now() - start_time).total_seconds()
        stats.memory_usage_mb = df_processed.memory_usage(deep=True).sum() / 1024 / 1024
        stats.quality_score = self._calculate_quality_score(df_processed)

        # Actualizar metadatos
        metadata.column_names = df_processed.columns.tolist()
        metadata.data_types = df_processed.dtypes.astype(str).to_dict()
        metadata.processing_timestamp = datetime.now().isoformat()

        # Guardar resultado si se especifica ruta de salida
        if output_path:
            output_path = Path(output_path)
            self._save_processed_data(df_processed, output_path, metadata, stats)

        self.logger.info(
            f"Procesamiento completado en {stats.processing_time_seconds:.2f}s"
        )
        return df_processed, stats, metadata

    def _validate_input_file(self, file_path: Path) -> None:
        """Valida que el archivo de entrada sea válido"""
        if not file_path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")

        if not file_path.is_file():
            raise ValueError(f"La ruta no es un archivo válido: {file_path}")

        # Verificar tamaño del archivo
        file_size_mb = file_path.stat().st_size / 1024 / 1024
        if file_size_mb > self.config.processing.max_file_size_mb:
            raise ValueError(
                f"Archivo demasiado grande: {file_size_mb:.2f}MB > {self.config.processing.max_file_size_mb}MB"
            )

        # Verificar extensión
        if file_path.suffix.lower() not in [".csv", ".txt"]:
            self.logger.warning(f"Extensión de archivo inusual: {file_path.suffix}")

    def _analyze_file(self, file_path: Path) -> CSVMetadata:
        """Analiza el archivo CSV para detectar sus características"""
        metadata = CSVMetadata()
        metadata.filename = file_path.name
        metadata.file_size_mb = file_path.stat().st_size / 1024 / 1024

        # Detectar encoding
        with open(file_path, "rb") as f:
            raw_data = f.read(10000)  # Leer primeros 10KB
            encoding_result = chardet.detect(raw_data)
            metadata.detected_encoding = encoding_result["encoding"] or "utf-8"
            metadata.encoding = metadata.detected_encoding

        # Detectar delimitador
        with open(file_path, "r", encoding=metadata.encoding, errors="ignore") as f:
            sample = f.read(5000)  # Leer muestra para detección
            sniffer = csv.Sniffer()
            try:
                dialect = sniffer.sniff(sample, delimiters=",;\t|")
                metadata.detected_delimiter = dialect.delimiter
                metadata.delimiter = metadata.detected_delimiter
                metadata.has_header = sniffer.has_header(sample)
            except csv.Error:
                # Usar valores por defecto si la detección falla
                metadata.delimiter = self.config.processing.default_delimiter
                metadata.detected_delimiter = metadata.delimiter
                metadata.has_header = True

        self.logger.info(
            f"Archivo analizado - Encoding: {metadata.encoding}, Delimitador: '{metadata.delimiter}'"
        )
        return metadata

    def _load_csv(self, file_path: Path, metadata: CSVMetadata) -> pd.DataFrame:
        """Carga el archivo CSV usando los parámetros detectados"""
        try:
            # Parámetros de carga
            load_params = {
                "filepath_or_buffer": file_path,
                "encoding": metadata.encoding,
                "delimiter": metadata.delimiter,
                "header": 0 if metadata.has_header else None,
                "low_memory": False,  # Para mejor detección de tipos
                "na_values": ["", "NULL", "null", "None", "N/A", "n/a", "#N/A"],
                "keep_default_na": True,
            }

            # Cargar en chunks si el archivo es muy grande
            if metadata.file_size_mb > 50:  # Para archivos > 50MB
                self.logger.info("Archivo grande detectado, cargando en chunks")
                chunks = []
                chunk_size = self.config.processing.batch_size

                for chunk in pd.read_csv(chunksize=chunk_size, **load_params):
                    chunks.append(chunk)
                    if len(chunks) % 10 == 0:  # Log cada 10 chunks
                        self.logger.info(
                            f"Cargados {len(chunks) * chunk_size} registros..."
                        )

                df = pd.concat(chunks, ignore_index=True)
            else:
                df = pd.read_csv(**load_params)

            self.logger.info(
                f"CSV cargado: {len(df)} filas, {len(df.columns)} columnas"
            )
            return df

        except UnicodeDecodeError:
            # Intentar con encoding alternativo
            self.logger.warning(
                f"Error de encoding con {metadata.encoding}, intentando con latin-1"
            )
            metadata.encoding = "latin-1"
            load_params["encoding"] = "latin-1"
            return pd.read_csv(**load_params)

        except Exception as e:
            self.logger.error(f"Error al cargar CSV: {e}")
            raise

    def _apply_processing_pipeline(
        self, df: pd.DataFrame, stats: ProcessingStats, profile: str
    ) -> pd.DataFrame:
        """Aplica el pipeline completo de procesamiento"""
        df_processed = df.copy()

        # 1. Limpieza inicial
        df_processed = self._clean_column_names(df_processed)

        # 2. Manejo de duplicados
        if self.processing_rules.get("cleaning_rules", {}).get(
            "remove_duplicates", True
        ):
            original_count = len(df_processed)
            df_processed = df_processed.drop_duplicates()
            stats.duplicates_removed = original_count - len(df_processed)

            if stats.duplicates_removed > 0:
                self.logger.info(
                    f"Eliminados {stats.duplicates_removed} registros duplicados"
                )

        # 3. Detección y conversión de tipos de datos
        df_processed = self._detect_and_convert_types(df_processed)

        # 4. Manejo de valores faltantes
        df_processed, filled_count = self._handle_missing_values(df_processed)
        stats.missing_values_filled = filled_count

        # 5. Limpieza de texto
        df_processed = self._clean_text_data(df_processed)

        # 6. Validación y filtrado
        df_processed, invalid_count = self._validate_and_filter_data(df_processed)
        stats.invalid_rows_removed = invalid_count

        return df_processed

    def _clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpia y normaliza los nombres de columnas"""
        if (
            self.processing_rules.get("transformation_rules", {})
            .get("normalize_names", {})
            .get("enabled", True)
        ):
            # Convertir a snake_case
            new_columns = []
            for col in df.columns:
                # Limpiar espacios y caracteres especiales
                clean_col = str(col).strip()
                clean_col = clean_col.replace(" ", "_").replace("-", "_")
                clean_col = "".join(c for c in clean_col if c.isalnum() or c == "_")
                clean_col = clean_col.lower()
                new_columns.append(clean_col)

            df.columns = new_columns
            self.logger.debug("Nombres de columnas normalizados")

        return df

    def _detect_and_convert_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Detecta y convierte tipos de datos automáticamente"""
        if not self.processing_rules.get("data_types", {}).get("auto_detect", True):
            return df

        for column in df.columns:
            try:
                # Intentar conversión a numérico
                if df[column].dtype == "object":
                    # Verificar si puede ser numérico
                    numeric_series = pd.to_numeric(df[column], errors="coerce")
                    non_null_ratio = numeric_series.notna().sum() / len(df[column])

                    if non_null_ratio > 0.8:  # Si >80% son números válidos
                        if numeric_series.apply(
                            lambda x: x == int(x) if pd.notna(x) else True
                        ).all():
                            df[column] = numeric_series.astype(
                                "Int64"
                            )  # Nullable integer
                        else:
                            df[column] = numeric_series.astype("float64")
                        continue

                    # Intentar conversión a datetime
                    try:
                        date_series = pd.to_datetime(df[column], errors="coerce")
                        date_ratio = date_series.notna().sum() / len(df[column])

                        if date_ratio > 0.8:  # Si >80% son fechas válidas
                            df[column] = date_series
                            continue
                    except:
                        pass

                    # Intentar conversión a boolean
                    if (
                        df[column]
                        .dropna()
                        .str.lower()
                        .isin(["true", "false", "1", "0", "yes", "no"])
                        .all()
                    ):
                        bool_map = {
                            "true": True,
                            "false": False,
                            "1": True,
                            "0": False,
                            "yes": True,
                            "no": False,
                        }
                        df[column] = df[column].str.lower().map(bool_map)
                        continue

            except Exception as e:
                self.logger.debug(f"No se pudo convertir columna {column}: {e}")
                continue

        self.logger.info("Detección y conversión de tipos completada")
        return df

    def _handle_missing_values(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, int]:
        """Maneja valores faltantes según la estrategia configurada"""
        missing_strategy = self.processing_rules.get("cleaning_rules", {}).get(
            "handle_missing_values", {}
        )
        strategy = missing_strategy.get("strategy", "smart")

        filled_count = 0

        if strategy == "smart":
            for column in df.columns:
                missing_count = df[column].isna().sum()
                if missing_count == 0:
                    continue

                if df[column].dtype in ["int64", "Int64", "float64"]:
                    # Para columnas numéricas, usar mediana
                    fill_value = df[column].median()
                    df[column] = df[column].fillna(fill_value)
                    filled_count += missing_count

                elif df[column].dtype == "object":
                    # Para columnas de texto, usar moda o valor más frecuente
                    mode_values = df[column].mode()
                    if len(mode_values) > 0:
                        df[column] = df[column].fillna(mode_values.iloc[0])
                        filled_count += missing_count

                elif "datetime" in str(df[column].dtype):
                    # Para fechas, usar forward fill
                    df[column] = df[column].ffill()
                    filled_count += missing_count

        if filled_count > 0:
            self.logger.info(f"Valores faltantes manejados: {filled_count}")

        return df, filled_count

    def _clean_text_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpia datos de texto"""
        text_rules = self.processing_rules.get("cleaning_rules", {}).get(
            "text_cleaning", {}
        )

        for column in df.select_dtypes(include=["object"]).columns:
            if text_rules.get("strip_whitespace", True):
                df[column] = df[column].astype(str).str.strip()

            if text_rules.get("normalize_case", False):
                df[column] = df[column].str.lower()

        return df

    def _validate_and_filter_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, int]:
        """Valida datos y filtra filas inválidas"""
        original_count = len(df)

        # Filtrar filas completamente vacías
        df = df.dropna(how="all")

        # Aplicar validaciones específicas según reglas
        validation_rules = self.processing_rules.get("validation_rules", {})

        # Validar número mínimo de filas
        min_rows = validation_rules.get("min_rows", 1)
        if len(df) < min_rows:
            raise ValueError(
                f"El archivo tiene menos filas que el mínimo requerido: {len(df)} < {min_rows}"
            )

        invalid_count = original_count - len(df)

        if invalid_count > 0:
            self.logger.info(f"Filas inválidas removidas: {invalid_count}")

        return df, invalid_count

    def _calculate_quality_score(self, df: pd.DataFrame) -> float:
        """Calcula una puntuación de calidad de los datos"""
        if len(df) == 0:
            return 0.0

        # Métricas de calidad
        completeness = df.count().sum() / (len(df) * len(df.columns))

        # Unicidad (promedio de unicidad por columna)
        uniqueness_scores = []
        for column in df.columns:
            unique_ratio = df[column].nunique() / len(df)
            uniqueness_scores.append(min(unique_ratio, 1.0))
        uniqueness = np.mean(uniqueness_scores) if uniqueness_scores else 1.0

        # Consistencia (basada en tipos de datos exitosos)
        consistency = 1.0  # Simplificado por ahora

        # Validez (filas sin valores nulos críticos)
        validity = 1.0 - (df.isnull().any(axis=1).sum() / len(df))

        # Puntuación ponderada
        quality_weights = self.config.processing_rules.get(
            "quality_metrics",
            {
                "completeness": {"weight": 0.3},
                "uniqueness": {"weight": 0.2},
                "consistency": {"weight": 0.25},
                "validity": {"weight": 0.25},
            },
        )

        w_completeness = quality_weights.get("completeness", {}).get("weight", 0.3)
        w_uniqueness = quality_weights.get("uniqueness", {}).get("weight", 0.2)
        w_consistency = quality_weights.get("consistency", {}).get("weight", 0.25)
        w_validity = quality_weights.get("validity", {}).get("weight", 0.25)

        quality_score = (
            completeness * w_completeness
            + uniqueness * w_uniqueness
            + consistency * w_consistency
            + validity * w_validity
        )

        return quality_score

    def _save_processed_data(
        self,
        df: pd.DataFrame,
        output_path: Path,
        metadata: CSVMetadata,
        stats: ProcessingStats,
    ) -> None:
        """Guarda los datos procesados con metadatos"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Determinar formato de salida
        if output_path.suffix.lower() == ".csv":
            self._save_as_csv(df, output_path)
        elif output_path.suffix.lower() in [".xlsx", ".xls"]:
            self._save_as_excel(df, output_path, metadata, stats)
        elif output_path.suffix.lower() == ".json":
            self._save_as_json(df, output_path)
        else:
            # Por defecto, guardar como CSV
            output_path = output_path.with_suffix(".csv")
            self._save_as_csv(df, output_path)

        # Guardar metadatos y estadísticas
        self._save_metadata(output_path, metadata, stats)

        self.logger.info(f"Datos procesados guardados en: {output_path}")

    def _save_as_csv(self, df: pd.DataFrame, output_path: Path) -> None:
        """Guarda DataFrame como CSV"""
        csv_rules = self.output_rules.get("formats", {}).get("csv", {})

        df.to_csv(
            output_path,
            sep=csv_rules.get("separator", ","),
            encoding=csv_rules.get("encoding", "utf-8"),
            index=csv_rules.get("include_index", False),
        )

    def _save_as_excel(
        self,
        df: pd.DataFrame,
        output_path: Path,
        metadata: CSVMetadata,
        stats: ProcessingStats,
    ) -> None:
        """Guarda DataFrame como Excel con múltiples hojas"""
        excel_rules = self.output_rules.get("formats", {}).get("excel", {})

        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            # Hoja de datos
            sheet_name = excel_rules.get("sheet_name", "ProcessedData")
            df.to_excel(
                writer,
                sheet_name=sheet_name,
                index=excel_rules.get("include_index", False),
            )

            # Hoja de metadatos
            metadata_df = pd.DataFrame([metadata.to_dict()]).T
            metadata_df.columns = ["Value"]
            metadata_df.to_excel(writer, sheet_name="Metadata")

            # Hoja de estadísticas
            stats_df = pd.DataFrame([stats.to_dict()]).T
            stats_df.columns = ["Value"]
            stats_df.to_excel(writer, sheet_name="Statistics")

    def _save_as_json(self, df: pd.DataFrame, output_path: Path) -> None:
        """Guarda DataFrame como JSON"""
        json_rules = self.output_rules.get("formats", {}).get("json", {})

        df.to_json(
            output_path,
            orient=json_rules.get("orient", "records"),
            indent=json_rules.get("indent", 2),
            date_format="iso",
        )

    def _save_metadata(
        self, output_path: Path, metadata: CSVMetadata, stats: ProcessingStats
    ) -> None:
        """Guarda metadatos y estadísticas en archivo JSON separado"""
        metadata_path = output_path.with_suffix(".metadata.json")

        combined_data = {
            "metadata": metadata.to_dict(),
            "statistics": stats.to_dict(),
            "processing_info": {
                "processor_version": "1.0.0",
                "config_profile": "default",
                "output_file": str(output_path),
            },
        }

        # Convertir tipos numpy a tipos JSON serializables
        combined_data = convert_numpy_types(combined_data)

        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(combined_data, f, indent=2, ensure_ascii=False)

    def get_processing_summary(
        self, stats: ProcessingStats, metadata: CSVMetadata
    ) -> str:
        """Genera un resumen legible del procesamiento"""
        return f"""
=== RESUMEN DE PROCESAMIENTO ===
Archivo: {metadata.filename}
Tamaño: {metadata.file_size_mb:.2f} MB
Encoding: {metadata.encoding}
Delimitador: '{metadata.delimiter}'

=== TRANSFORMACIONES ===
Filas: {stats.original_rows:,} → {stats.final_rows:,} ({stats.original_rows - stats.final_rows:+,})
Columnas: {stats.original_columns} → {stats.final_columns}
Duplicados eliminados: {stats.duplicates_removed:,}
Valores faltantes completados: {stats.missing_values_filled:,}

=== MÉTRICAS DE CALIDAD ===
Puntuación de calidad: {stats.quality_score:.2%}
Tiempo de procesamiento: {stats.processing_time_seconds:.2f}s
Uso de memoria: {stats.memory_usage_mb:.2f} MB

=== ESTADO ===
✅ Procesamiento completado exitosamente
"""


if __name__ == "__main__":
    # Ejemplo de uso del CSVProcessor
    from .config_manager import ConfigManager, setup_logging

    # Inicializar configuración
    config = ConfigManager()
    setup_logging(config)

    # Crear procesador
    processor = CSVProcessor(config)

    print("CSVProcessor inicializado correctamente")
    print("Listo para procesar archivos CSV")
