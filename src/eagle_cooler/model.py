from typing import TypedDict, Any


class FolderModel(TypedDict):
    """TypedDict model for Eagle folder structure"""
    id: str
    name: str
    description: str
    children: list[str]  # List of child folder IDs
    modificationTime: int  # Unix timestamp in milliseconds
    tags: list[str]
    extendTags: list[str]
    pinyin: str
    password: str
    passwordTips: str


class OCRModel(TypedDict):
    """TypedDict model for OCR data"""
    done: str
    text: str


class DetectionModel(TypedDict):
    """TypedDict model for object detection data"""
    done: str
    objects: list[Any]  # Object detection results


class ItemModel(TypedDict):
    """TypedDict model for Eagle item structure"""
    id: str
    name: str
    size: int  # File size in bytes
    btime: int  # Birth time (creation time) in milliseconds
    mtime: int  # File modification time in milliseconds
    ext: str  # File extension
    tags: list[str]
    folders: list[str]  # List of folder IDs this item belongs to
    isDeleted: bool
    url: str
    annotation: str
    modificationTime: int  # Eagle modification time in milliseconds
    noPreview: bool
    lastModified: int  # Last modified time in milliseconds
    ocr: OCRModel
    detection: DetectionModel

