import pathlib
from typing import Any, Dict, Union

class FileProvider:
    """
    Loads configuration data from a file.

    Currently supports JSON files.
    """

    _file_path: pathlib.Path

    def __init__(self, file_path: Union[str, pathlib.Path]) -> None:
        """
        Initializes the FileProvider.

        Args:
            file_path: The path to the configuration file (string or Path object).
        """
        ...

    def load(self) -> Dict[str, Any]:
        """
        Loads configuration data from the specified file.

        Returns:
            A dictionary containing the configuration key-value pairs.

        Raises:
            ConfigLoadError: If the file cannot be found, read, decoded,
                             or if the file type is unsupported.
        """
        ...
