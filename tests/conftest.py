import os
import sys
from typing import Callable

# Add project root to sys.path for apiconfig imports, but prevent test modules
# from being importable as top-level to avoid mypy module name conflicts
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def envreturn(key: str, default: str | None = None) -> str | None:
    """Return environment variable or default value."""
    return os.environ.get(key, default)


# Use Codex secret() if available, fallback to os.environ (for local/dev)
secret: Callable[[str], str | None] = globals().get("secret", envreturn)

# Set secrets into env (noop locally if already present)
for key in [
    "TRIPLETEX_TEST_CONSUMER_TOKEN",
    "TRIPLETEX_TEST_EMPLOYEE_TOKEN",
    "FIKEN_ACCESS_TOKEN",
    "ONEFLOW_API_KEY",
    # legg til flere etter behov
]:
    val: str | None = secret(key)
    if val is not None:
        os.environ[key] = val
