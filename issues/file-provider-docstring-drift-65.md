---
github_issue_number: 65
github_issue_url: https://github.com/Leikaab/apiconfig/issues/65
github_issue_id: I_kwDOObjluc6zNukT
github_issue_state: OPEN
github_issue_author: Leikaab
github_issue_author_id: MDQ6VXNlcjQ5NzkxNzAx
github_issue_created_at: 2025-04-20T00:22:44Z
github_issue_updated_at: 2025-04-20T00:22:44Z
---

---
title: "Docstring drift between config/providers/file.py and file.pyi for FileProvider"
severity: medium
location: "apiconfig/config/providers/file.py, apiconfig/config/providers/file.pyi"
---

## Summary
The `apiconfig/config/providers/file.pyi` stub provides a class-level docstring and detailed method docstrings for `FileProvider`, including argument and return value descriptions, and raised exceptions. The implementation file `file.py` has no class-level or method docstrings. This leads to incomplete runtime documentation and can confuse users and maintainers.

## Evidence
```python
# apiconfig/config/providers/file.py
class FileProvider:
    # No class-level or method docstrings

# apiconfig/config/providers/file.pyi
class FileProvider:
    """
    Loads configuration data from a file.

    Currently supports JSON files.
    """

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
```

## Impact
- Users relying on runtime docstrings or auto-generated documentation will not see the full contract or expected behavior.
- Increases the risk of misuse or misunderstanding of the `FileProvider` class.
- Creates a maintenance burden and potential for further drift.

## Suggested Direction
- Add a class-level docstring and detailed method docstrings to `file.py` to match the `.pyi` stub, including argument and return value descriptions, and raised exceptions.
- Ensure future changes to documentation are made in both files.

## Related
- See other findings on .py ↔ .pyi drift, if any.
- Project documentation and type hinting guidelines.