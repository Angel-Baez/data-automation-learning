#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏭 Generador de Datos de Muestra - Sistema de Procesamiento CSV

Este script genera varios archivos CSV con diferentes características para testing:
- Datos limpios y bien formateados
- Datos con valores faltantes
- Datos con duplicados
- Datos con inconsistencias de tipo
- Datasets grandes para pruebas de rendimiento
- Datos corruptos para pruebas de manejo de errores

Autor: Angel Baez
Fecha: Octubre 2025
Proyecto: Data + Automation Engineer Journey - Semana 3
Versión: 1.0.0
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json
from pathlib import Path
import argparse


class SampleDataGenerator:
    """Genera archivos CSV de muestra para probar el sistema de procesamiento CSV"""

    def __init__(self, output_dir: str = "data/samples"):
        """
        Inicializa el generador de datos de muestra

        Args:
            output_dir: Directory to save sample files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Set random seeds for reproducibility
        np.random.seed(42)
        random.seed(42)

        self.departments = [
            "Engineering",
            "Sales",
            "Marketing",
            "HR",
            "Finance",
            "Operations",
        ]
        self.first_names = [
            "Alice",
            "Bob",
            "Charlie",
            "Diana",
            "Eve",
            "Frank",
            "Grace",
            "Henry",
            "Ivy",
            "Jack",
            "Kate",
            "Liam",
            "Maya",
            "Noah",
            "Olivia",
            "Peter",
            "Quinn",
            "Rachel",
            "Sam",
            "Tara",
            "Uma",
            "Victor",
            "Wendy",
            "Xander",
            "Yara",
            "Zoe",
            "Alex",
            "Blake",
            "Casey",
            "Drew",
        ]
        self.last_names = [
            "Smith",
            "Johnson",
            "Williams",
            "Brown",
            "Jones",
            "Garcia",
            "Miller",
            "Davis",
            "Rodriguez",
            "Martinez",
            "Hernandez",
            "Lopez",
            "Gonzalez",
            "Wilson",
            "Anderson",
            "Thomas",
            "Taylor",
            "Moore",
            "Jackson",
            "Martin",
            "Lee",
            "Perez",
            "Thompson",
            "White",
            "Harris",
            "Sanchez",
            "Clark",
        ]
        self.domains = [
            "company.com",
            "business.org",
            "enterprise.net",
            "corp.com",
            "firm.co",
        ]

    def generate_clean_data(
        self, rows: int = 1000, filename: str = "clean_data.csv"
    ) -> Path:
        """
        Generate clean, well-formatted CSV data

        Args:
            rows: Number of rows to generate
            filename: Output filename

        Returns:
            Path to generated file
        """
        data = {
            "employee_id": range(1, rows + 1),
            "first_name": [random.choice(self.first_names) for _ in range(rows)],
            "last_name": [random.choice(self.last_names) for _ in range(rows)],
            "email": [
                f"{random.choice(self.first_names).lower()}.{random.choice(self.last_names).lower()}@{random.choice(self.domains)}"
                for _ in range(rows)
            ],
            "age": np.random.randint(22, 65, rows),
            "salary": np.random.normal(65000, 20000, rows).round(2),
            "department": [random.choice(self.departments) for _ in range(rows)],
            "hire_date": [
                (datetime.now() - timedelta(days=random.randint(30, 3650))).strftime(
                    "%Y-%m-%d"
                )
                for _ in range(rows)
            ],
            "active": np.random.choice([True, False], rows, p=[0.85, 0.15]),
            "performance_score": np.random.uniform(1.0, 5.0, rows).round(1),
        }

        df = pd.DataFrame(data)
        file_path = self.output_dir / filename
        df.to_csv(file_path, index=False)

        print(f"Generated clean data: {file_path} ({rows} rows)")
        return file_path

    def generate_messy_data(
        self, rows: int = 800, filename: str = "messy_data.csv"
    ) -> Path:
        """
        Generate data with various quality issues

        Args:
            rows: Number of rows to generate
            filename: Output filename

        Returns:
            Path to generated file
        """
        # Start with clean data
        data = {
            "ID": list(range(1, rows + 1)),
            " First Name ": [random.choice(self.first_names) for _ in range(rows)],
            "Last-Name!": [random.choice(self.last_names) for _ in range(rows)],
            "EMAIL_ADDRESS": [
                f"{random.choice(self.first_names).lower()}.{random.choice(self.last_names).lower()}@{random.choice(self.domains)}"
                for _ in range(rows)
            ],
            "Age (Years)": np.random.randint(22, 65, rows),
            "Annual Salary $": np.random.normal(65000, 20000, rows).round(2),
            "Dept.": [random.choice(self.departments) for _ in range(rows)],
            "Start Date": [
                (datetime.now() - timedelta(days=random.randint(30, 3650))).strftime(
                    "%Y-%m-%d"
                )
                for _ in range(rows)
            ],
            "Is Active?": np.random.choice(
                ["Yes", "No", "TRUE", "FALSE", "1", "0"], rows
            ),
            "Score": np.random.uniform(1.0, 5.0, rows).round(1),
        }

        # Introduce missing values (10% of data)
        missing_indices = np.random.choice(rows, size=int(rows * 0.1), replace=False)
        for idx in missing_indices:
            if random.random() < 0.3:
                data[" First Name "][idx] = ""
            if random.random() < 0.2:
                data["EMAIL_ADDRESS"][idx] = None
            if random.random() < 0.15:
                data["Annual Salary $"][idx] = np.nan

        # Introduce duplicates (5% of rows)
        duplicate_count = int(rows * 0.05)
        duplicate_source_indices = np.random.choice(
            rows // 2, size=duplicate_count, replace=False
        )
        duplicate_target_indices = np.random.choice(
            range(rows // 2, rows), size=duplicate_count, replace=False
        )

        for src, tgt in zip(duplicate_source_indices, duplicate_target_indices):
            data["ID"][tgt] = data["ID"][src]
            data[" First Name "][tgt] = data[" First Name "][src]
            data["Last-Name!"][tgt] = data["Last-Name!"][src]
            data["EMAIL_ADDRESS"][tgt] = data["EMAIL_ADDRESS"][src]

        # Introduce invalid emails (3% of data)
        invalid_email_indices = np.random.choice(
            rows, size=int(rows * 0.03), replace=False
        )
        for idx in invalid_email_indices:
            if data["EMAIL_ADDRESS"][idx] is not None:
                data["EMAIL_ADDRESS"][idx] = "invalid.email"

        # Add extra whitespace and special characters
        for i in range(rows):
            if random.random() < 0.1:
                data[" First Name "][i] = f"  {data[' First Name '][i]}  "
            if random.random() < 0.1:
                data["Last-Name!"][i] = f"{data['Last-Name!'][i]}\t"

        df = pd.DataFrame(data)
        file_path = self.output_dir / filename
        df.to_csv(file_path, index=False)

        print(f"Generated messy data: {file_path} ({rows} rows)")
        return file_path

    def generate_large_dataset(
        self, rows: int = 50000, filename: str = "large_dataset.csv"
    ) -> Path:
        """
        Generate large dataset for performance testing

        Args:
            rows: Number of rows to generate
            filename: Output filename

        Returns:
            Path to generated file
        """
        print(f"Generating large dataset with {rows} rows...")

        # Generate in chunks to manage memory
        chunk_size = 10000
        chunks = []

        for chunk_start in range(0, rows, chunk_size):
            chunk_end = min(chunk_start + chunk_size, rows)
            chunk_rows = chunk_end - chunk_start

            chunk_data = {
                "transaction_id": range(chunk_start + 1, chunk_end + 1),
                "customer_id": np.random.randint(1, rows // 10, chunk_rows),
                "product_code": [
                    f"PROD_{random.randint(1000, 9999)}" for _ in range(chunk_rows)
                ],
                "quantity": np.random.randint(1, 20, chunk_rows),
                "unit_price": np.random.uniform(10.0, 500.0, chunk_rows).round(2),
                "discount": np.random.uniform(0.0, 0.3, chunk_rows).round(3),
                "total_amount": np.random.uniform(10.0, 2000.0, chunk_rows).round(2),
                "transaction_date": [
                    (datetime.now() - timedelta(days=random.randint(1, 365))).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    for _ in range(chunk_rows)
                ],
                "customer_segment": np.random.choice(
                    ["Premium", "Standard", "Basic"], chunk_rows
                ),
                "region": np.random.choice(
                    ["North", "South", "East", "West", "Central"], chunk_rows
                ),
            }

            chunks.append(pd.DataFrame(chunk_data))

            if len(chunks) % 5 == 0:  # Progress indicator
                print(f"  Generated {chunk_end} / {rows} rows...")

        df = pd.concat(chunks, ignore_index=True)
        file_path = self.output_dir / filename
        df.to_csv(file_path, index=False)

        print(f"Generated large dataset: {file_path} ({rows} rows)")
        return file_path

    def generate_mixed_types_data(
        self, rows: int = 500, filename: str = "mixed_types_data.csv"
    ) -> Path:
        """
        Generate data with mixed data types for type detection testing

        Args:
            rows: Number of rows to generate
            filename: Output filename

        Returns:
            Path to generated file
        """
        data = {
            "id_as_string": [str(i) for i in range(1, rows + 1)],
            "numeric_as_string": [
                str(random.uniform(10.0, 100.0)) for _ in range(rows)
            ],
            "boolean_as_string": [
                random.choice(["true", "false", "TRUE", "FALSE", "1", "0"])
                for _ in range(rows)
            ],
            "date_as_string": [
                (datetime.now() - timedelta(days=random.randint(1, 1000))).strftime(
                    "%Y-%m-%d"
                )
                for _ in range(rows)
            ],
            "percentage_as_string": [f"{random.randint(1, 100)}%" for _ in range(rows)],
            "currency_as_string": [
                f"${random.randint(1000, 10000)}" for _ in range(rows)
            ],
            "mixed_numeric": [
                random.choice(
                    [
                        str(random.randint(1, 1000)),
                        f"{random.uniform(1.0, 1000.0):.2f}",
                        f"{random.randint(1, 100)}%",
                        f"${random.randint(100, 1000)}",
                    ]
                )
                for _ in range(rows)
            ],
            "categorical_data": [
                random.choice(["A", "B", "C", "D", "E"]) for _ in range(rows)
            ],
            "free_text": [
                f"This is sample text entry {i} with some description"
                for i in range(1, rows + 1)
            ],
        }

        df = pd.DataFrame(data)
        file_path = self.output_dir / filename
        df.to_csv(file_path, index=False)

        print(f"Generated mixed types data: {file_path} ({rows} rows)")
        return file_path

    def generate_corrupted_data(
        self, rows: int = 200, filename: str = "corrupted_data.csv"
    ) -> Path:
        """
        Generate corrupted CSV data for error handling testing

        Args:
            rows: Number of rows to generate
            filename: Output filename

        Returns:
            Path to generated file
        """
        file_path = self.output_dir / filename

        with open(file_path, "w", encoding="utf-8") as f:
            # Write header
            f.write("id,name,email,age,salary,department\n")

            for i in range(1, rows + 1):
                if i % 50 == 0:
                    # Missing comma (wrong number of fields)
                    f.write(f"{i},User{i} invalid_email@domain,25,50000,Engineering\n")
                elif i % 37 == 0:
                    # Extra comma (too many fields)
                    f.write(
                        f"{i},User{i},user{i}@test.com,25,50000,Engineering,Extra Field\n"
                    )
                elif i % 29 == 0:
                    # Unescaped quotes
                    f.write(
                        f'{i},"User{i} "Special Name",user{i}@test.com,25,50000,Engineering\n'
                    )
                elif i % 23 == 0:
                    # Invalid characters
                    f.write(f"{i},User{i}™,user{i}@test.com,25,50000,Engineering\n")
                elif i % 19 == 0:
                    # Completely malformed line
                    f.write("This is not a valid CSV line at all!\n")
                else:
                    # Normal line
                    name = random.choice(self.first_names)
                    email = f"{name.lower()}{i}@test.com"
                    age = random.randint(22, 65)
                    salary = random.randint(40000, 100000)
                    dept = random.choice(self.departments)
                    f.write(f"{i},{name},{email},{age},{salary},{dept}\n")

        print(f"Generated corrupted data: {file_path} ({rows} rows)")
        return file_path

    def generate_different_delimiters(self, rows: int = 300) -> list:
        """
        Generate CSV files with different delimiters

        Args:
            rows: Number of rows per file

        Returns:
            List of generated file paths
        """
        files = []
        delimiters = {
            "semicolon_data.csv": ";",
            "tab_data.csv": "\t",
            "pipe_data.csv": "|",
        }

        base_data = {
            "id": range(1, rows + 1),
            "name": [
                f"{random.choice(self.first_names)} {random.choice(self.last_names)}"
                for _ in range(rows)
            ],
            "email": [f"user{i}@test.com" for i in range(1, rows + 1)],
            "value": np.random.uniform(10.0, 1000.0, rows).round(2),
        }

        for filename, delimiter in delimiters.items():
            df = pd.DataFrame(base_data)
            file_path = self.output_dir / filename
            df.to_csv(file_path, index=False, sep=delimiter)
            files.append(file_path)
            print(f"Generated {delimiter}-delimited data: {file_path}")

        return files

    def generate_encoding_variants(self, rows: int = 200) -> list:
        """
        Generate files with different encodings

        Args:
            rows: Number of rows per file

        Returns:
            List of generated file paths
        """
        files = []

        # Data with international characters
        international_names = [
            "José García",
            "François Dubois",
            "Müller Schmidt",
            "Андрей Петров",
            "Mohammed Ahmed",
            "Takeshi Yamada",
            "Björk Guðmundsdóttir",
            "Αλέξανδρος Παπαδόπουλος",
        ]

        data = {
            "id": range(1, rows + 1),
            "name": [random.choice(international_names) for _ in range(rows)],
            "city": [
                random.choice(
                    ["México", "París", "München", "Москва", "القاهرة", "東京", "Αθήνα"]
                )
                for _ in range(rows)
            ],
            "description": [
                f"Description with special chars: áéíóú ñç ßø æå" for _ in range(rows)
            ],
        }

        df = pd.DataFrame(data)

        encodings = {
            "utf8_data.csv": "utf-8",
            "latin1_data.csv": "latin-1",
            "utf16_data.csv": "utf-16",
        }

        for filename, encoding in encodings.items():
            file_path = self.output_dir / filename
            try:
                df.to_csv(file_path, index=False, encoding=encoding)
                files.append(file_path)
                print(f"Generated {encoding} encoded data: {file_path}")
            except UnicodeEncodeError:
                print(f"Warning: Could not encode to {encoding}, skipping {filename}")

        return files

    def generate_all_samples(self):
        """Generate all sample datasets"""
        print("=== Generating Sample CSV Files ===")

        generated_files = []

        # Clean data
        generated_files.append(self.generate_clean_data(1000, "01_clean_employees.csv"))

        # Messy data
        generated_files.append(self.generate_messy_data(800, "02_messy_employees.csv"))

        # Mixed types
        generated_files.append(
            self.generate_mixed_types_data(500, "03_mixed_types.csv")
        )

        # Large dataset
        generated_files.append(
            self.generate_large_dataset(10000, "04_large_transactions.csv")
        )

        # Corrupted data
        generated_files.append(
            self.generate_corrupted_data(200, "05_corrupted_data.csv")
        )

        # Different delimiters
        delimiter_files = self.generate_different_delimiters(300)
        generated_files.extend(delimiter_files)

        # Different encodings
        encoding_files = self.generate_encoding_variants(200)
        generated_files.extend(encoding_files)

        # Create summary
        summary = {
            "generated_date": datetime.now().isoformat(),
            "total_files": len(generated_files),
            "files": [
                {
                    "name": file.name,
                    "path": str(file),
                    "size_bytes": file.stat().st_size if file.exists() else 0,
                }
                for file in generated_files
            ],
        }

        summary_file = self.output_dir / "sample_files_summary.json"
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)

        print(f"\n=== Summary ===")
        print(f"Generated {len(generated_files)} sample files")
        print(f"Output directory: {self.output_dir}")
        print(f"Summary saved to: {summary_file}")

        return generated_files


def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(
        description="Generate sample CSV files for testing"
    )
    parser.add_argument(
        "--output-dir", default="data/samples", help="Output directory for sample files"
    )
    parser.add_argument(
        "--clean-only", action="store_true", help="Generate only clean data"
    )
    parser.add_argument(
        "--large-size",
        type=int,
        default=10000,
        help="Size of large dataset (default: 10000)",
    )

    args = parser.parse_args()

    generator = SampleDataGenerator(args.output_dir)

    if args.clean_only:
        generator.generate_clean_data(1000, "clean_employees.csv")
    else:
        # Override large dataset size
        original_method = generator.generate_large_dataset
        generator.generate_large_dataset = lambda rows=args.large_size, filename="04_large_transactions.csv": original_method(
            rows, filename
        )

        generator.generate_all_samples()


if __name__ == "__main__":
    main()
