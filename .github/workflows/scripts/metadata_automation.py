"""
Automates metadata ingestion from Google Sheets to the models.
"""

from pathlib import Path

import yaml

METADATA_FILE_PATH = "metadata.yaml"


def dump_metadata_into_schema_yaml(
    dataset_id: str, table_id: str, metadata: dict
) -> None:
    """
    Dumps the metadata into the schema.yaml file.
    """
    schema_yaml_path = f"models/{dataset_id}/schema.yml"
    if not Path(schema_yaml_path).exists():
        schema = {"version": 2, "models": []}
    else:
        schema = load_yaml(schema_yaml_path)
    if len(schema["models"]) > 0:
        # If we find a model with the same name, we delete it.
        schema["models"] = [m for m in schema["models"] if m["name"] != table_id]
    schema["models"].append(metadata)
    with open(schema_yaml_path, "w") as f:
        yaml.dump(schema, f)


def fetch_metadata_from_google_sheets(spreadsheet_id: str):
    """
    Fetches the metadata from Google Sheets.
    """
    return {
        "name": "my_first_model",
        "description": "A starter dbt model",
        "columns": [
            {
                "name": "id",
                "description": "The primary key for this table",
                "tests": [
                    "unique",
                    "not_null",
                ],
            },
        ],
    }


def load_yaml(filepath: str) -> dict:
    """
    Loads a YAML file.
    """
    with open(filepath, "r") as f:
        return yaml.safe_load(f)


def load_metadata_file() -> dict:
    """
    Loads the file that contains path to the models' metadata.
    """
    return load_yaml(METADATA_FILE_PATH)


if __name__ == "__main__":
    # Load the metadata file
    metadata: dict = load_metadata_file()

    # List all models
    models: dict = metadata["models"]

    # Iterate over datasets
    for dataset_id in models.keys():

        # Get the dataset
        dataset: dict = models[dataset_id]
        print(f"Ingesting metadata for dataset {dataset_id}")

        # Iterate over tables
        for table_id in dataset.keys():

            # Get the table
            table: dict = dataset[table_id]

            # Check whether there is a spreadsheet ID set for this table
            if "spreadsheet_id" in table and table["spreadsheet_id"]:
                print(f"- Fetching metadata for table {table_id}...", end="")

                # Fetch the metadata from Google Sheets
                table_metadata = fetch_metadata_from_google_sheets(
                    table["spreadsheet_id"]
                )

                # Dump the metadata into the schema.yaml file
                dump_metadata_into_schema_yaml(dataset_id, table_id, table_metadata)
