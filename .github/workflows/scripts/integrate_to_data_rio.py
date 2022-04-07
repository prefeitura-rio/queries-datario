"""
Publishes data to data.rio

For future reference, this is what the content_manager.add command supports:

# content_manager.add(
#     item_properties={
#         "type" :"",# Optional string. Indicates type of item, see URL 1 below for valid values.
#         "dataUrl" :"",# Optional string. The Url of the data stored on cloud storage. If given, filename is required.
#         "filename" :"",# Optional string. The name of the file on cloud storage. This is required is dataUrl is used.
#         "typeKeywords" :"",# Optional string. Provide a lists all subtypes, see URL below for valid values.
#         "description" :"",# Optional string. Description of the item.
#         "title" :"",# Optional string. Name label of the item.
#         "url" :"",# Optional string. URL to item that are based on URLs.
#         "text" :"",# Optional string. For text based items such as Feature Collections & WebMaps
#         "tags" :"",# Optional string. Tags listed as commaseparated values, or a list of strings.
#                     # Used for searches on items.
#         "snippet" :"",# Optional string. Provide a short summary (limit to max 250 characters) of the what the item is.
#         "extent" :"",# Optional string. Provide commaseparated values for min x, min y, max x, max y.
#         "spatialReference" :"",# Optional string. Coordinate system that the item is in.
#         "accessInformation" :"",# Optional string. Information on the source of the content.
#         "licenseInfo" :"",# Optional string. Any license information or restrictions regarding the content.
#         "culture" :"",# Optional string. Locale, country and language information.
#         "commentsEnabled" :"",# Optional boolean. Default is true, controls whether comments are allowed (true)
#                                 # or not allowed (false).
#         "culture" :"",# Optional string. Language and country information.
#         "overwrite" :"",# Optional boolean. Default is `false`. Controls whether item can be overwritten.
#     },
#     data=None,      # Optional string. Either a path or URL to the data.
#     thumbnail=None, # Optional string. Either a path or URL to a thumbnail image.
#     metadata=None,  # Optional string. Either a path or URL to the metadata.
#     owner=None,     # Optional string. Defaults to the logged in user.
#     folder=None,    # Optional string. Name of the folder where placing item.
#     item_id=None,   # Optional string. Available in ArcGIS Enterprise 10.8.1+. Not available in ArcGIS Online.
#                     # This parameter allows the desired item id to be specified during creation which
#                     # can be useful for cloning and automated content creation scenarios.
#                     # The specified id must be a 32 character GUID string without any special characters.
#                     # If the `item_id` is already being used, an error will be raised
#                     # during the `add` process.
#                     # Example: item_id=9311d21a9a2047d19c0faaebd6f2cca6
# )
"""

from os import getenv
from pathlib import Path
from typing import List

from arcgis import GIS
from arcgis.gis import ContentManager, Item
import markdown
import ruamel.yaml as ryaml

DEFAULT_TAG = "datario"


class GisItemNotFound(Exception):
    """
    Raised when an item is not found.
    """


def load_ruamel():
    """
    Loads ryaml module.
    """
    ruamel = ryaml.YAML()
    ruamel.default_flow_style = False
    ruamel.top_level_colon_align = True
    ruamel.indent(mapping=2, sequence=4, offset=2)
    return ruamel


def load_metadata_file(filepath: str) -> dict:
    """
    Loads the file that contains path to the models' metadata.
    """
    ruamel = load_ruamel()
    return ruamel.load((Path(filepath)).open(encoding="utf-8"))


def get_gis_client(url: str = None, username: str = None, password: str = None) -> GIS:
    """
    Returns a GIS client.
    """
    url = url or getenv("ARCGIS_URL")
    username = username or getenv("ARCGIS_USERNAME")
    password = password or getenv("ARCGIS_PASSWORD")
    return GIS(url, username, password)


def get_item(*, item_id: str = None, search_query: str = None, gis: GIS = None) -> Item:
    """
    Returns an item.
    """
    # Ensures that either item_id or search is provided.
    if not search_query and not item_id:
        raise ValueError("You must provide either an item_id or a search query.")
    # Get GIS client and the content manager.
    gis = gis or get_gis_client()
    content_manager: ContentManager = gis.content
    # If item_id is provided, get and return the item.
    if item_id:
        item = content_manager.get(item_id)
        if not item:
            raise GisItemNotFound(f"Item with id {item_id} not found.")
        return item
    # Else, search for the item.
    items = content_manager.search(search_query)
    if len(items) == 0:
        raise GisItemNotFound(f"No items found for search query: {search_query}")
    return items[0]


def create_or_update_item(dataset_id: str, table_id: str, data: dict) -> Item:
    """
    Creates or updates an item.
    """
    gis = get_gis_client()
    try:  # If item already exists, update it.
        item = get_item(
            search_query=f'tags:"{DEFAULT_TAG}" AND tags:"{dataset_id}" AND tags:"{table_id}"',
            gis=gis,
        )
        item.update(**data)
        return item
    except GisItemNotFound:  # Else, create it.
        content_manager: ContentManager = gis.content
        item = content_manager.add(**data)
        return item


def list_all_schema_yml_files(root_directory: str) -> List[Path]:
    """
    List all `schema.yml` files in the given directory.
    Args:
        root_directory: The root directory to search for `schema.yml` files.
    Returns:
        A list of `Path` objects pointing to the `schema.yml` files.
    """
    return [path for path in Path(root_directory).rglob("schema.yml") if path.is_file()]


def markdown_to_html(markdown_text: str) -> str:
    """
    Converts markdown text to HTML. As we're in a custom
    environment, we must replace `<hX>` tags with `<font size="X">`
    tags.
    """
    base_html = markdown.markdown(markdown_text)
    hx_replacements = {
        "<h1>": '<font size="6">',
        "<h2>": '<font size="5">',
        "<h3>": '<font size="4">',
        "<h4>": '<font size="3">',
        "<h5>": '<font size="2">',
        "<h6>": '<font size="1">',
        "</h1>": "</font>",
        "</h2>": "</font>",
        "</h3>": "</font>",
        "</h4>": "</font>",
        "</h5>": "</font>",
        "</h6>": "</font>",
        "\n": "<br>",
    }
    for key, value in hx_replacements.items():
        base_html = base_html.replace(key, value)
    print([base_html])
    return base_html


def generate_name(dataset_id: str, table_id: str) -> str:
    """
    Generates a name for the item.
    """
    return f"datario.{dataset_id}.{table_id}"


def get_url(dataset_id: str, table_id: str) -> str:
    """
    Returns the URL for the item.
    """
    return f"https://dados.rio/"


def get_tags(dataset_id: str, table_id: str) -> str:
    """
    Returns the tags for the item.
    """
    return f"{DEFAULT_TAG},{dataset_id},{table_id}"


def build_items_data_from_schema_yml(schema_yml_files: List[Path]) -> List[dict]:
    """
    Builds item data from a schema.yml file.

    Args:
        schema_yml_files: Path to the schema.yml files. After loaded, each schema
            will look like this:
            {
                "version": "2",
                "models": [
                    {
                        "name": "table_name",
                        "description": "table description",
                        "columns": [
                            {
                                "name": "column_name",
                                "description": "column description",
                            },
                            ...
                        ]
                    },
                    ...
                ],
            }

    Returns:
        A dictionary containing the item data. The format is:
        {
            item_properties={
                "type": "Document Link",
                "typeKeywords": "Data, Document",
                "description": "some description here", # We need to parse from Markdown to HTML
                "title": "some title here",
                "url": "https://some.url.here",
                "tags": "tag1, tag2, tag3",
            },
        }
    """
    items_data = []
    dataset_ids = []
    table_ids = []
    for schema_yml_path in schema_yml_files:
        schema: dict = load_metadata_file(schema_yml_path)
        dataset_id = Path(schema_yml_path).absolute().parent.name
        for model in schema["models"]:
            item_data = {
                "item_properties": {
                    "type": "Document Link",
                    "typeKeywords": "Data, Document",
                    "description": markdown_to_html(model["description"]),
                    "title": generate_name(
                        dataset_id=dataset_id, table_id=model["name"]
                    ),
                    "url": get_url(dataset_id=dataset_id, table_id=model["name"]),
                    "tags": get_tags(dataset_id=dataset_id, table_id=model["name"]),
                },
            }
            items_data.append(item_data)
            dataset_ids.append(dataset_id)
            table_ids.append(model["name"])
    return items_data, dataset_ids, table_ids


if __name__ == "__main__":

    schema_yml_files = list_all_schema_yml_files(root_directory="./")
    items_data, dataset_ids, table_ids = build_items_data_from_schema_yml(
        schema_yml_files=schema_yml_files
    )
    for item_data, dataset_id, table_id in zip(items_data, dataset_ids, table_ids):
        item: Item = create_or_update_item(
            dataset_id=dataset_id, table_id=table_id, data=item_data
        )
        print(f"Created/updated item: ID={item.id}, Title={item.title}")
