# Eagle Cooler 🦅❄️

[![PyPI version](https://badge.fury.io/py/eagle-cooler.svg)](https://badge.fury.io/py/eagle-cooler)
[![Python Support](https://img.shields.io/pypi/pyversions/eagle-cooler.svg)](https://pypi.org/project/eagle-cooler/)
[![License](https://img.shields.io/github/license/ZackaryW/py-eagle-cooler.svg)](LICENSE)

A modern Python wrapper for the [Eagle.cool](https://eagle.cool) HTTP API. Works independently with Eagle's web API or seamlessly integrates with the Power Eagle plugin system for enhanced functionality.

## ✨ Features

- 🚀 **Complete API Coverage** - Full implementation of Eagle's HTTP API
- 🔐 **Flexible Authentication** - Works standalone with manual token setup or automatically with Power Eagle
- 📝 **Type Hints** - Better development experience with full type annotations
- 🎯 **Easy-to-use Interface** - Clean, class-based API design
- ⚡ **Modern Python** - Built for Python 3.13+ with modern best practices
- 🔌 **Plugin Ready** - Enhanced integration with Power Eagle plugin ecosystem
- 🏠 **Standalone Ready** - Can work independently with just Eagle's web API

## 📦 Installation

Install the latest stable version from PyPI:

```bash
# Using uv (recommended)
uv add eagle-cooler

# Using pip
pip install eagle-cooler

# For development
git clone https://github.com/ZackaryW/py-eagle-cooler.git
cd py-eagle-cooler
uv sync --dev
```

## 🚀 Quick Start

### Standalone Usage (Web API Only)

For basic functionality using Eagle's HTTP API directly:

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

# Add item from local file
local_item = EagleWebApi.item.add_from_path(
    path="/path/to/image.jpg",
    name="Local Image",
    tags=["local"]
)
```

### Power Eagle Integration (Enhanced Features)

When running in a Power Eagle context, access to enhanced features:

```python
# In a Power Eagle Python script
from eagle_cooler import eagleContext, EagleCallback

# Get selected items and folders from Power Eagle context
selected_items = eagleContext.get_selected_items()
selected_folders = eagleContext.get_selected_folders()

# Get just the IDs if needed
selected_item_ids = eagleContext.get_selected_item_ids()
selected_folder_ids = eagleContext.get_selected_folder_ids()

# Use callback system for advanced plugin operations
# (extensive callback API available for plugin development)
```

## 📚 API Reference

### 🏢 Application
- `EagleWebApi.application.info()` - Get application information

### 📁 Folders
- `EagleWebApi.folder.create(name, parent_id=None)` - Create folder
- `EagleWebApi.folder.rename(folder_id, new_name)` - Rename folder
- `EagleWebApi.folder.update(folder_id, new_name=None, new_description=None, new_color=None)` - Update folder properties
- `EagleWebApi.folder.list()` - List all folders
- `EagleWebApi.folder.list_recent()` - List recent folders

### 📚 Library
- `EagleWebApi.library.info()` - Get library information
- `EagleWebApi.library.history()` - Get library history
- `EagleWebApi.library.switch(library_path)` - Switch to different library
- `EagleWebApi.library.icon(library_path)` - Get library icon

### 🖼️ Items
- `EagleWebApi.item.list(limit=None, offset=None, order_by=None, keyword=None, ext=None, tags=None, folders=None)` - List items with filters
- `EagleWebApi.item.get_info(item_id)` - Get item details
- `EagleWebApi.item.get_thumbnail(item_id)` - Get item thumbnail
- `EagleWebApi.item.update(item_id, tags=None, annotation=None, url=None, star=None)` - Update item properties
- `EagleWebApi.item.add_from_url(url, name, website=None, tags=None, star=None, annotation=None, modification_time=None, folder_id=None, headers=None)` - Add item from URL
- `EagleWebApi.item.add_from_path(path, name, website=None, annotation=None, tags=None, folder_id=None)` - Add item from file path
- `EagleWebApi.item.add_from_urls(items, folder_id=None)` - Add multiple items from URLs
- `EagleWebApi.item.add_bookmark(url, name, base64=None, tags=None, modification_time=None, folder_id=None)` - Add bookmark
- `EagleWebApi.item.move_to_trash(item_ids)` - Move items to trash
- `EagleWebApi.item.refresh_thumbnail(item_id)` - Refresh thumbnail
- `EagleWebApi.item.refresh_palette(item_id)` - Refresh color palette

### 🔧 Context (Power Eagle Mode)
- `eagleContext.get_selected_item_ids()` - Get selected item IDs from Power Eagle context
- `eagleContext.get_selected_folder_ids()` - Get selected folder IDs from Power Eagle context  
- `eagleContext.get_selected_items(throw=False)` - Get selected items as typed ItemModel objects
- `eagleContext.get_selected_folders()` - Get selected folders as typed FolderModel objects

### 📞 Callbacks (Power Eagle Plugins)
- `EagleCallback` - Callback system for Power Eagle plugin integration (extensive API available)

## 🔌 Usage Modes

Eagle Cooler supports two usage modes:

### 🏠 Standalone Mode (Web API)
- **Limited Capacity**: Basic API operations through Eagle's HTTP interface
- **Manual Setup**: Requires Eagle application running with HTTP API enabled
- **Authentication**: Uses direct API calls (no token management)
- **Features**: Core operations like listing, creating folders, basic item management

### 🚀 Power Eagle Mode (Enhanced)
- **Full Capacity**: Complete feature set with enhanced functionality
- **Automatic Setup**: Token and context management handled automatically
- **Authentication**: Seamless integration with Power Eagle's security context
- **Features**: All core operations plus callbacks, advanced file operations, and plugin ecosystem integration

```python
# Standalone mode example
from eagle_cooler import EagleWebApi

# Basic operations available
folders = EagleWebApi.folder.list()

# Power Eagle mode example (when POWEREAGLE_CONTEXT is available)
from eagle_cooler import EagleWebApi, eagleContext, EagleCallback

# Enhanced operations available:
# 1. Automatic token management
folders = EagleWebApi.folder.list()

# 2. Access to Power Eagle context with typed models
selected_items = eagleContext.get_selected_items()  # Returns list[ItemModel]
selected_folders = eagleContext.get_selected_folders()  # Returns list[FolderModel]

# 3. Callback system for advanced plugin operations
if selected_items:
    for item in selected_items:
        print(f"Selected item: {item['name']} ({item['ext']})")
        # Use callback system to interact with Power Eagle host
        # (extensive callback API available - see METHODS_WITH_RETURN_VALUES)
```

## ⚙️ Requirements

- **Python**: >= 3.13
- **Eagle.cool**: Application running with API access enabled
- **Dependencies**: `requests >= 2.25.0`
- **For Power Eagle**: `POWEREAGLE_CONTEXT` environment variable set

### Setup Eagle API Access

1. Open Eagle.cool application
2. Go to **Preferences** → **Plugin**
3. Enable **HTTP API**
4. Note the API port (default: 41595)

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/py-eagle-cooler.git
   cd py-eagle-cooler
   ```
3. **Install development dependencies**:
   ```bash
   uv sync --dev
   ```
4. **Make your changes**
5. **Run tests** (when available):
   ```bash
   uv run pytest
   ```
6. **Submit a pull request**

### Development Setup

```bash
# Clone the repository
git clone https://github.com/ZackaryW/py-eagle-cooler.git
cd py-eagle-cooler

# Install with development dependencies
uv sync --dev

# Run the package in development mode
uv run python -m eagle_cooler
```

## 📜 License

This project is licensed under the same terms as Power Eagle.

---

<p align="center">
  <sub>Built with ❤️ for the Eagle.cool community</sub>
</p>