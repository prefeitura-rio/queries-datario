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

import json
from os import getenv
import re
from typing import List

from arcgis import GIS
from arcgis.gis import ContentManager, Item
import jinja2
import requests

DEFAULT_TAGS = ["datario", "escritorio_de_dados", "datalake"]
HTML_TEMPLATE_PATH = ".github/workflows/templates/description.html.jinja"

DATA_404_PAGE = "https://prefeitura-rio.github.io/queries-datario/pages/404?prefix={prefix}"
DUPLICATES_FILE_PATH = "duplicates.txt"
METADATA_FILE_PATH = "metadata.json"
THUMBNAIL_URL = (
    "https://nayemdevs.com/wp-content/uploads/2020/03/default-product-image.png"
)


class GisItemNotFound(Exception):
    """
    Raised when an item is not found.
    """


def get_license():
    """
    Returns the license (can be HTML formatted).
    """
    cc_license = "by-nd/3.0"
    cc_license_name = "Attribution-NoDerivatives 3.0"
    license_url = f"https://creativecommons.org/licenses/{cc_license}/deed.pt_BR"
    return f"""
    <a href={license_url}>
        <img    alt="Creative Commons License"
                src="https://i.creativecommons.org/l/{cc_license}/88x31.png"
                style="border-width:0"
        />
    </a>
    <br />
    This work is licensed under a
    <a rel="license" href={license_url}>Creative Commons {cc_license_name} Unported License</a>.
    """

def get_duplicates() -> List[str]:
    """
    Returns the list of duplicates.
    """
    with open(DUPLICATES_FILE_PATH, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    # Remove lines that start with # and empty lines after stripping
    return [line.strip() for line in lines if line.strip() and not line.startswith("#")]

def get_default_tags(dataset_id: str, table_id: str) -> List[str]:
    """
    Returns the default tags.
    """
    return DEFAULT_TAGS + [dataset_id, table_id]


def get_directory(dataset_id: str, table_id: str, duplicates_list: List[str] = None) -> str:
    """
    Returns the directory where the item will be stored.
    """
    duplicates_list = duplicates_list or get_duplicates()
    full_name = f"{dataset_id}.{table_id}"
    if full_name in duplicates_list:
        return "duplicates"
    return "public"

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
    tags = get_default_tags(dataset_id, table_id)
    tags_query = ""
    for tag in tags:
        if tags_query == "":
            tags_query = f"tags:{tag}"
        else:
            tags_query += f" AND tags:{tag}"
    try:  # If item already exists, update it.
        item = get_item(search_query=tags_query, gis=gis,)
        item.update(**data)
        return item
    except GisItemNotFound:  # Else, create it.
        content_manager: ContentManager = gis.content
        item = content_manager.add(**data)
        return item


def load_metadata_file() -> dict:
    """
    Loads the file that contains path to the models' metadata.
    """
    with open(METADATA_FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_html_from_metadata(
    metadata: json, dataset_id: str, table_id: str, url: str
) -> str:
    """
    Input format:
    {
        "title": "some-title-here",
        "short_description": "some short description here",
        "long_description": "some long description here",
        "update_frequency": "some update frequency here",
        "temporal_coverage": "some temporal coverage here",
        "data_owner": "some data owner here",
        "publisher_name": "some publisher name here",
        "publisher_email": "some publisher email here",
        "tags": [
            "some tag here",
            "some other tag here"
        ],
        "columns": [
            {
                "name": "some column name here",
                "description": "some column description here",
            },
            ...
        ]
    }

    """
    with open(HTML_TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template: jinja2.Template = jinja2.Template(f.read())
    return template.render(
        **metadata, dataset_id=dataset_id, table_id=table_id, url=url
    )


def get_url(dataset_id: str, table_id: str, full_title: str) -> str:
    """
    Returns the URL for the item.
    """
    def parse_title(title: str) -> str:
        # Remove symbols (allow only letters with or without accents, spaces, numbers and hiphens)
        title = re.sub(r"[^a-zA-ZáàâãéèêíìîóòôõúùûçÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ0-9\s-]", "", title)
        # To lower
        title = title.lower()
        # Replace spaces with dashes
        title = re.sub(r"\s", "-", title)
        return title
    # Build a base download URL
    base_url = f"https://storage.googleapis.com/datario/share/{dataset_id}/{table_id}/data.csv.gz"
    # Check if the URL exists
    try:
        response = requests.head(base_url)
        if response.status_code == 200:
            return base_url
        title = parse_title(full_title)
        return DATA_404_PAGE.format(prefix=title)
    except requests.exceptions.RequestException:
        return DATA_404_PAGE.format(prefix=title)


def build_items_data_from_metadata_json() -> List[dict]:
    """
    Builds item data from a schema.yml file.

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
                ...
            },
        }
    """
    items_data = []
    categories = []
    dataset_ids = []
    table_ids = []
    metadata = load_metadata_file()
    for dataset_id in metadata:
        for table_id in metadata[dataset_id]:
            url = get_url(dataset_id=dataset_id, table_id=table_id, full_title=metadata[dataset_id][table_id]["title"])
            item_data = {
                "item_properties": {
                    "type": "Document Link",
                    "typeKeywords": "Data, Document",
                    "description": build_html_from_metadata(
                        metadata[dataset_id][table_id],
                        dataset_id,
                        table_id,
                        url,
                    ),
                    "snippet": metadata[dataset_id][table_id]["short_description"],
                    "title": metadata[dataset_id][table_id]["title"],
                    "url": url,
                    "tags": ",".join(
                        get_default_tags(dataset_id, table_id)
                        + metadata[dataset_id][table_id]["tags"]
                    ) if "tags" in metadata[dataset_id][table_id] else ",".join(
                        get_default_tags(dataset_id, table_id)
                    ),
                    "licenseInfo": get_license(),
                    "accessInformation": metadata[dataset_id][table_id]["data_owner"],
                },
                # "thumbnail": THUMBNAIL_URL,
            }
            items_data.append(item_data)
            if "categories" in metadata[dataset_id][table_id]:
                categories.append(metadata[dataset_id][table_id]["categories"])
            dataset_ids.append(dataset_id)
            table_ids.append(table_id)
    return items_data, categories, dataset_ids, table_ids


def categorize_item(item: Item, categories: List[str], gis: GIS = None) -> bool:
    """
    Categorizes an item.
    """
    gis = gis or get_gis_client()
    cs = gis.admin.category_schema
    return cs.categorize_item(item, categories)


if __name__ == "__main__":
    duplicates_list = get_duplicates()
    (
        items_data,
        categories,
        dataset_ids,
        table_ids,
    ) = build_items_data_from_metadata_json()
    for item_data, item_categories, dataset_id, table_id in zip(
        items_data, categories, dataset_ids, table_ids
    ):
        item: Item = create_or_update_item(
            dataset_id=dataset_id, table_id=table_id, data=item_data
        )
        print(f"Created/updated item: ID={item.id}, Title={item.title}")
        item.share(everyone=True, org=True, groups=item_categories)
        print(f"Shared item: ID={item.id} with groups: {item_categories}")
        move_dir = get_directory(dataset_id, table_id, duplicates_list)
        item.move(move_dir)
        print(f"Moved item: ID={item.id} to {move_dir}/ directory")
