import json
from pathlib import Path
from typing import Optional, Dict, List, Union


class UrlManager:
    """
    Object-oriented UrlManager with modular URL components and legacy support.
    Checks JSON file once during initialization and auto-saves modifications.
    """

    # NEEDS TO FIX ABSOULUTE PATH
    def __init__(self, json_path: Optional[str] = None) -> None:
        self.json_path: Path = Path(json_path or r"C:\Users\a\Desktop\ListAnalize\app\lexicon\urls\list_am\list_am_url.json")
        self.urls: Dict[str, Union[str, Dict[str, Union[str, Dict[str, List[str]]]]]] = {}
        self._active: bool = True

        # Load or create JSON once
        if self.json_path.exists():
            self._load_urls()
        else:
            self.urls = {}
            self._save_urls()

    # --- Internal helpers ---
    def _load_urls(self) -> None:
        """Load URLs from JSON file."""
        with open(self.json_path, "r", encoding="utf-8") as f:
            try:
                data: Union[Dict, None] = json.load(f)
                if isinstance(data, dict):
                    self.urls = data  # type: ignore
                else:
                    self.urls = {}
            except json.JSONDecodeError:
                self.urls = {}

    def _save_urls(self) -> None:
        """Save URLs to JSON file."""
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(self.urls, f, indent=4)

    # --- Lifecycle methods ---
    def close(self, save: bool = True) -> None:
        """
        Gracefully close the manager.
        If `save=True`, saves URLs before closing.
        """
        if not self._active:
            return
        if save:
            self._save_urls()
        self._active = False
        self.urls.clear()

    # --- Core methods ---

    # NEEDS TO FIX OUTPUT
    def add_url(
        self,
        key: str,
        base_or_full: str,
        components: Optional[Dict[str, List[str]]] = None
    ) -> str:
        """Add or update a URL entry and auto-save."""
        if not self._active:
            raise RuntimeError("UrlManager is closed.")
        is_new: bool = key not in self.urls
        if components:
            self.urls[key] = {"base": base_or_full, "components": components}
        else:
            self.urls[key] = base_or_full
        self._save_urls()
        return "Added" if is_new else "Already exists"

    def remove_url(self, key: str) -> bool:
        """Remove a URL entry and auto-save."""
        if not self._active:
            raise RuntimeError("UrlManager is closed.")
        if key in self.urls:
            del self.urls[key]
            self._save_urls()
            return True
        return False

    def get_url(self, key: str, **kwargs: str) -> Optional[str]:
        """
        Get full URL using component keyword arguments.
        Example: get_url("example_com", language="en", category="4")
        """
        if not self._active:
            raise RuntimeError("UrlManager is closed.")

        entry: Union[str, Dict[str, Union[str, Dict[str, List[str]]]], None] = self.urls.get(key)
        if not entry:
            return None

        # Legacy full URL
        if isinstance(entry, str):
            return entry

        # Modular URL
        base: Optional[str] = entry.get("base")
        components: Dict[str, List[str]] = entry.get("components", {})

        if not base:
            return None

        path_segments: List[str] = [str(kwargs[comp]) for comp in components.keys() if comp in kwargs]
        return f"{base}/{'/'.join(path_segments)}" if path_segments else base

    def get_all_urls(self) -> Dict[str, Union[str, Dict[str, Union[str, Dict[str, List[str]]]]]]:
        """Return a copy of all URLs."""
        if not self._active:
            raise RuntimeError("UrlManager is closed.")
        return self.urls.copy()
