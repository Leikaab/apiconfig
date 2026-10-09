# apiconfig.utils.endpoint_builder

## Module Description

Builds the path part of REST endpoints, such as `companies/acme/contacts/1`,
from a resource path, an optional prefix and an optional parent resource.
Configuration is declarative: subclass `EndpointBuilder` and set class
attributes, in the style of Django REST Framework serializers. API clients such
as `crudclient` use it to turn resource objects into request paths.

## Navigation

**Parent Module:** [apiconfig.utils](../README.md)

There are no submodules.

## Contents
- `builder.py` – the `EndpointBuilder` class.
- `validators.py` – `validate_path_segments`, which rejects wrong types and path traversal.
- `segments.py` – `build_resource_segments`, which turns a resource path and arguments into segments.
- `path_utils.py` – `join_path_segments`, which joins segments without a leading slash.
- `__init__.py` – re-exports the names above.

## Usage
```python
from apiconfig.utils.endpoint_builder import EndpointBuilder


class CompaniesBuilder(EndpointBuilder):
    resource_path = "companies"
    endpoint_prefix = ["api"]


class ContactsBuilder(EndpointBuilder):
    resource_path = "contacts"


contacts = ContactsBuilder(parent_builder=CompaniesBuilder())
contacts.build_endpoint(1, parent_args=["acme"])  # "api/companies/acme/contacts/1"
```

### Class attributes
| Attribute | Purpose |
| --------- | ------- |
| `resource_path` | The resource's own path segment, such as `"users"`. |
| `endpoint_prefix` | A string (`"a/b"`) or list of segments placed before the resource. |
| `prefix_mode` | `"override"` (default) uses the builder's own prefix, falling back to the parent's. `"append"` adds it after the parent's prefix. |

### Path rules
- A nested resource is placed under its parent's path, which already carries the
  parent's prefix, so prefixes are only added for resources without a parent.
- `None` and empty-string segments are accepted and left out of the path.
- Segments with `..` or a leading or trailing `/` raise `ValueError`; other types raise `TypeError`.
- Subclasses can override `get_prefix_segments(crud_instance)` to add dynamic
  segments, for example a company slug read from the resource object.

## Tests
```bash
poetry run pytest tests/unit/utils/endpoint_builder -q
```

## Status
**Stability:** Beta – moved from `crudclient.utils.endpoint_builder` in 0.3.4.
