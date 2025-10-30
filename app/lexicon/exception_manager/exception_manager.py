import json
from pathlib import Path
from typing import Optional, List, Dict


class ExceptionManager:
    """
    A class to manage exceptions stored in a JSON file with keys.

    Allows adding, removing, fetching, and listing exceptions by key.
    """
    def __init__(self, json_path: str):
        self.json_path = Path(json_path)
        self.exceptions: Dict[str, str] = {}
        self.load_exceptions()

    def load_exceptions(self) -> None:
        """Loads exceptions from the JSON file; initializes empty dict if file missing or invalid."""
        if self.json_path.exists():
            with open(self.json_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if isinstance(data, dict):
                        self.exceptions = data
                    else:
                        self.exceptions = {}
                except json.JSONDecodeError:
                    self.exceptions = {}
        else:
            self.exceptions = {}

    def save_exceptions(self) -> None:
        """Saves the current exceptions dictionary back to the JSON file."""
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(self.exceptions, f, indent=4)

    def add_exception(self, key: str, message: str) -> bool:
        """
        Adds an exception under a given key. Overwrites if key already exists.

        Args:
            key (str): Key for the exception.
            message (str): The exception message.

        Returns:
            bool: True if new key was added, False if overwritten.
        """
        is_new = key not in self.exceptions
        self.exceptions[key] = message
        self.save_exceptions()
        return is_new

    def remove_exception(self, key: str) -> bool:
        """
        Removes an exception by key.

        Args:
            key (str): Key of the exception to remove.

        Returns:
            bool: True if removed, False if key was not found.
        """
        if key in self.exceptions:
            del self.exceptions[key]
            self.save_exceptions()
            return True
        return False

    def get_exception(self, key: str) -> Optional[str]:
        """
        Retrieves an exception message by key.

        Args:
            key (str): The key of the exception.

        Returns:
            Optional[str]: Exception message if found, else None.
        """
        return self.exceptions.get(key)

    def get_all_exceptions(self) -> Dict[str, str]:
        """Returns a copy of all key → exception message pairs."""
        return self.exceptions.copy()

    def get_keys(self) -> List[str]:
        """Returns a list of all exception keys."""
        return list(self.exceptions.keys())
