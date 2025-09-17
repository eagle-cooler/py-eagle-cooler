

import requests
from typing import Optional, Dict, Any, List
from .core import EagleCoolerCore


class EagleWebApi:
    """Python implementation of Eagle API client for HTTP requests to Eagle application"""
    
    _token: Optional[str] = None

    @classmethod
    def _make_request(cls, path: str, method: str = "GET", data: Optional[Dict[str, Any]] = None, 
                     params: Optional[Dict[str, Any]] = None) -> Any:
        """Makes internal HTTP request to Eagle API"""
        token = EagleCoolerCore.token()
        if not token:
            raise Exception("No API token found")
            
        url = f"http://localhost:41595/api/{path}"
        
        # Add token to params
        if params is None:
            params = {}
        params["token"] = token
        
        # Remove None values from params and data
        if params:
            params = {k: v for k, v in params.items() if v is not None}
        if data:
            data = {k: v for k, v in data.items() if v is not None}
            
        try:
            if method.upper() == "POST":
                response = requests.post(url, params=params, json=data)
            else:
                response = requests.get(url, params=params)
                
            response.raise_for_status()
            result = response.json()
            return result.get("data")
        except Exception as e:
            print(f"Request failed: {e}")
            raise e
    
    class _Application:
        """_Application-related API methods"""
        
        @staticmethod
        def info() -> Any:
            """Gets application information"""
            return EagleWebApi._make_request("application/info")
    
    class _Folder:
        """_Folder-related API methods"""
        
        @staticmethod
        def create(name: str, parent_id: Optional[str] = None) -> Any:
            """Creates a new folder"""
            return EagleWebApi._make_request("folder/create", "POST", {
                "folderName": name,
                "parent": parent_id
            })
        
        @staticmethod
        def rename(folder_id: str, new_name: str) -> Any:
            """Renames a folder"""
            return EagleWebApi._make_request("folder/rename", "POST", {
                "folderId": folder_id,
                "newName": new_name
            })
        
        @staticmethod
        def update(folder_id: str, new_name: Optional[str] = None, 
                  new_description: Optional[str] = None, new_color: Optional[str] = None) -> Any:
            """Updates folder properties"""
            return EagleWebApi._make_request("folder/update", "POST", {
                "folderId": folder_id,
                "newName": new_name,
                "newDescription": new_description,
                "newColor": new_color
            })
        
        @staticmethod
        def list() -> Any:
            """Lists all folders"""
            return EagleWebApi._make_request("folder/list")
        
        @staticmethod
        def list_recent() -> Any:
            """Lists recent folders"""
            return EagleWebApi._make_request("folder/listRecent")
    
    class _Library:
        """_Library-related API methods"""
        
        @staticmethod
        def info() -> Any:
            """Gets library information"""
            return EagleWebApi._make_request("library/info")
        
        @staticmethod
        def history() -> Any:
            """Gets library history"""
            return EagleWebApi._make_request("library/history")
        
        @staticmethod
        def switch(library_path: str) -> Any:
            """Switches to a different library"""
            return EagleWebApi._make_request("library/switch", "POST", {
                "libraryPath": library_path
            })
        
        @staticmethod
        def icon(library_path: str) -> Any:
            """Gets library icon"""
            return EagleWebApi._make_request("library/icon", params={
                "libraryPath": library_path
            })
    
    class _Item:
        """_Item-related API methods"""
        
        @staticmethod
        def update(item_id: str, tags: Optional[List[str]] = None, annotation: Optional[str] = None,
                  url: Optional[str] = None, star: Optional[int] = None) -> Any:
            """Updates item properties"""
            return EagleWebApi._make_request("item/update", "POST", {
                "id": item_id,
                "tags": tags,
                "annotation": annotation,
                "url": url,
                "star": star
            })
        
        @staticmethod
        def refresh_thumbnail(item_id: str) -> Any:
            """Refreshes item thumbnail"""
            return EagleWebApi._make_request("item/refreshThumbnail", "POST", {
                "id": item_id
            })
        
        @staticmethod
        def refresh_palette(item_id: str) -> Any:
            """Refreshes item color palette"""
            return EagleWebApi._make_request("item/refreshPalette", "POST", {
                "id": item_id
            })
        
        @staticmethod
        def move_to_trash(item_ids: List[str]) -> Any:
            """Moves items to trash"""
            return EagleWebApi._make_request("item/moveToTrash", "POST", {
                "itemIds": item_ids
            })
        
        @staticmethod
        def list(limit: Optional[int] = None, offset: Optional[int] = None,
                order_by: Optional[str] = None, keyword: Optional[str] = None,
                ext: Optional[str] = None, tags: Optional[List[str]] = None,
                folders: Optional[List[str]] = None) -> Any:
            """Lists items with filters"""
            return EagleWebApi._make_request("item/list", params={
                "limit": limit,
                "offset": offset,
                "orderBy": order_by,
                "keyword": keyword,
                "ext": ext,
                "tags": tags,
                "folders": folders
            })
        
        @staticmethod
        def get_thumbnail(item_id: str) -> Any:
            """Gets item thumbnail"""
            return EagleWebApi._make_request("item/thumbnail", params={
                "id": item_id
            })
        
        @staticmethod
        def get_info(item_id: str) -> Any:
            """Gets item information"""
            return EagleWebApi._make_request("item/info", params={
                "id": item_id
            })
        
        @staticmethod
        def add_bookmark(url: str, name: str, base64: Optional[str] = None,
                        tags: Optional[List[str]] = None, modification_time: Optional[int] = None,
                        folder_id: Optional[str] = None) -> Any:
            """Adds bookmark item"""
            return EagleWebApi._make_request("item/addBookmark", "POST", {
                "url": url,
                "name": name,
                "base64": base64,
                "tags": tags,
                "modificationTime": modification_time,
                "folderId": folder_id
            })
        
        @staticmethod
        def add_from_url(url: str, name: str, website: Optional[str] = None,
                        tags: Optional[List[str]] = None, star: Optional[int] = None,
                        annotation: Optional[str] = None, modification_time: Optional[int] = None,
                        folder_id: Optional[str] = None, headers: Optional[Dict[str, Any]] = None) -> Any:
            """Adds item from URL"""
            return EagleWebApi._make_request("item/addFromUrl", "POST", {
                "url": url,
                "name": name,
                "website": website,
                "tags": tags,
                "star": star,
                "annotation": annotation,
                "modificationTime": modification_time,
                "folderId": folder_id,
                "headers": headers
            })
        
        @staticmethod
        def add_from_path(path: str, name: str, website: Optional[str] = None,
                         annotation: Optional[str] = None, tags: Optional[List[str]] = None,
                         folder_id: Optional[str] = None) -> Any:
            """Adds item from file path"""
            return EagleWebApi._make_request("item/addFromPath", "POST", {
                "path": path,
                "name": name,
                "website": website,
                "annotation": annotation,
                "tags": tags,
                "folderId": folder_id
            })
        
        @staticmethod
        def add_from_urls(items: List[Dict[str, Any]], folder_id: Optional[str] = None) -> Any:
            """Adds multiple items from URLs"""
            return EagleWebApi._make_request("item/addFromURLs", "POST", {
                "items": items,
                "folderId": folder_id
            })
    
    # Create class-level aliases for easier access
    application = _Application()
    folder = _Folder()
    library = _Library()
    item = _Item()
