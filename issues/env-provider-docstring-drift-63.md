---
title: "Docstring drift between config/providers/env.py and env.pyi for EnvProvider"
issue_number: 63
issue_url: "https://github.com/Leikaab/apiconfig/issues/63"
labels: [documentation]
created: 2025-04-20
location: "apiconfig/config/providers/env.py, apiconfig/config/providers/env.pyi"
---

## Summary
The `apiconfig/config/providers/env.pyi` stub provides a class-level docstring and detailed method docstrings for `EnvProvider`, including argument and return value descriptions, and raised exceptions. The implementation file `env.py` has no class-level or method docstrings. This leads to incomplete runtime documentation and can confuse users and maintainers.

## Evidence
```python
# apiconfig/config/providers/env.py
class EnvProvider:
    # No class-level or method docstrings

# apiconfig/config/providers/env.pyi
class EnvProvider:
    """
    Loads configuration values from environment variables.

    Looks for environment variables starting with a specific prefix (defaulting
    to "APICONFIG_"), strips the prefix, converts the remaining key to lowercase,
    and attempts basic type inference (int, bool, float, str).
    """

    def __init__(self, prefix: str = "APICONFIG_") -> None:
        """
        Initializes the provider with a specific prefix.

        Args:
            prefix: The prefix to look for in environment variable names.
        """
        ...

    def load(self) -> Dict[str, Any]:
        """
        Loads configuration from environment variables matching the prefix.

        Returns:
            A dictionary containing the loaded configuration key-value pairs.

        Raises:
            InvalidConfigError: If a value intended as an integer cannot be parsed.
        """
        ...
```

## Impact
- Users relying on runtime docstrings or auto-generated documentation will not see the full contract or expected behavior.
- Increases the risk of misuse or misunderstanding of the `EnvProvider` class.
- Creates a maintenance burden and potential for further drift.

## Suggested Direction
- Add a class-level docstring and detailed method docstrings to `env.py` to match the `.pyi` stub, including argument and return value descriptions, and raised exceptions.
- Ensure future changes to documentation are made in both files.

## Related
- See other findings on .py ↔ .pyi drift, if any.
- Project documentation and type hinting guidelines.