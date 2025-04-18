# Nested Resources and Custom Actions

Beyond standard CRUD on top-level resources, `tripletex-python` supports interacting with nested resources and performing custom actions defined by the Tripletex API.

## Nested Resources

Some Tripletex resources are nested under others (e.g., accounting periods under ledger, items under orders). The library handles this relationship through the `parent` argument during endpoint initialization.

### Implementation

1.  **Parent Endpoint**: The parent resource endpoint (e.g., `TripletexLedger`) is defined as usual.
2.  **Child Endpoint**:
    *   Define the child endpoint class (e.g., `TripletexAccountingPeriod`) inheriting `TripletexCrud`.
    *   Set its `_resource_path` relative to the parent (e.g., `"accountingPeriod"`).
    *   Define its models (`_datamodel`, etc.).
3.  **Registration (`tripletex/core/api.py`)**:
    *   Instantiate the parent endpoint first (e.g., `self.ledger = TripletexLedger(self.client)`).
    *   Instantiate the child endpoint, passing **both** `self.client` and the parent instance via the `parent` argument (e.g., `self.ledger.accounting_period = TripletexAccountingPeriod(self.client, parent=self.ledger)`). Assign the child instance as an attribute of the parent instance.

### Usage

When calling CRUD methods on a nested endpoint instance, you often need to provide the `parent_id`.

```python
# Example: List accounting periods for a specific ledger (assuming ledger ID is 1)
# Access the nested endpoint via the parent instance
accounting_periods = api.ledger.accounting_period.list(parent_id="1")

# Example: Read a specific accounting period (ID 5) belonging to ledger 1
period = api.ledger.accounting_period.read(resource_id="5", parent_id="1")

# Example: Create a new accounting period under ledger 1
new_period_data = AccountingPeriodCreate(...) # Define data
created_period = api.ledger.accounting_period.create(data=new_period_data, parent_id="1")
```

The `_get_endpoint` method in the `Crud` base class uses the `parent` instance and `parent_id` to construct the correct nested URL path (e.g., `/ledger/1/accountingPeriod/5`).

## Custom Actions

Some endpoints expose actions beyond the standard CRUD operations (e.g., posting a voucher, sending an invoice). These are handled using the `custom_action` method.

### `custom_action(action: str, method: str = "post", resource_id: Optional[str] = None, parent_id: Optional[str] = None, data: Optional[Union[JSONDict, T]] = None, params: Optional[JSONDict] = None) -> Union[T, JSONDict, List[JSONDict]]`

*   **Purpose**: Executes a non-standard action on a resource or collection.
*   **HTTP Method**: Specified by the `method` argument (defaults to "post", but can be "get", "put", etc., depending on the API).
*   **Endpoint**: Constructed based on `_resource_path`, optional `resource_id`, and the `action` string (e.g., `/voucher/123/:post`).
*   **Parameters**:
    *   `action` (str): The name of the custom action, which becomes part of the URL path (e.g., `":post"` for posting a voucher).
    *   `method` (str): The HTTP method required for the action.
    *   `resource_id` (Optional[str]): The ID of the specific resource to perform the action on, if applicable.
    *   `parent_id` (Optional[str]): Used for nested resources.
    *   `data` (Optional[Union[JSONDict, T]]): Payload for methods like POST, PUT, PATCH. Can be a dict or model instance. Validation against `_datamodel` is *not* automatically performed here, as custom actions might use different input/output structures.
    *   `params` (Optional[JSONDict]): Query parameters.
*   **Returns**: The response data, potentially converted to `_datamodel` if the response structure matches a single object, otherwise returned as a dictionary or list. Careful handling of the return type might be needed depending on the specific custom action.

### Example (Conceptual - Posting a Voucher)

```python
# Assuming a voucher endpoint exists: api.voucher
voucher_id = 12345
try:
    # Perform the ':post' action using PUT method (hypothetical)
    # No specific data payload needed for this action in this example
    response = api.voucher.custom_action(action=":post", method="put", resource_id=voucher_id)
    print(f"Voucher {voucher_id} posted successfully. Response: {response}")
except Exception as e:
    print(f"Error posting voucher {voucher_id}: {e}")

# Example with data (Conceptual - Sending an Invoice)
invoice_id = 67890
send_details = {"sendMethod": "EMAIL", "recipientEmail": "customer@example.com"}
try:
    # Perform the ':send' action using POST
    response = api.invoice.custom_action(
        action=":send",
        method="post",
        resource_id=invoice_id,
        data=send_details
    )
    print(f"Invoice {invoice_id} sent. Response: {response}")
except Exception as e:
    print(f"Error sending invoice {invoice_id}: {e}")

```

**Note**: Implementing and using `custom_action` requires careful reading of the specific Tripletex API documentation for that action to understand the required HTTP method, URL structure (how the `action` string is used), expected payload (`data`), query parameters (`params`), and response format. The library provides the mechanism, but the specifics depend on the API itself.