# Pydantic Models in tripletex-python

Pydantic models play a crucial role in `tripletex-python` for data validation, serialization, and providing type hints. They ensure data conforms to the expected structure before sending requests and after receiving responses.

## Role of Models

1.  **Response Deserialization & Validation**: When the library receives a JSON response from the Tripletex API, it uses the Pydantic model defined in the endpoint's `_datamodel` attribute (e.g., `Supplier` in `TripletexSuppliers`) to parse and validate the data. This converts the JSON dictionary into a Python object with type-checked attributes. The `TripletexCrud` base class specifically looks for data within the `value` key for single objects and `values` key for lists.
2.  **Request Serialization & Validation**: When you provide data for `create`, `update`, or `partial_update` operations (either as a dictionary or a Pydantic model instance), the library uses the corresponding model (`_create_model` or `_update_model`, falling back to `_datamodel`) to validate the input. It then serializes the validated model instance into a JSON dictionary suitable for the request body using `model_dump()`.
3.  **Type Hinting & Autocompletion**: Using Pydantic models provides excellent type hinting, enabling better static analysis and autocompletion in IDEs.

## Defining Models (`models.py`)

Each endpoint directory (e.g., `tripletex/endpoints/supplier/`) has a `models.py` file where Pydantic models for that resource are defined.

### Key Considerations:

*   **Base Model**: Models typically inherit from `pydantic.BaseModel`.
*   **Field Aliases**: Tripletex API uses camelCase field names in JSON, while Python prefers snake_case. Use `pydantic.Field(alias="...")` to map Python attribute names to JSON field names.
    ```python
    from pydantic import BaseModel, Field

    class Supplier(BaseModel):
        # Python attribute: snake_case
        organization_number: Optional[str] = Field(None, alias="organizationNumber") # JSON field: camelCase
        supplier_number: int = Field(..., alias="supplierNumber")
        # Add other fields as needed
    ```
*   **Configuration**: Use `model_config = ConfigDict(populate_by_name=True)` to allow initialization using either the Python attribute name or the JSON alias.
    ```python
    from pydantic import BaseModel, ConfigDict, Field

    class Supplier(BaseModel):
        # Define fields here
        supplier_number: int = Field(..., alias="supplierNumber")
        name: str
        # Add other fields as needed

        model_config = ConfigDict(populate_by_name=True)

    # Can initialize using either name:
    s1 = Supplier(supplier_number=123, name="Example") # Add other required fields
    s2 = Supplier(supplierNumber=123, name="Example") # Also works because of populate_by_name=True
    ```
*   **Separate Create/Update Models**: Often, the data required or allowed for creating a resource differs from updating it. Define separate models (e.g., `SupplierCreate`, `SupplierUpdate`) inheriting from `BaseModel` for these operations. These models typically include only the fields relevant to that specific operation.
    ```python
    # models.py
    class SupplierCreate(BaseModel):
        name: str
        email: Optional[str] = None
        # Only fields needed/allowed for creation

    class SupplierUpdate(BaseModel):
        name: Optional[str] = None # Fields are optional for partial updates
        email: Optional[str] = None
        # Only fields allowed for update
    ```
*   **Nested Models**: If the API response includes nested objects, define corresponding Pydantic models for those nested structures and use them as type hints in the parent model (e.g., `currency: IdUrl`).
*   **Response Wrapper**: Sometimes the API wraps the list result in a larger structure with metadata (like pagination). A model inheriting `TripletexResponse[YourModel]` (e.g., `SupplierResponse(TripletexResponse[Supplier])`) can be defined to handle this, although the `TripletexCrud` base class often handles extracting the `values` list directly.

## Using Models

*   **Input**: When calling `create`, `update`, or `partial_update`, you can pass either a dictionary matching the expected structure or an instance of the corresponding Pydantic model (`_create_model` or `_update_model`). Using model instances is generally preferred for better type safety and autocompletion.
    ```python
    # Using a model instance (preferred)
    new_supplier_data = SupplierCreate(name="Supplier X", email="x@example.com")
    created = api.suppliers.create(data=new_supplier_data)

    # Using a dictionary
    update_data = {"name": "Supplier Y"}
    updated = api.suppliers.partial_update(resource_id=123, data=update_data)
    ```
*   **Output**: Methods like `list`, `read`, `create`, `update`, and `partial_update` typically return instances of the `_datamodel` (e.g., `Supplier`) or a list of them. You can access their attributes directly.
    ```python
    supplier = api.suppliers.read(resource_id=123)
    print(supplier.name)
    print(supplier.organization_number) # Access using Python name
    ```

## Serialization (`model_dump`)

The library automatically calls `model_dump(mode='json', by_alias=True, exclude_unset=...)` on your input models before sending the request.
*   `mode='json'`: Ensures data types are JSON-compatible.
*   `by_alias=True`: Uses the defined field aliases (camelCase) in the output JSON.
*   `exclude_unset=True`: Used implicitly for `partial_update` (via the `_dump_data` logic in `TripletexCrud` when using `_update_model`) to only include fields that were explicitly set in the input model/dict, which is essential for PATCH requests. For `create` and `update` (PUT), `exclude_unset` is effectively `False` to include all fields.