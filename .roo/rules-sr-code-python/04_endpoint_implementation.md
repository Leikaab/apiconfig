# Implementing New Endpoints

Adding support for a new Tripletex API endpoint involves creating a specific endpoint class that inherits from `TripletexCrud` and defining associated Pydantic models.

## Steps

1.  **Create Directory**: Create a new directory under `tripletex/endpoints/` named after the resource (e.g., `tripletex/endpoints/new_resource/`).
2.  **Define Models (`models.py`)**:
    *   Create a `models.py` file in the new directory.
    *   Define the main Pydantic model representing the resource data returned by the API (e.g., `NewResource`). Use `Field(alias="...")` for camelCase mapping. Include `model_config = ConfigDict(populate_by_name=True)`.
    *   Define separate models for create (`NewResourceCreate`) and update (`NewResourceUpdate`) operations if their structure differs from the main model. These usually contain a subset of fields, potentially with different optionality.
    *   Optionally, define a response wrapper model (e.g., `NewResourceResponse(TripletexResponse[NewResource])`) if the API wraps list results in metadata beyond the standard `values` key.
3.  **Define Endpoint Class (`crud.py`)**:
    *   Create a `crud.py` file in the new directory.
    *   Define the endpoint class, inheriting from `TripletexCrud[YourMainModel]` (e.g., `class TripletexNewResources(TripletexCrud[NewResource]):`).
    *   Set the required class attributes:
        *   `_resource_path`: The URL path segment for this resource (e.g., `"new-resource"`).
        *   `_datamodel`: The main Pydantic model (e.g., `NewResource`).
    *   Set optional class attributes as needed:
        *   `_create_model`: The Pydantic model for create operations (e.g., `NewResourceCreate`).
        *   `_update_model`: The Pydantic model for update/partial_update operations (e.g., `NewResourceUpdate`).
        *   `_api_response_model`: The response wrapper model if defined (e.g., `NewResourceResponse`).
        *   `allowed_actions`: A list of permitted standard CRUD operations (e.g., `["list", "read", "create"]`). If not set, it defaults to all standard actions defined in `Crud`.
        *   `_list_return_keys`: Defaults to `['values']` in `TripletexCrud`. Only override if the API uses a different key for lists for this specific endpoint.
4.  **Register Endpoint (`tripletex/core/api.py`)**:
    *   Import the new endpoint class in `tripletex/core/api.py`.
    *   In the `TripletexAPI._register_endpoints` method, instantiate the new class, passing `self.client`, and assign it to a descriptive attribute name on `self`.
        ```python
        # tripletex/core/api.py
        from tripletex.endpoints.new_resource.crud import TripletexNewResources
        # ... other imports

        class TripletexAPI(API):
            # ... client_class, __init__ ...

            def _register_endpoints(self):
                # ... other endpoints ...
                self.new_resources = TripletexNewResources(self.client) # Register the new endpoint
        ```
5.  **Add Stub Files (`.pyi`)**: Create corresponding `.pyi` files for `models.py` and `crud.py` with type hints and docstrings. This ensures proper type checking and interface definition.

## Example (`Supplier` Endpoint)

This example illustrates the files and code structure for the existing `Supplier` endpoint.
**`tripletex/endpoints/supplier/models.py`**:

```python
from pydantic import BaseModel, ConfigDict, Field
# ... other imports

class Supplier(BaseModel):
    id: int
    name: str
    organization_number: Optional[str] = Field(None, alias="organizationNumber")
    # ... other fields ...
    model_config = ConfigDict(populate_by_name=True)

class SupplierCreate(BaseModel):
    name: str
    email: Optional[str] = None

class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class SupplierResponse(TripletexResponse[Supplier]):
    pass
```

**`tripletex/endpoints/supplier/crud.py`**:

```python
from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.supplier.models import Supplier, SupplierCreate, SupplierResponse, SupplierUpdate

class TripletexSuppliers(TripletexCrud[Supplier]):
    _resource_path = "supplier"      # URL path
    _datamodel = Supplier            # Model for read/list responses
    _create_model = SupplierCreate   # Model for create input
    _update_model = SupplierUpdate   # Model for update/partial_update input
    _api_response_model = SupplierResponse # Optional: Wrapper for list response
    allowed_actions = ["list", "read", "create", "update", "destroy"] # Allowed ops
```

**`tripletex/core/api.py` (Registration Snippet)**:

```python
from tripletex.endpoints.supplier.crud import TripletexSuppliers
# ...

class TripletexAPI(API):
    # ...
    def _register_endpoints(self):
        # ...
        self.suppliers = TripletexSuppliers(self.client)
        # ...
```

By following these steps, you integrate a new Tripletex resource into the library, leveraging the validation, serialization, and standardized methods provided by the `crudclient` and `TripletexCrud` base classes.