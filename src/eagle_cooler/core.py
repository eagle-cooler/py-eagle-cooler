import json
import os
import requests
from typing import Optional

class EagleCoolerCore:
    __fullBridgeContext = None
    __token = None
    __applicationInfo = None
    
    @classmethod
    def __load(cls):
        # Load context when class is defined
        try:
            context_env = os.environ.get("POWEREAGLE_CONTEXT")
            if context_env:
                cls.__fullBridgeContext = json.loads(context_env)
                cls.__token = cls.__fullBridgeContext.get("apiToken")
                return  # Successfully loaded, exit early
        except Exception as e:
            print(f"Failed to load Power Eagle context: {e}")
          
        # Fallback to Eagle API if Power Eagle context failed
        try:
            response = requests.get("http://localhost:41595/api/application/info", timeout=5)
            if response.status_code == 200:
                cls.__applicationInfo = response.json()
                token = cls.__applicationInfo.get("data", {}).get("preferences", {}).get("developer", {}).get("apiToken")
                if token:
                    cls.__token = token
        except Exception as api_error:
            print(f"Failed to get token from Eagle API: {api_error}")
            cls.__token = None

    @classmethod
    def token(cls) -> Optional[str]:
        """Get API token"""
        return cls.__token
    
    @classmethod
    def selected_item_ids(cls) -> Optional[list]:
        """Get selected items from the context if available"""
        if cls.__fullBridgeContext:
            return cls.__fullBridgeContext.get("selected").get("items")
        return None
    
    @classmethod
    def selected_folder_ids(cls) -> Optional[list]:
        """Get selected folders from the context if available"""
        if cls.__fullBridgeContext:
            return cls.__fullBridgeContext.get("selected").get("folders")
        return None
    
EagleCoolerCore._EagleCoolerCore__load()

