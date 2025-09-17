# Eagle Cooler - Python API for Eagle.cool

A Python wrapper for the Eagle.cool HTTP API, designed to work seamlessly with the Power Eagle plugin system.

## Features

- Complete Python implementation of Eagle's HTTP API
- Automatic token management (works with Power Eagle context)
- Type hints for better development experience
- Easy-to-use class-based interface
- Comprehensive coverage of Eagle's API endpoints

## Installation

```bash
uv add eagle-cooler
# or
pip install eagle-cooler
```

## Quick Start

```python
from eagle_cooler import EagleWebApi

# Get application info
app_info = EagleWebApi.application.info()
print(f"Eagle version: {app_info['version']}")

# List folders
folders = EagleWebApi.folder.list()
print(f"Found {len(folders)} folders")

# Create a new folder
new_folder = EagleWebApi.folder.create("My New Folder")
print(f"Created: {new_folder['name']}")

# List items with filters
items = EagleWebApi.item.list(limit=10, ext="jpg")
print(f"Found {len(items)} JPG images")

# Add item from URL
result = EagleWebApi.item.add_from_url(
    url="https://example.com/image.jpg",
    name="Example Image",
    tags=["example", "test"]
)
```

## API Documentation

### Application
- `EagleWebApi.application.info()` - Get application information

### Folders
- `EagleWebApi.folder.create(name, parent_id=None)` - Create folder
- `EagleWebApi.folder.rename(folder_id, new_name)` - Rename folder
- `EagleWebApi.folder.update(folder_id, **kwargs)` - Update folder properties
- `EagleWebApi.folder.list()` - List all folders
- `EagleWebApi.folder.list_recent()` - List recent folders

### Library
- `EagleWebApi.library.info()` - Get library information
- `EagleWebApi.library.history()` - Get library history
- `EagleWebApi.library.switch(library_path)` - Switch to different library
- `EagleWebApi.library.icon(library_path)` - Get library icon

### Items
- `EagleWebApi.item.list(**filters)` - List items with filters
- `EagleWebApi.item.get_info(item_id)` - Get item details
- `EagleWebApi.item.get_thumbnail(item_id)` - Get item thumbnail
- `EagleWebApi.item.update(item_id, **kwargs)` - Update item properties
- `EagleWebApi.item.add_from_url(url, name, **kwargs)` - Add item from URL
- `EagleWebApi.item.add_from_path(path, name, **kwargs)` - Add item from file
- `EagleWebApi.item.add_bookmark(url, name, **kwargs)` - Add bookmark
- `EagleWebApi.item.move_to_trash(item_ids)` - Move items to trash
- `EagleWebApi.item.refresh_thumbnail(item_id)` - Refresh thumbnail
- `EagleWebApi.item.refresh_palette(item_id)` - Refresh color palette

## Power Eagle Integration

This package is designed to work with the Power Eagle plugin system. When running in a Power Eagle context, the API token is automatically obtained from the environment.

```python
# In a Power Eagle Python script
from eagle_cooler import EagleWebApi

# Token is automatically available from Power Eagle context
folders = EagleWebApi.folder.list()
```

## Requirements

- Python >= 3.13
- Eagle.cool application running
- API access enabled in Eagle preferences
- For Power Eagle: POWEREAGLE_CONTEXT environment variable set

## License

This project is licensed under the same terms as Power Eagle.