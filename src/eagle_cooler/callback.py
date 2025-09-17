from typing import Optional, Dict, Any, List

# get script path
import os
import sys

from eagle_cooler.core import EagleCoolerCore

_script_path = os.path.join(os.getcwd(), "main.py")
_script_dir = os.getcwd()
_plugin_manifest = None
# check if plugin.json exists in parent _script_path
if os.path.exists(os.path.join(_script_dir, "plugin.json")):
    import json

    with open(
        os.path.join(_script_dir, "plugin.json"), "r", encoding="utf-8"
    ) as f:
        _plugin_manifest = json.load(f)

_stderr = sys.stderr


class EagleCallbackCore:
    """
    this class is used for PowerEagle python-script plugins to callback to the host plugin
    using stderr for handshake

    the signal being passed is $$${api token}$$${plugin id}$$${method to call}({varname}={value}, ...)(({map}))

    for example

    $$${api token}$$${plugin id}$$$folder.createSubfolder(parentId=123)((options))(name=New Folder)(description=This is a new folder)((options))

    will call
    await eagle.folder.createSubfolder(parentId=123, options={name: "New Folder", description: "This is a new folder"})
    """

    @staticmethod
    def _callback(method: str, kwargs: dict):
        if _plugin_manifest is None:
            raise Exception("plugin.json not found in script directory")
        plugin_id = _plugin_manifest.get("id")
        token = EagleCoolerCore.token()
        if token is None:
            raise Exception(
                "POWEREAGLE_CONTEXT environment variable not found, are you running inside PowerEagle?"
            )
        signal = f"$$${token}$$${plugin_id}$$${method}"
        for k, v in kwargs.items():
            if isinstance(v, dict):
                signal += f"(({k}))"
                for mk, mv in v.items():
                    signal += f"({mk}={mv})"
                signal += f"(({k}))"
            else:
                signal += f"({k}={v})"
        print(signal, file=_stderr)
        _stderr.flush()


# List of methods that return values and cannot be implemented with the callback system
METHODS_WITH_RETURN_VALUES = [
    # Tag methods
    "tag.get",
    "tag.get_recents",
    # TagGroup methods
    "tag_group.get",
    "tag_group.create",
    # Library methods
    "library.info",
    "library.get_name",
    "library.get_path",
    "library.get_modification_time",
    # Window methods
    "window.is_minimized",
    "window.is_maximized",
    "window.is_full_screen",
    "window.get_size",
    "window.get_bounds",
    "window.is_resizable",
    "window.is_always_on_top",
    "window.get_position",
    "window.get_opacity",
    # App methods
    "app.is_dark_colors",
    "app.get_path",
    "app.get_file_icon",
    "app.get_version",
    "app.get_build",
    "app.get_locale",
    "app.get_arch",
    "app.get_platform",
    "app.get_env",
    "app.get_exec_path",
    "app.get_pid",
    "app.is_windows",
    "app.is_mac",
    "app.is_running_under_arm64_translation",
    "app.get_theme",
    # OS methods
    "os.tmpdir",
    "os.version",
    "os.type",
    "os.release",
    "os.hostname",
    "os.homedir",
    "os.arch",
    # Screen methods
    "screen.get_cursor_screen_point",
    "screen.get_primary_display",
    "screen.get_all_displays",
    "screen.get_display_nearest_point",
    # Item methods
    "item.get",
    "item.get_all",
    "item.get_by_id",
    "item.get_by_ids",
    "item.get_selected",
    "item.add_from_url",
    "item.add_from_base64",
    "item.add_from_path",
    "item.add_bookmark",
    "item.open",
    # Folder methods
    "folder.create",
    "folder.create_subfolder",
    "folder.get",
    "folder.get_all",
    "folder.get_by_id",
    "folder.get_by_ids",
    "folder.get_selected",
    "folder.get_recents",
    # Dialog methods
    "dialog.show_open_dialog",
    "dialog.show_save_dialog",
    #"dialog.show_message_box",
    # Clipboard methods
    "clipboard.has",
    "clipboard.read_text",
    "clipboard.read_buffer",
    "clipboard.read_image",
    "clipboard.read_html",
]


class EagleCallback:
    """Python interface for Eagle native API methods"""

    class _Tag:
        """Tag-related API methods"""

        @staticmethod
        def get():
            """Returns all tags"""
            raise NotImplementedError(
                "tag.get returns data and cannot be used with callback system. Use EagleWebApi instead."
            )

        @staticmethod
        def get_recents():
            """Returns recently used tags"""
            raise NotImplementedError(
                "tag.get_recents returns data and cannot be used with callback system. Use EagleWebApi instead."
            )

    class _TagGroup:
        """TagGroup-related API methods"""

        @staticmethod
        def get():
            """Returns all tag groups"""
            raise NotImplementedError(
                "tag_group.get returns data and cannot be used with callback system. Use EagleWebApi instead."
            )

        @staticmethod
        def create(name: str, color: str, tags: List[str]):
            """Creates a new tag group - returns created group data"""
            raise NotImplementedError(
                "tag_group.create returns data and cannot be used with callback system. Use EagleWebApi instead."
            )

    class _Library:
        """Library-related API methods"""

        @staticmethod
        def info():
            """Gets library information"""
            raise NotImplementedError(
                "library.info returns data and cannot be used with callback system. Use EagleWebApi instead."
            )

        @staticmethod
        def get_name():
            """Gets library name"""
            raise NotImplementedError(
                "library.get_name returns data and cannot be used with callback system. Use EagleWebApi instead."
            )

        @staticmethod
        def get_path():
            """Gets library path"""
            raise NotImplementedError(
                "library.get_path returns data and cannot be used with callback system. Use EagleWebApi instead."
            )

        @staticmethod
        def get_modification_time():
            """Gets library modification time"""
            raise NotImplementedError(
                "library.get_modification_time returns data and cannot be used with callback system. Use EagleWebApi instead."
            )

    class _Window:
        """Window-related API methods"""

        @staticmethod
        def show():
            """Shows the window"""
            EagleCallbackCore._callback("window.show", {})

        @staticmethod
        def show_inactive():
            """Shows the window without focusing"""
            EagleCallbackCore._callback("window.showInactive", {})

        @staticmethod
        def hide():
            """Hides the window"""
            EagleCallbackCore._callback("window.hide", {})

        @staticmethod
        def focus():
            """Focuses the window"""
            EagleCallbackCore._callback("window.focus", {})

        @staticmethod
        def minimize():
            """Minimizes the window"""
            EagleCallbackCore._callback("window.minimize", {})

        @staticmethod
        def is_minimized():
            """Checks if window is minimized"""
            raise NotImplementedError(
                "window.is_minimized returns data and cannot be used with callback system."
            )

        @staticmethod
        def restore():
            """Restores the window"""
            EagleCallbackCore._callback("window.restore", {})

        @staticmethod
        def maximize():
            """Maximizes the window"""
            EagleCallbackCore._callback("window.maximize", {})

        @staticmethod
        def unmaximize():
            """Unmaximizes the window"""
            EagleCallbackCore._callback("window.unmaximize", {})

        @staticmethod
        def is_maximized():
            """Checks if window is maximized"""
            raise NotImplementedError(
                "window.is_maximized returns data and cannot be used with callback system."
            )

        @staticmethod
        def set_full_screen(flag: bool):
            """Sets fullscreen mode"""
            EagleCallbackCore._callback("window.setFullScreen", {"flag": flag})

        @staticmethod
        def is_full_screen():
            """Checks if window is in fullscreen"""
            raise NotImplementedError(
                "window.is_full_screen returns data and cannot be used with callback system."
            )

        @staticmethod
        def set_aspect_ratio(aspect_ratio: float):
            """Sets window aspect ratio"""
            EagleCallbackCore._callback(
                "window.setAspectRatio", {"aspectRatio": aspect_ratio}
            )

        @staticmethod
        def set_background_color(background_color: str):
            """Sets window background color"""
            EagleCallbackCore._callback(
                "window.setBackgroundColor", {"backgroundColor": background_color}
            )

        @staticmethod
        def set_size(width: int, height: int):
            """Sets window size"""
            EagleCallbackCore._callback(
                "window.setSize", {"width": width, "height": height}
            )

        @staticmethod
        def get_size():
            """Gets window size [width, height]"""
            raise NotImplementedError(
                "window.get_size returns data and cannot be used with callback system."
            )

        @staticmethod
        def set_bounds(bounds: Dict[str, int]):
            """Sets window bounds

            Args:
                bounds: Dictionary with x, y, width, height keys
            """
            EagleCallbackCore._callback("window.setBounds", {"bounds": bounds})

        @staticmethod
        def get_bounds():
            """Gets window bounds"""
            raise NotImplementedError(
                "window.get_bounds returns data and cannot be used with callback system."
            )

        @staticmethod
        def set_resizable(resizable: bool):
            """Sets if window is resizable"""
            EagleCallbackCore._callback("window.setResizable", {"resizable": resizable})

        @staticmethod
        def is_resizable():
            """Checks if window is resizable"""
            raise NotImplementedError(
                "window.is_resizable returns data and cannot be used with callback system."
            )

        @staticmethod
        def set_always_on_top(flag: bool):
            """Sets always on top flag"""
            EagleCallbackCore._callback("window.setAlwaysOnTop", {"flag": flag})

        @staticmethod
        def is_always_on_top():
            """Checks if window is always on top"""
            raise NotImplementedError(
                "window.is_always_on_top returns data and cannot be used with callback system."
            )

        @staticmethod
        def set_position(x: int, y: int):
            """Sets window position"""
            EagleCallbackCore._callback("window.setPosition", {"x": x, "y": y})

        @staticmethod
        def get_position():
            """Gets window position [x, y]"""
            raise NotImplementedError(
                "window.get_position returns data and cannot be used with callback system."
            )

        @staticmethod
        def set_opacity(opacity: float):
            """Sets window opacity (0.0 to 1.0)"""
            EagleCallbackCore._callback("window.setOpacity", {"opacity": opacity})

        @staticmethod
        def get_opacity():
            """Gets window opacity"""
            raise NotImplementedError(
                "window.get_opacity returns data and cannot be used with callback system."
            )

        @staticmethod
        def flash_frame(flag: bool):
            """Flashes the window frame"""
            EagleCallbackCore._callback("window.flashFrame", {"flag": flag})

        @staticmethod
        def set_ignore_mouse_events(ignore: bool):
            """Sets ignore mouse events"""
            EagleCallbackCore._callback(
                "window.setIgnoreMouseEvents", {"ignore": ignore}
            )

        @staticmethod
        def capture_page(rect: Optional[Dict[str, int]] = None):
            """Captures page screenshot"""
            kwargs = {}
            if rect:
                kwargs["rect"] = rect
            EagleCallbackCore._callback("window.capturePage", kwargs)

        @staticmethod
        def set_referer(url: str):
            """Sets referer URL"""
            EagleCallbackCore._callback("window.setReferer", {"url": url})

    class _App:
        """Application-related API methods"""

        @staticmethod
        def is_dark_colors():
            """Checks if using dark colors"""
            raise NotImplementedError(
                "app.is_dark_colors returns data and cannot be used with callback system."
            )

        @staticmethod
        def get_path(name: str):
            """Gets system path"""
            raise NotImplementedError(
                "app.get_path returns data and cannot be used with callback system."
            )

        @staticmethod
        def get_file_icon(path: str, size: str = "normal"):
            """Gets file icon"""
            raise NotImplementedError(
                "app.get_file_icon returns data and cannot be used with callback system."
            )

        @staticmethod
        def create_thumbnail_from_path(path: str, max_size: Dict[str, int]):
            """Creates thumbnail from path - action only, no return"""
            EagleCallbackCore._callback(
                "app.createThumbnailFromPath", {"path": path, "maxSize": max_size}
            )

        @staticmethod
        def get_version():
            """Gets app version"""
            raise NotImplementedError(
                "app.get_version returns data and cannot be used with callback system."
            )

        @staticmethod
        def get_build():
            """Gets app build number"""
            raise NotImplementedError(
                "app.get_build returns data and cannot be used with callback system."
            )

        @staticmethod
        def get_locale():
            """Gets app locale"""
            raise NotImplementedError(
                "app.get_locale returns data and cannot be used with callback system."
            )

        @staticmethod
        def get_arch():
            """Gets app architecture"""
            raise NotImplementedError(
                "app.get_arch returns data and cannot be used with callback system."
            )

        @staticmethod
        def get_platform():
            """Gets app platform"""
            raise NotImplementedError(
                "app.get_platform returns data and cannot be used with callback system."
            )

        @staticmethod
        def get_env():
            """Gets environment variables"""
            raise NotImplementedError(
                "app.get_env returns data and cannot be used with callback system."
            )

        @staticmethod
        def get_exec_path():
            """Gets executable path"""
            raise NotImplementedError(
                "app.get_exec_path returns data and cannot be used with callback system."
            )

        @staticmethod
        def get_pid():
            """Gets process ID"""
            raise NotImplementedError(
                "app.get_pid returns data and cannot be used with callback system."
            )

        @staticmethod
        def is_windows():
            """Checks if running on Windows"""
            raise NotImplementedError(
                "app.is_windows returns data and cannot be used with callback system."
            )

        @staticmethod
        def is_mac():
            """Checks if running on Mac"""
            raise NotImplementedError(
                "app.is_mac returns data and cannot be used with callback system."
            )

        @staticmethod
        def is_running_under_arm64_translation():
            """Checks if running under ARM64 translation"""
            raise NotImplementedError(
                "app.is_running_under_arm64_translation returns data and cannot be used with callback system."
            )

        @staticmethod
        def get_theme():
            """Gets current theme"""
            raise NotImplementedError(
                "app.get_theme returns data and cannot be used with callback system."
            )

    class _OS:
        """Operating system API methods"""

        @staticmethod
        def tmpdir():
            """Gets temporary directory"""
            raise NotImplementedError(
                "os.tmpdir returns data and cannot be used with callback system."
            )

        @staticmethod
        def version():
            """Gets OS version"""
            raise NotImplementedError(
                "os.version returns data and cannot be used with callback system."
            )

        @staticmethod
        def type():
            """Gets OS type"""
            raise NotImplementedError(
                "os.type returns data and cannot be used with callback system."
            )

        @staticmethod
        def release():
            """Gets OS release"""
            raise NotImplementedError(
                "os.release returns data and cannot be used with callback system."
            )

        @staticmethod
        def hostname():
            """Gets hostname"""
            raise NotImplementedError(
                "os.hostname returns data and cannot be used with callback system."
            )

        @staticmethod
        def homedir():
            """Gets home directory"""
            raise NotImplementedError(
                "os.homedir returns data and cannot be used with callback system."
            )

        @staticmethod
        def arch():
            """Gets OS architecture"""
            raise NotImplementedError(
                "os.arch returns data and cannot be used with callback system."
            )

    class _Screen:
        """Screen-related API methods"""

        @staticmethod
        def get_cursor_screen_point():
            """Gets cursor screen point"""
            raise NotImplementedError(
                "screen.get_cursor_screen_point returns data and cannot be used with callback system."
            )

        @staticmethod
        def get_primary_display():
            """Gets primary display info"""
            raise NotImplementedError(
                "screen.get_primary_display returns data and cannot be used with callback system."
            )

        @staticmethod
        def get_all_displays():
            """Gets all displays info"""
            raise NotImplementedError(
                "screen.get_all_displays returns data and cannot be used with callback system."
            )

        @staticmethod
        def get_display_nearest_point(point: Dict[str, int]):
            """Gets display nearest to point"""
            raise NotImplementedError(
                "screen.get_display_nearest_point returns data and cannot be used with callback system."
            )

    class _Notification:
        """Notification API methods"""

        @staticmethod
        def show(
            title: str,
            description: str,
            icon: Optional[str] = None,
            mute: Optional[bool] = None,
            duration: Optional[int] = None,
        ):
            """Shows notification

            Args:
                title: Notification title
                description: Notification description
                icon: Optional icon path
                mute: Optional mute flag
                duration: Optional duration in ms
            """
            options = {"title": title, "description": description}
            if icon is not None:
                options["icon"] = icon
            if mute is not None:
                options["mute"] = mute
            if duration is not None:
                options["duration"] = duration
            EagleCallbackCore._callback("notification.show", {"options": options})

    class _Event:
        """Event handling API methods"""

        @staticmethod
        def on_plugin_create(callback_name: str):
            """Register plugin create event callback"""
            EagleCallbackCore._callback(
                "event.onPluginCreate", {"callback": callback_name}
            )

        @staticmethod
        def on_plugin_run(callback_name: str):
            """Register plugin run event callback"""
            EagleCallbackCore._callback(
                "event.onPluginRun", {"callback": callback_name}
            )

        @staticmethod
        def on_plugin_before_exit(callback_name: str):
            """Register plugin before exit event callback"""
            EagleCallbackCore._callback(
                "event.onPluginBeforeExit", {"callback": callback_name}
            )

        @staticmethod
        def on_plugin_show(callback_name: str):
            """Register plugin show event callback"""
            EagleCallbackCore._callback(
                "event.onPluginShow", {"callback": callback_name}
            )

        @staticmethod
        def on_plugin_hide(callback_name: str):
            """Register plugin hide event callback"""
            EagleCallbackCore._callback(
                "event.onPluginHide", {"callback": callback_name}
            )

        @staticmethod
        def on_library_changed(callback_name: str):
            """Register library changed event callback"""
            EagleCallbackCore._callback(
                "event.onLibraryChanged", {"callback": callback_name}
            )

        @staticmethod
        def on_theme_changed(callback_name: str):
            """Register theme changed event callback"""
            EagleCallbackCore._callback(
                "event.onThemeChanged", {"callback": callback_name}
            )

    class _Item:
        """Item-related API methods"""

        @staticmethod
        def get(
            id: Optional[str] = None,
            ids: Optional[List[str]] = None,
            is_selected: Optional[bool] = None,
            is_untagged: Optional[bool] = None,
            is_unfiled: Optional[bool] = None,
            keywords: Optional[List[str]] = None,
            tags: Optional[List[str]] = None,
            folders: Optional[List[str]] = None,
            ext: Optional[str] = None,
            annotation: Optional[str] = None,
            rating: Optional[int] = None,
            url: Optional[str] = None,
            shape: Optional[str] = None,
        ):
            """Gets items with filters - returns data"""
            raise NotImplementedError(
                "item.get returns data and cannot be used with callback system. Use EagleWebApi instead."
            )

        @staticmethod
        def get_all():
            """Gets all items"""
            raise NotImplementedError(
                "item.get_all returns data and cannot be used with callback system. Use EagleWebApi instead."
            )

        @staticmethod
        def get_by_id(item_id: str):
            """Gets item by ID"""
            raise NotImplementedError(
                "item.get_by_id returns data and cannot be used with callback system. Use EagleWebApi instead."
            )

        @staticmethod
        def get_by_ids(item_ids: List[str]):
            """Gets items by IDs"""
            raise NotImplementedError(
                "item.get_by_ids returns data and cannot be used with callback system. Use EagleWebApi instead."
            )

        @staticmethod
        def get_selected():
            """Gets selected items"""
            raise NotImplementedError(
                "item.get_selected returns data and cannot be used with callback system. Use EagleWebApi instead."
            )

        @staticmethod
        def add_from_url(
            url: str,
            name: Optional[str] = None,
            website: Optional[str] = None,
            tags: Optional[List[str]] = None,
            folders: Optional[List[str]] = None,
            annotation: Optional[str] = None,
        ):
            """Adds item from URL - returns item ID"""
            raise NotImplementedError(
                "item.add_from_url returns data and cannot be used with callback system. Use EagleWebApi instead."
            )

        @staticmethod
        def add_from_base64(
            base64: str,
            name: Optional[str] = None,
            website: Optional[str] = None,
            tags: Optional[List[str]] = None,
            folders: Optional[List[str]] = None,
            annotation: Optional[str] = None,
        ):
            """Adds item from base64 - returns item ID"""
            raise NotImplementedError(
                "item.add_from_base64 returns data and cannot be used with callback system. Use EagleWebApi instead."
            )

        @staticmethod
        def add_from_path(
            path: str,
            name: Optional[str] = None,
            website: Optional[str] = None,
            tags: Optional[List[str]] = None,
            folders: Optional[List[str]] = None,
            annotation: Optional[str] = None,
        ):
            """Adds item from file path - returns item ID"""
            raise NotImplementedError(
                "item.add_from_path returns data and cannot be used with callback system. Use EagleWebApi instead."
            )

        @staticmethod
        def add_bookmark(
            url: str,
            name: Optional[str] = None,
            base64: Optional[str] = None,
            tags: Optional[List[str]] = None,
            folders: Optional[List[str]] = None,
            annotation: Optional[str] = None,
        ):
            """Adds bookmark - returns item ID"""
            raise NotImplementedError(
                "item.add_bookmark returns data and cannot be used with callback system. Use EagleWebApi instead."
            )

        @staticmethod
        def open(item_id: str):
            """Opens item - returns success status"""
            raise NotImplementedError(
                "item.open returns data and cannot be used with callback system."
            )

    class _Folder:
        """Folder-related API methods"""

        @staticmethod
        def create(
            name: str, description: Optional[str] = None, parent: Optional[str] = None
        ):
            """Creates folder - returns folder data"""
            raise NotImplementedError(
                "folder.create returns data and cannot be used with callback system. Use EagleWebApi instead."
            )

        @staticmethod
        def create_subfolder(
            parent_id: str, name: str, description: Optional[str] = None
        ):
            """Creates subfolder - returns folder data"""
            raise NotImplementedError(
                "folder.create_subfolder returns data and cannot be used with callback system. Use EagleWebApi instead."
            )

        @staticmethod
        def get(
            id: Optional[str] = None,
            ids: Optional[List[str]] = None,
            is_selected: Optional[bool] = None,
            is_recent: Optional[bool] = None,
        ):
            """Gets folders with filters"""
            raise NotImplementedError(
                "folder.get returns data and cannot be used with callback system. Use EagleWebApi instead."
            )

        @staticmethod
        def get_all():
            """Gets all folders"""
            raise NotImplementedError(
                "folder.get_all returns data and cannot be used with callback system. Use EagleWebApi instead."
            )

        @staticmethod
        def get_by_id(folder_id: str):
            """Gets folder by ID"""
            raise NotImplementedError(
                "folder.get_by_id returns data and cannot be used with callback system. Use EagleWebApi instead."
            )

        @staticmethod
        def get_by_ids(folder_ids: List[str]):
            """Gets folders by IDs"""
            raise NotImplementedError(
                "folder.get_by_ids returns data and cannot be used with callback system. Use EagleWebApi instead."
            )

        @staticmethod
        def get_selected():
            """Gets selected folders"""
            raise NotImplementedError(
                "folder.get_selected returns data and cannot be used with callback system. Use EagleWebApi instead."
            )

        @staticmethod
        def get_recents():
            """Gets recent folders"""
            raise NotImplementedError(
                "folder.get_recents returns data and cannot be used with callback system. Use EagleWebApi instead."
            )

        @staticmethod
        def open(folder_id: str):
            """Opens folder - action only"""
            EagleCallbackCore._callback("folder.open", {"folderId": folder_id})

    class _ContextMenu:
        """Context menu API methods"""

        @staticmethod
        def open(menu_items: List[Dict[str, Any]]):
            """Opens context menu

            Args:
                menu_items: List of menu item dictionaries with id, label, click, submenu
            """
            EagleCallbackCore._callback("contextMenu.open", {"menuItems": menu_items})

    class _Dialog:
        """Dialog API methods"""

        @staticmethod
        def show_open_dialog(
            title: Optional[str] = None,
            default_path: Optional[str] = None,
            button_label: Optional[str] = None,
            filters: Optional[List[Dict[str, Any]]] = None,
            properties: Optional[List[str]] = None,
            message: Optional[str] = None,
        ):
            """Shows open dialog - returns result"""
            raise NotImplementedError(
                "dialog.show_open_dialog returns data and cannot be used with callback system."
            )

        @staticmethod
        def show_save_dialog(
            title: Optional[str] = None,
            default_path: Optional[str] = None,
            button_label: Optional[str] = None,
            filters: Optional[List[Dict[str, Any]]] = None,
            properties: Optional[List[str]] = None,
        ):
            """Shows save dialog - returns result"""
            raise NotImplementedError(
                "dialog.show_save_dialog returns data and cannot be used with callback system."
            )

        @staticmethod
        def show_message_box(
            message: str,
            title: Optional[str] = None,
            detail: Optional[str] = None,
            buttons: Optional[List[str]] = None,
            type: Optional[str] = None,
        ):
            """Shows message box - returns button response"""
            EagleCallbackCore._callback(
                "dialog.showMessageBox",
                {
                    "message": message,
                    "title": title,
                    "detail": detail,
                    "buttons": buttons,
                    "type": type,
                },
            )

        @staticmethod
        def show_error_box(title: str, content: str):
            """Shows error box - action only"""
            EagleCallbackCore._callback(
                "dialog.showErrorBox", {"title": title, "content": content}
            )

    class _Clipboard:
        """Clipboard API methods"""

        @staticmethod
        def clear():
            """Clears clipboard"""
            EagleCallbackCore._callback("clipboard.clear", {})

        @staticmethod
        def has(format: str):
            """Checks if clipboard has format - returns boolean"""
            raise NotImplementedError(
                "clipboard.has returns data and cannot be used with callback system."
            )

        @staticmethod
        def write_text(text: str):
            """Writes text to clipboard - action only"""
            EagleCallbackCore._callback("clipboard.writeText", {"text": text})

        @staticmethod
        def read_text():
            """Reads text from clipboard - returns text"""
            raise NotImplementedError(
                "clipboard.read_text returns data and cannot be used with callback system."
            )

        @staticmethod
        def write_buffer(format: str, buffer: bytes):
            """Writes buffer to clipboard - action only"""
            EagleCallbackCore._callback(
                "clipboard.writeBuffer", {"format": format, "buffer": buffer}
            )

        @staticmethod
        def read_buffer(format: str):
            """Reads buffer from clipboard - returns buffer"""
            raise NotImplementedError(
                "clipboard.read_buffer returns data and cannot be used with callback system."
            )

        @staticmethod
        def write_image(image: Dict[str, Any]):
            """Writes image to clipboard - action only"""
            EagleCallbackCore._callback("clipboard.writeImage", {"image": image})

        @staticmethod
        def read_image():
            """Reads image from clipboard - returns image"""
            raise NotImplementedError(
                "clipboard.read_image returns data and cannot be used with callback system."
            )

        @staticmethod
        def write_html(markup: str):
            """Writes HTML to clipboard - action only"""
            EagleCallbackCore._callback("clipboard.writeHTML", {"markup": markup})

        @staticmethod
        def read_html():
            """Reads HTML from clipboard - returns HTML"""
            raise NotImplementedError(
                "clipboard.read_html returns data and cannot be used with callback system."
            )

        @staticmethod
        def copy_files(paths: List[str]):
            """Copies files to clipboard - action only"""
            EagleCallbackCore._callback("clipboard.copyFiles", {"paths": paths})

    class _Drag:
        """Drag and drop API methods"""

        @staticmethod
        def start_drag(file_paths: List[str]):
            """Starts drag operation"""
            EagleCallbackCore._callback("drag.startDrag", {"filePaths": file_paths})

    class _Shell:
        """Shell API methods"""

        @staticmethod
        def beep():
            """Makes system beep"""
            EagleCallbackCore._callback("shell.beep", {})

        @staticmethod
        def open_external(url: str):
            """Opens URL externally"""
            EagleCallbackCore._callback("shell.openExternal", {"url": url})

        @staticmethod
        def open_path(path: str):
            """Opens file path"""
            EagleCallbackCore._callback("shell.openPath", {"path": path})

        @staticmethod
        def show_item_in_folder(path: str):
            """Shows item in folder"""
            EagleCallbackCore._callback("shell.showItemInFolder", {"path": path})

    class _Log:
        """Logging API methods"""

        @staticmethod
        def info(message: str):
            """Logs info message"""
            EagleCallbackCore._callback("log.info", {"message": message})

        @staticmethod
        def warn(message: str):
            """Logs warning message"""
            EagleCallbackCore._callback("log.warn", {"message": message})

        @staticmethod
        def error(message: str):
            """Logs error message"""
            EagleCallbackCore._callback("log.error", {"message": message})

        @staticmethod
        def debug(message: str):
            """Logs debug message"""
            EagleCallbackCore._callback("log.debug", {"message": message})

    # Create class-level aliases for easier access
    tag = _Tag()
    tag_group = _TagGroup()
    library = _Library()
    window = _Window()
    app = _App()
    os = _OS()
    screen = _Screen()
    notification = _Notification()
    event = _Event()
    item = _Item()
    folder = _Folder()
    context_menu = _ContextMenu()
    dialog = _Dialog()
    clipboard = _Clipboard()
    drag = _Drag()
    shell = _Shell()
    log = _Log()
