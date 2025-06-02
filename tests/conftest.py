import os
import sys

# Add project root to sys.path for apiconfig imports, but prevent test modules
# from being importable as top-level to avoid mypy module name conflicts
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
