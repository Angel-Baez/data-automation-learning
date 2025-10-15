#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Aplicación Principal - Sistema de Procesamiento CSV

Este es el punto de entrada principal para la aplicación de procesamiento CSV, proporcionando:
- Interfaz de línea de comandos para procesamiento por lotes
- Menú interactivo para procesamiento guiado
- Integración de todos los módulos del sistema
- Manejo completo de errores y logging
- Reporte de progreso y estadísticas

Autor: Angel Baez
Fecha: Octubre 2025
Proyecto: Data + Automation Engineer Journey - Semana 3
Versión: 1.0.0
"""

import sys
import argparse
from pathlib import Path
from typing import Optional, Dict, Any
import json

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.config_manager import ConfigManager
from src.csv_processor import CSVProcessor
from src.data_validator import DataValidator
from src.utils import setup_logging, validate_file_path, timing_context


def convert_numpy_types(obj):
    """
    Convierte tipos numpy a tipos Python nativos para serialización JSON

    Args:
        obj: Objeto que puede contener tipos numpy

    Returns:
        Objeto con tipos Python nativos
    """
    import numpy as np
    from dataclasses import is_dataclass, asdict

    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif is_dataclass(obj) and not isinstance(obj, type):
        return convert_numpy_types(asdict(obj))
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    else:
        return obj


class CSVProcessorApp:
    """
    Aplicación Principal de Procesamiento CSV

    Coordina todos los componentes del sistema y proporciona interfaces de usuario
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Inicializa la aplicación

        Args:
            config_path: Ruta al archivo de configuración
        """
        # Setup logging first
        self.logger = setup_logging(log_level="INFO", log_dir="logs")
        self.logger.info("=== Aplicación de Procesamiento CSV Iniciando ===")

        try:
            # Inicializar administrador de configuración
            self.config_manager = ConfigManager(config_path)
            self.logger.info("Administrador de configuración inicializado")

            # Inicializar componentes
            self.csv_processor = CSVProcessor(self.config_manager)
            self.data_validator = DataValidator(self.config_manager)

            self.logger.info("Todos los componentes inicializados exitosamente")

        except Exception as e:
            self.logger.error(f"Error al inicializar la aplicación: {e}")
            raise

    def process_single_file(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        processing_profile: str = "standard",
        validate: bool = True,
    ) -> Dict[str, Any]:
        """
        Procesar un archivo CSV individual

        Args:
            input_path: Ruta al archivo CSV de entrada
            output_path: Ruta del archivo de salida (opcional)
            processing_profile: Perfil de procesamiento a usar
            validate: Si ejecutar validación

        Returns:
            Diccionario con los resultados del procesamiento
        """
        try:
            input_path_obj = validate_file_path(input_path)

            self.logger.info(f"Procesando archivo: {input_path}")
            self.logger.info(f"Perfil de procesamiento: {processing_profile}")

            results = {}

            with timing_context("Procesamiento de archivo"):
                # Usar el método principal del CSV processor que maneja todo
                if output_path:
                    processed_df, processing_stats, metadata = (
                        self.csv_processor.process_file(
                            input_path=input_path,
                            output_path=Path(output_path),
                            profile=processing_profile,
                        )
                    )
                    results["output_path"] = str(output_path)
                    results["metadata"] = metadata
                    results["processing_stats"] = processing_stats
                else:
                    # Si solo queremos procesar sin guardar, necesitamos usar los métodos internos
                    # Por ahora, usaremos un archivo temporal
                    import tempfile

                    with tempfile.NamedTemporaryFile(
                        suffix=".csv", delete=False
                    ) as tmp:
                        temp_path = Path(tmp.name)

                    try:
                        processed_df, processing_stats, metadata = (
                            self.csv_processor.process_file(
                                input_path=input_path,
                                output_path=temp_path,
                                profile=processing_profile,
                            )
                        )
                        results["output_path"] = str(temp_path)
                        results["metadata"] = metadata
                        results["processing_stats"] = processing_stats

                        # Leer el archivo procesado para validación si se solicita
                        if validate:
                            import pandas as pd

                            df = pd.read_csv(temp_path)
                            validation_report = self.data_validator.validate_dataframe(
                                df
                            )
                            results["validation"] = validation_report

                            if not validation_report.is_valid:
                                self.logger.warning(
                                    f"Problemas de validación encontrados: {validation_report.errors} errores, {validation_report.warnings} advertencias"
                                )
                            else:
                                self.logger.info("Validación de datos exitosa")
                    finally:
                        # Limpiar archivo temporal
                        if temp_path.exists():
                            temp_path.unlink()

                # Crear resumen
                summary = {
                    "archivo_entrada": str(input_path),
                    "archivo_salida": results.get("output_path"),
                    "perfil_procesamiento": processing_profile,
                    "filas_originales": processing_stats.original_rows,
                    "filas_procesadas": processing_stats.final_rows,
                    "validacion_exitosa": results.get(
                        "validation", type("", (), {"is_valid": True})
                    ).is_valid,
                    "puntuacion_calidad": processing_stats.quality_score,
                    "tiempo_procesamiento": processing_stats.processing_time_seconds,
                }
                results["summary"] = summary
                results["processing_success"] = True

                self.logger.info("Procesamiento de archivo completado exitosamente")
                return results

        except Exception as e:
            error_msg = f"Error procesando archivo {input_path}: {e}"
            self.logger.error(error_msg, exc_info=True)
            raise RuntimeError(error_msg) from e

    def batch_process(
        self,
        input_directory: str,
        output_directory: Optional[str] = None,
        pattern: str = "*.csv",
        validate: bool = True,
    ) -> Dict[str, Any]:
        """
        Procesar múltiples archivos CSV en lote

        Args:
            input_directory: Directorio que contiene archivos CSV
            output_directory: Directorio de salida (opcional)
            pattern: Patrón de archivos a coincidir
            validate: Si ejecutar validación

        Returns:
            Diccionario conteniendo resultados del procesamiento en lote
        """
        try:
            input_dir = Path(input_directory)
            if not input_dir.exists():
                raise FileNotFoundError(
                    f"Directorio de entrada no encontrado: {input_directory}"
                )

            # Encontrar archivos CSV
            csv_files = list(input_dir.glob(pattern))
            if not csv_files:
                raise ValueError(
                    f"No se encontraron archivos con patrón {pattern} en {input_directory}"
                )

            self.logger.info(f"Procesando {len(csv_files)} archivos CSV en lote")

            # Preparar directorio de salida si se especifica
            if output_directory:
                output_dir = Path(output_directory)
                output_dir.mkdir(parents=True, exist_ok=True)

            results = {
                "total_files": len(csv_files),
                "processed_files": [],
                "errors": [],
                "summary": {},
            }

            successful_processing = 0
            total_rows_processed = 0
            total_processing_time = 0

            for csv_file in csv_files:
                try:
                    # Generar ruta de salida
                    if output_directory:
                        output_path = (
                            Path(output_directory) / f"processed_{csv_file.name}"
                        )
                    else:
                        output_path = None

                    # Procesar archivo individual
                    file_result = self.process_single_file(
                        input_path=str(csv_file),
                        output_path=str(output_path) if output_path else None,
                        validate=validate,
                    )

                    results["processed_files"].append(
                        {
                            "input_file": str(csv_file),
                            "output_file": file_result.get("output_path"),
                            "success": True,
                            "summary": file_result["summary"],
                        }
                    )

                    successful_processing += 1
                    total_rows_processed += file_result["summary"]["filas_procesadas"]
                    total_processing_time += file_result["summary"][
                        "tiempo_procesamiento"
                    ]

                except Exception as e:
                    error_info = {
                        "input_file": str(csv_file),
                        "error": str(e),
                        "success": False,
                    }
                    results["errors"].append(error_info)
                    self.logger.error(f"Error procesando {csv_file}: {e}")

            # Crear resumen del lote
            results["summary"] = {
                "total_archivos": len(csv_files),
                "archivos_exitosos": successful_processing,
                "archivos_con_error": len(results["errors"]),
                "total_filas_procesadas": total_rows_processed,
                "tiempo_total_procesamiento": total_processing_time,
                "tasa_exito": successful_processing / len(csv_files) * 100,
            }

            self.logger.info(
                f"Procesamiento en lote completado: {successful_processing}/{len(csv_files)} archivos exitosos"
            )
            return results

        except Exception as e:
            error_msg = f"Error en procesamiento en lote: {e}"
            self.logger.error(error_msg, exc_info=True)
            raise RuntimeError(error_msg) from e

    def interactive_menu(self) -> None:
        """
        Mostrar menú interactivo para procesamiento guiado
        """
        while True:
            print("\n" + "=" * 60)
            print("🚀 SISTEMA DE PROCESAMIENTO CSV - MENÚ INTERACTIVO")
            print("=" * 60)
            print("1. Procesar archivo individual")
            print("2. Procesamiento en lote")
            print("3. Validar archivo CSV")
            print("4. Ver configuración actual")
            print("5. Salir")
            print("-" * 60)

            try:
                choice = input("Selecciona una opción (1-5): ").strip()

                if choice == "1":
                    self._interactive_single_file()
                elif choice == "2":
                    self._interactive_batch_process()
                elif choice == "3":
                    self._interactive_validate()
                elif choice == "4":
                    self._show_configuration()
                elif choice == "5":
                    print("¡Hasta luego! 👋")
                    break
                else:
                    print("❌ Opción inválida. Por favor selecciona 1-5.")

            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                self.logger.error(f"Error en menú interactivo: {e}")
                print(f"❌ Error: {e}")

    def _interactive_single_file(self) -> None:
        """Menú para procesamiento de archivo individual"""
        print("\n📄 PROCESAMIENTO DE ARCHIVO INDIVIDUAL")
        print("-" * 40)

        # Obtener ruta de entrada
        input_path = input("Ruta del archivo CSV de entrada: ").strip()
        if not input_path:
            print("❌ Se requiere una ruta de entrada.")
            return

        # Obtener ruta de salida (opcional)
        output_path = input(
            "Ruta del archivo de salida (opcional, presiona Enter para omitir): "
        ).strip()
        if not output_path:
            output_path = None

        # Seleccionar perfil de procesamiento
        print("\nPerfiles de procesamiento disponibles:")
        print("1. standard - Procesamiento estándar")
        print("2. strict - Procesamiento estricto con validaciones extra")
        print("3. lenient - Procesamiento permisivo")

        profile_choice = input("Selecciona perfil (1-3, default: 1): ").strip()
        profile_map = {"1": "standard", "2": "strict", "3": "lenient"}
        profile = profile_map.get(profile_choice, "standard")

        # Opción de validación
        validate_input = (
            input("¿Ejecutar validación de datos? (s/n, default: s): ").strip().lower()
        )
        validate = validate_input != "n"

        try:
            print(f"\n🔄 Procesando archivo: {input_path}")

            # Procesar archivo
            results = self.process_single_file(
                input_path=input_path,
                output_path=output_path,
                processing_profile=profile,
                validate=validate,
            )

            # Mostrar resultados
            print("\n✅ PROCESAMIENTO COMPLETADO")
            print("-" * 30)
            summary = results["summary"]
            print(f"📁 Archivo entrada: {summary['archivo_entrada']}")
            if summary["archivo_salida"]:
                print(f"📁 Archivo salida: {summary['archivo_salida']}")
            print(f"📊 Filas originales: {summary['filas_originales']}")
            print(f"📊 Filas procesadas: {summary['filas_procesadas']}")
            print(f"⭐ Puntuación calidad: {summary['puntuacion_calidad']:.2f}/10")
            print(f"⏱️ Tiempo procesamiento: {summary['tiempo_procesamiento']:.2f}s")

            if validate and "validation" in results:
                validation = results["validation"]
                if validation.is_valid:
                    print("✅ Validación: EXITOSA")
                else:
                    print(
                        f"⚠️ Validación: {validation.errors} errores, {validation.warnings} advertencias"
                    )

        except Exception as e:
            print(f"❌ Error: {e}")

    def _interactive_batch_process(self) -> None:
        """Menú para procesamiento en lote"""
        print("\n🗂️ PROCESAMIENTO EN LOTE")
        print("-" * 25)

        # Obtener directorio de entrada
        input_dir = input("Directorio con archivos CSV: ").strip()
        if not input_dir:
            print("❌ Se requiere un directorio de entrada.")
            return

        # Obtener directorio de salida (opcional)
        output_dir = input(
            "Directorio de salida (opcional, presiona Enter para omitir): "
        ).strip()
        if not output_dir:
            output_dir = None

        # Patrón de archivos
        pattern = input("Patrón de archivos (default: *.csv): ").strip()
        if not pattern:
            pattern = "*.csv"

        # Opción de validación
        validate_input = (
            input("¿Ejecutar validación de datos? (s/n, default: s): ").strip().lower()
        )
        validate = validate_input != "n"

        try:
            print(f"\n🔄 Procesando archivos en: {input_dir}")

            # Procesar en lote
            results = self.batch_process(
                input_directory=input_dir,
                output_directory=output_dir,
                pattern=pattern,
                validate=validate,
            )

            # Mostrar resultados
            print("\n✅ PROCESAMIENTO EN LOTE COMPLETADO")
            print("-" * 35)
            summary = results["summary"]
            print(f"📁 Total archivos: {summary['total_archivos']}")
            print(f"✅ Archivos exitosos: {summary['archivos_exitosos']}")
            print(f"❌ Archivos con error: {summary['archivos_con_error']}")
            print(f"📊 Total filas procesadas: {summary['total_filas_procesadas']}")
            print(f"⏱️ Tiempo total: {summary['tiempo_total_procesamiento']:.2f}s")
            print(f"📈 Tasa de éxito: {summary['tasa_exito']:.1f}%")

            if results["errors"]:
                print(f"\n⚠️ Errores encontrados:")
                for error in results["errors"][:5]:  # Mostrar solo los primeros 5
                    print(f"  • {error['input_file']}: {error['error']}")
                if len(results["errors"]) > 5:
                    print(f"  ... y {len(results['errors']) - 5} errores más")

        except Exception as e:
            print(f"❌ Error: {e}")

    def _interactive_validate(self) -> None:
        """Menú para validación de archivos"""
        print("\n✅ VALIDACIÓN DE ARCHIVO CSV")
        print("-" * 30)

        # Obtener ruta de archivo
        input_path = input("Ruta del archivo CSV a validar: ").strip()
        if not input_path:
            print("❌ Se requiere una ruta de archivo.")
            return

        try:
            import pandas as pd

            print(f"\n🔍 Validando archivo: {input_path}")

            # Leer archivo
            df = pd.read_csv(input_path)

            # Ejecutar validación
            validation_report = self.data_validator.validate_dataframe(df)

            # Mostrar resultados
            print("\n📋 REPORTE DE VALIDACIÓN")
            print("-" * 25)
            print(f"📊 Total filas: {len(df)}")
            print(f"📊 Total columnas: {len(df.columns)}")

            if validation_report.is_valid:
                print("✅ Estado: VÁLIDO")
            else:
                print("❌ Estado: INVÁLIDO")
                print(f"🚨 Errores: {validation_report.errors}")
                print(f"⚠️ Advertencias: {validation_report.warnings}")

            # Mostrar detalles si hay problemas
            if hasattr(validation_report, "results") and validation_report.results:
                print("\n📝 Detalles:")
                for result in validation_report.results[
                    :10
                ]:  # Mostrar solo los primeros 10
                    print(f"  • {result.message}")
                if len(validation_report.results) > 10:
                    print(f"  ... y {len(validation_report.results) - 10} detalles más")

        except Exception as e:
            print(f"❌ Error: {e}")

    def _show_configuration(self) -> None:
        """Mostrar configuración actual"""
        print("\n⚙️ CONFIGURACIÓN ACTUAL")
        print("-" * 25)

        try:
            config = self.config_manager.get_config_summary()

            print(f"📁 Directorio configuración: {self.config_manager.config_dir}")
            print("\n📋 Configuraciones:")

            for section, settings in config.items():
                print(f"\n[{section}]")
                if isinstance(settings, dict):
                    for key, value in settings.items():
                        print(f"  {key}: {value}")
                else:
                    print(f"  {settings}")

        except Exception as e:
            print(f"❌ Error mostrando configuración: {e}")


def setup_cli_parser() -> argparse.ArgumentParser:
    """
    Configurar parser de argumentos de línea de comandos

    Returns:
        Parser configurado
    """
    parser = argparse.ArgumentParser(
        description="🚀 Sistema de Procesamiento CSV - Herramienta profesional para procesar y validar archivos CSV",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  %(prog)s --interactive                                    # Menú interactivo
  %(prog)s single -i datos.csv -o datos_limpio.csv         # Procesar archivo individual
  %(prog)s batch -i ./datos/ -o ./procesados/              # Procesamiento en lote
  %(prog)s validate -i datos.csv                           # Validar archivo CSV
        """,
    )

    # Comando principal
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponibles")

    # Comando para archivo individual
    single_parser = subparsers.add_parser("single", help="Procesar archivo individual")
    single_parser.add_argument(
        "-i", "--input", required=True, help="Archivo CSV de entrada"
    )
    single_parser.add_argument(
        "-o", "--output", help="Archivo CSV de salida (opcional)"
    )
    single_parser.add_argument(
        "-p",
        "--profile",
        default="standard",
        choices=["standard", "strict", "lenient"],
        help="Perfil de procesamiento (default: standard)",
    )
    single_parser.add_argument(
        "--no-validate", action="store_true", help="Omitir validación de datos"
    )
    single_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Salida detallada"
    )

    # Comando para procesamiento en lote
    batch_parser = subparsers.add_parser("batch", help="Procesamiento en lote")
    batch_parser.add_argument(
        "-i", "--input-dir", required=True, help="Directorio con archivos CSV"
    )
    batch_parser.add_argument(
        "-o", "--output-dir", help="Directorio de salida (opcional)"
    )
    batch_parser.add_argument(
        "--pattern", default="*.csv", help="Patrón de archivos (default: *.csv)"
    )
    batch_parser.add_argument(
        "--no-validate", action="store_true", help="Omitir validación de datos"
    )
    batch_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Salida detallada"
    )

    # Comando para validación
    validate_parser = subparsers.add_parser("validate", help="Validar archivo CSV")
    validate_parser.add_argument(
        "-i", "--input", required=True, help="Archivo CSV a validar"
    )
    validate_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Salida detallada"
    )

    # Opciones globales
    parser.add_argument(
        "--interactive", action="store_true", help="Iniciar menú interactivo"
    )
    parser.add_argument("--config", help="Archivo de configuración personalizado")
    parser.add_argument("--version", action="version", version="CSV Processor 1.0.0")

    return parser


def main():
    """
    Función principal - punto de entrada de la aplicación
    """
    try:
        # Configurar parser CLI
        parser = setup_cli_parser()
        args = parser.parse_args()

        # Si no hay argumentos, mostrar ayuda
        if len(sys.argv) == 1:
            parser.print_help()
            return

        # Inicializar aplicación
        app = CSVProcessorApp(config_path=args.config)

        # Menú interactivo
        if args.interactive:
            app.interactive_menu()
            return

        # Procesar comandos
        if args.command == "single":
            print(f"🔄 Procesando archivo: {args.input}")

            results = app.process_single_file(
                input_path=args.input,
                output_path=args.output,
                processing_profile=args.profile,
                validate=not args.no_validate,
            )

            print("✅ Procesamiento completado")

            if args.verbose:
                # Convertir tipos numpy para serialización JSON
                results_serializable = convert_numpy_types(results)
                print("\n📊 Resultados detallados:")
                print(json.dumps(results_serializable, indent=2, ensure_ascii=False))
            else:
                summary = results["summary"]
                print(
                    f"📊 Filas procesadas: {summary['filas_originales']} → {summary['filas_procesadas']}"
                )
                print(f"⭐ Puntuación calidad: {summary['puntuacion_calidad']:.2f}/10")
                if summary["archivo_salida"]:
                    print(f"📁 Archivo guardado: {summary['archivo_salida']}")

        elif args.command == "batch":
            print(f"🔄 Procesando directorio: {args.input_dir}")

            results = app.batch_process(
                input_directory=args.input_dir,
                output_directory=args.output_dir,
                pattern=args.pattern,
                validate=not args.no_validate,
            )

            print("✅ Procesamiento en lote completado")

            if args.verbose:
                print("\n📊 Resultados detallados:")
                print(json.dumps(results, indent=2, ensure_ascii=False))
            else:
                summary = results["summary"]
                print(
                    f"📊 Procesamiento: {summary['archivos_exitosos']}/{summary['total_archivos']} archivos"
                )
                print(f"📈 Tasa de éxito: {summary['tasa_exito']:.1f}%")
                print(f"📊 Total filas procesadas: {summary['total_filas_procesadas']}")

        elif args.command == "validate":
            print(f"🔍 Validando archivo: {args.input}")

            import pandas as pd

            df = pd.read_csv(args.input)
            validation_report = app.data_validator.validate_dataframe(df)

            if validation_report.is_valid:
                print("✅ Archivo válido")
            else:
                print(
                    f"❌ Archivo inválido: {validation_report.errors} errores, {validation_report.warnings} advertencias"
                )

            if args.verbose and hasattr(validation_report, "results"):
                print("\n📝 Detalles de validación:")
                for result in validation_report.results:
                    print(f"  • {result.message}")

        else:
            parser.print_help()

    except KeyboardInterrupt:
        print("\n👋 ¡Proceso interrumpido por el usuario!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
