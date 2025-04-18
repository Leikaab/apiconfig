# CRUD Operations in tripletex-python

The `TripletexCrud` base class (and its parent `crudclient.Crud`) provides standardized methods for performing Create, Read, Update, and Delete (CRUD) operations, plus listing.

## Common Parameters

*   `resource_id` (str): The unique identifier for a specific resource (used in `read`, `update`, `partial_update`, `destroy`).
*   `parent_id` (Optional[str]): The identifier of the parent resource, if the endpoint is nested (e.g., getting items for a specific order).
*   `params` (Optional[JSONDict]): A dictionary of query parameters to add to the request URL (commonly used in `list` operations for filtering, sorting, pagination, etc.).
*   `data` (Union[JSONDict, T]): The data payload for the request. This can be a Pydantic model instance (matching `_datamodel`, `_create_model`, or `_update_model`) or a dictionary. The library handles validation and serialization.

## Standard Methods

These methods are available on endpoint instances (e.g., `api.suppliers`).

### `list(parent_id: Optional[str] = None, params: Optional[JSONDict] = None) -> Union[JSONList, List[T], ApiResponse]`

*   **Purpose**: Retrieves a collection of resources.
*   **HTTP Method**: GET
*   **Endpoint**: Base resource path (e.g., `/supplier`) or nested path (e.g., `/order/123/item`).
*   **Parameters**:
    *   `parent_id`: Used for nested resources.
    *   `params`: Used for filtering, pagination (`from`, `count`), sorting, etc. Refer to Tripletex API documentation for available parameters for each endpoint.
*   **Returns**: Typically a list of Pydantic model instances (`List[T]`) extracted from the `values` key of the response. May return the raw `ApiResponse` model if defined and conversion fails or if the strategy dictates.

```python
# List first 10 suppliers
suppliers = api.suppliers.list(params={"count": 10})

# List activities after a certain date
activities = api.activities.list(params={"activityDateFrom": "2024-01-01"})
```

### `create(data: Union[JSONDict, T], parent_id: Optional[str] = None) -> Union[T, JSONDict]`

*   **Purpose**: Creates a new resource.
*   **HTTP Method**: POST
*   **Endpoint**: Base resource path (e.g., `/supplier`) or nested path.
*   **Parameters**:
    *   `data`: The data for the new resource (Pydantic model instance or dict). Validated against `_create_model` if defined, otherwise `_datamodel`.
    *   `parent_id`: Used for nested resources.
*   **Returns**: A Pydantic model instance (`T`) of the newly created resource, extracted from the `value` key of the response.

```python
from tripletex.endpoints.supplier.models import SupplierCreate

new_supplier_data = SupplierCreate(name="New Supplier Inc.", email="contact@newsupplier.com")
created_supplier = api.suppliers.create(data=new_supplier_data)
print(f"Created Supplier ID: {created_supplier.id}")
```

### `read(resource_id: str, parent_id: Optional[str] = None) -> Union[T, JSONDict]`

*   **Purpose**: Retrieves a single specific resource by its ID.
*   **HTTP Method**: GET
*   **Endpoint**: Resource path including ID (e.g., `/supplier/12345`).
*   **Parameters**:
    *   `resource_id`: The ID of the resource to retrieve.
    *   `parent_id`: Used for nested resources.
*   **Returns**: A Pydantic model instance (`T`) of the retrieved resource, extracted from the `value` key of the response.

```python
supplier_id = 12345
supplier = api.suppliers.read(resource_id=supplier_id)
print(f"Supplier Name: {supplier.name}")
```

### `update(resource_id: str, data: Union[JSONDict, T], parent_id: Optional[str] = None) -> Union[T, JSONDict]`

*   **Purpose**: Replaces an existing resource entirely with new data (full update).
*   **HTTP Method**: PUT
*   **Endpoint**: Resource path including ID (e.g., `/supplier/12345`).
*   **Parameters**:
    *   `resource_id`: The ID of the resource to update.
    *   `data`: The complete new data for the resource (Pydantic model instance or dict). Validated against `_update_model` if defined, otherwise `_datamodel`. All required fields must be present.
    *   `parent_id`: Used for nested resources.
*   **Returns**: A Pydantic model instance (`T`) of the updated resource, extracted from the `value` key of the response.

```python
from tripletex.endpoints.supplier.models import SupplierUpdate

supplier_id = 12345
update_data = SupplierUpdate(name="Updated Supplier Name", email="new@example.com") # Assuming SupplierUpdate requires name and email
updated_supplier = api.suppliers.update(resource_id=supplier_id, data=update_data)
print(f"Updated Supplier Name: {updated_supplier.name}")
```

### `partial_update(resource_id: str, data: Union[JSONDict, T], parent_id: Optional[str] = None) -> Union[T, JSONDict]`

*   **Purpose**: Modifies specific fields of an existing resource (partial update).
*   **HTTP Method**: PATCH
*   **Endpoint**: Resource path including ID (e.g., `/supplier/12345`).
*   **Parameters**:
    *   `resource_id`: The ID of the resource to update.
    *   `data`: A Pydantic model instance or dict containing only the fields to be changed. Validated against `_update_model` if defined (only provided fields are validated for type correctness).
    *   `parent_id`: Used for nested resources.
*   **Returns**: A Pydantic model instance (`T`) of the updated resource, extracted from the `value` key of the response.

```python
from tripletex.endpoints.supplier.models import SupplierUpdate

supplier_id = 12345
# Only update the email
partial_data = SupplierUpdate(email="latest@example.com")
updated_supplier = api.suppliers.partial_update(resource_id=supplier_id, data=partial_data)
print(f"Partially Updated Supplier Email: {updated_supplier.email}")
```

### `destroy(resource_id: str, parent_id: Optional[str] = None) -> None`

*   **Purpose**: Deletes a specific resource by its ID.
*   **HTTP Method**: DELETE
*   **Endpoint**: Resource path including ID (e.g., `/supplier/12345`).
*   **Parameters**:
    *   `resource_id`: The ID of the resource to delete.
    *   `parent_id`: Used for nested resources.
*   **Returns**: `None`. Raises an exception on failure.

```python
supplier_id = 12345
try:
    api.suppliers.destroy(resource_id=supplier_id)
    print(f"Supplier {supplier_id} deleted successfully.")
except Exception as e:
    print(f"Error deleting supplier {supplier_id}: {e}")
```

## Custom Actions

Some endpoints might have actions beyond standard CRUD. These are typically handled via the `custom_action` method (details in a separate document).

## Error Handling

Standard HTTP errors (4xx, 5xx) are raised as exceptions (e.g., `NotFoundError`, `BadRequestError`, `AuthenticationError`, `ServerError`) inheriting from `crudclient.exceptions.CrudClientError`. Data validation errors during request serialization or response deserialization raise `crudclient.exceptions.DataValidationError`.