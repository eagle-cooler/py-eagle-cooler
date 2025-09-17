
from eagle_cooler import EagleWebApi

from eagle_cooler.model import FolderModel, ItemModel
from .core import EagleCoolerCore

class EagleContext:
    def get_selected_folder_ids(self) -> list[str]:
        """Get selected folder IDs from the context if available"""
        return EagleCoolerCore.selected_folder_ids()

    def get_selected_item_ids(self) -> list[str]:
        """Get selected item IDs from the context if available"""
        return EagleCoolerCore.selected_item_ids()
    
    def get_selected_folders(self) -> list[FolderModel]:
        folder_ids = self.get_selected_folder_ids()
        if not folder_ids:
            return []
        
        all_folders = EagleWebApi.folder.list()
        return [folder for folder in all_folders if folder['id'] in folder_ids]

    def get_selected_items(self, throw : bool = False) -> list[ItemModel]:
        item_ids = self.get_selected_item_ids()
        if not item_ids:
            return []

        selected_items = []    
        for selected_item in item_ids:
            try:
                item_info = EagleWebApi.item.get_info(selected_item)
                if item_info:
                    selected_items.append(item_info)
                    continue
            except Exception as e:
                if throw:
                    raise e
                
                continue

        return selected_items

eagleContext = EagleContext()
            
__all__ = ["eagleContext"]