"""
Explores `schema.yml` files in order to build fixtures for the database.

Each `schema.yml` file is a collection of tables and its columns. The
format of the file is:

```yaml
version: 2
models:
    -   name: table_name
        description: table_description
        columns:
            -   name: column_name
                description: column_description
            ...
    ...
```

The path to the `schema.yml` file tells us the dataset name. For example,
if the path is `models/dataset/schema.yml`, then the dataset name is `dataset`.

We, then, want to generate a single fixture file such as:

```json
[
    {
        "model": "metadata_api.dataset",
        "pk": 1,
        "fields": {
            "name": "dataset",
            "description": null,
        },
    },
    {
        "model": "metadata_api.table",
        "pk": 1,
        "fields": {
            "name": "table_name",
            "description": "table_description",
            "dataset": 1,
        },
    },
    ...
    {
        "model": "metadata_api.column",
        "pk": 1,
        "fields": {
            "name": "column_name",
            "description": "column_description",
            "table": 1,
        },
    },
    ...
]
```
"""

import argparse
import json
from pathlib import Path
from typing import List

import yaml


def list_all_schema_yml_files(root_directory: str) -> List[Path]:
    """
    List all `schema.yml` files in the given directory.

    Args:
        root_directory: The root directory to search for `schema.yml` files.

    Returns:
        A list of `Path` objects pointing to the `schema.yml` files.
    """
    return [path for path in Path(root_directory).rglob("schema.yml") if path.is_file()]


def generate_fixtures(schema_yml_files: List[Path]) -> List[dict]:
    """
    Generate fixtures for the database.

    Args:
        schema_yml_files: A list of `Path` objects pointing to the `schema.yml` files.

    Returns:
        A list of fixtures.
    """
    fixtures = []
    idx_dataset = 1
    idx_table = 1
    idx_column = 1

    for schema_yml_file in schema_yml_files:

        dataset_name = schema_yml_file.parent.name

        with open(schema_yml_file, "r") as f:
            schema = yaml.safe_load(f)

        dataset_fixture = {
            "model": "metadata_api.dataset",
            "pk": idx_dataset,
            "fields": {
                "name": dataset_name,
                "description": None,
            },
        }
        fixtures.append(dataset_fixture)

        for table_schema in schema["models"]:
            table_name = table_schema["name"]
            table_description = table_schema.get("description", None)

            table_fixture = {
                "model": "metadata_api.table",
                "pk": idx_table,
                "fields": {
                    "name": table_name,
                    "description": table_description,
                    "dataset": idx_dataset,
                },
            }
            fixtures.append(table_fixture)

            for column_schema in table_schema["columns"]:
                column_name = column_schema["name"]
                column_description = column_schema.get("description", None)

                column_fixture = {
                    "model": "metadata_api.column",
                    "pk": idx_column,
                    "fields": {
                        "name": column_name,
                        "description": column_description,
                        "table": idx_table,
                    },
                }
                fixtures.append(column_fixture)
                idx_column += 1

            idx_table += 1

        idx_dataset += 1

    return fixtures


def serialize_fixtures_to_file(fixtures: List[dict], output_file: str) -> None:
    """
    Serialize the fixtures to a file.

    Args:
        fixtures: A list of fixtures.
        output_file: The output file path.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(fixtures, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate fixtures for the database.")
    parser.add_argument(
        "--input-directory",
        "-i",
        type=str,
        required=True,
        help="The root directory to search for `schema.yml` files.",
    )
    parser.add_argument(
        "--output-file", "-o", type=str, required=True, help="The output file path."
    )
    args = parser.parse_args()

    schema_yml_files = list_all_schema_yml_files(args.input_directory)
    fixtures = generate_fixtures(schema_yml_files)
    serialize_fixtures_to_file(fixtures, args.output_file)
