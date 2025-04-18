# tripletex-python Library Overview

This document provides a high-level overview of the `tripletex-python` library structure and basic usage patterns.

## Core Components

The library is built upon a generic `crudclient` foundation and specialized components for Tripletex:

1.  **`crudclient`**:
    *   `Client`: Handles low-level HTTP requests, authentication, configuration loading, and basic error handling (like 403 retries).
    *   `Crud`: A generic base class for defining RESTful API endpoints. It provides standard methods (`list`, `create`, `read`, `update`, `partial_update`, `destroy`) and handles endpoint path construction, request data serialization (using Pydantic models), and response data deserialization/validation (also using Pydantic).

2.  **`tripletex/core`**:
    *   `TripletexClient`: Inherits from `crudclient.Client` and configures it specifically for the Tripletex API (e.g., base URL, authentication methods via `TripletexConfig`).
    *   `TripletexCrud`: Inherits from `crudclient.Crud` and adapts it to Tripletex API conventions. Key adaptations include:
        *   Expecting list results within a `values` key in the JSON response.
        *   Expecting single resource results within a `value` key.
        *   Using Pydantic models with `by_alias=True` for serialization to match Tripletex's JSON field names (often camelCase).
        *   Allowing separate Pydantic models for creating (`_create_model`) and updating (`_update_model`) resources.
    *   `TripletexAPI`: The main entry point for interacting with the library. It initializes the `TripletexClient` and registers instances of all available endpoint classes (e.g., `TripletexSuppliers`, `TripletexActivities`) as attributes.

3.  **`tripletex/endpoints/<resource>`**:
    *   Each directory represents a specific Tripletex API resource (e.g., `supplier`, `project`, `activity`).
    *   `crud.py`: Contains the endpoint class (e.g., `TripletexSuppliers`) inheriting from `TripletexCrud`. It defines the specific `_resource_path` (e.g., `"supplier"`), the Pydantic models to use (`_datamodel`, `_create_model`, `_update_model`), and the `allowed_actions`.
    *   `models.py`: Contains the Pydantic models defining the data structure for the resource, including variations for creation and updates. These models use `Field(alias="...")` to map Python snake_case attributes to Tripletex's camelCase JSON fields.

## Basic Usage

1.  **Initialization**: Create an instance of `TripletexAPI`. It automatically handles client configuration (loading from environment variables via `TripletexConfig` by default).

    ```python
    from tripletex import TripletexAPI

    # Initialize the API client
    api = TripletexAPI()
    ```

2.  **Accessing Endpoints**: Access specific API resources via attributes on the `api` object. These attributes correspond to the endpoint classes registered in `TripletexAPI._register_endpoints`.

    ```python
    # Access the suppliers endpoint
    suppliers_endpoint = api.suppliers

    # Access the activities endpoint
    activities_endpoint = api.activities
    ```

3.  **Performing Operations**: Call the standard CRUD methods on the endpoint instance.

    ```python
    # List suppliers (example)
    try:
        all_suppliers = suppliers_endpoint.list(params={"count": 10})
        for supplier in all_suppliers:
            print(f"Supplier ID: {supplier.id}, Name: {supplier.name}")
    except Exception as e:
        print(f"Error listing suppliers: {e}")

    # Read a specific supplier (example)
    try:
        supplier_id = 12345
        specific_supplier = suppliers_endpoint.read(resource_id=supplier_id)
        print(f"Read Supplier: {specific_supplier.name}")
    except Exception as e:
        print(f"Error reading supplier {supplier_id}: {e}")
    ```

Refer to the subsequent documents for details on specific CRUD operations, Pydantic model usage, and other features.