Real-World Examples
==================

This page provides complete, real-world examples of using ``apiconfig`` with various APIs. These examples are based on the integration tests in the project.

JSONPlaceholder API
------------------

`JSONPlaceholder <https://jsonplaceholder.typicode.com/>`_ is a free online REST API for testing and prototyping. Here's how to use ``apiconfig`` with it:

.. code-block:: python

   import httpx
   from apiconfig import ClientConfig

   # Create a basic configuration (no auth needed for JSONPlaceholder)
   config = ClientConfig(
       hostname="jsonplaceholder.typicode.com",
       # No version needed for this API
       timeout=10,
   )

   # Make a request to get a list of posts
   with httpx.Client(timeout=config.timeout) as client:
       response = client.get(f"{config.base_url}/posts")
       posts = response.json()

       # Print the first post
       if posts:
           print(f"Post #{posts[0]['id']}: {posts[0]['title']}")

   # Make a request to create a new post
   new_post = {
       "title": "Testing apiconfig",
       "body": "This is a test post created using apiconfig",
       "userId": 1
   }

   with httpx.Client(timeout=config.timeout) as client:
       response = client.post(
           f"{config.base_url}/posts",
           json=new_post,
       )
       created_post = response.json()
       print(f"Created post with ID: {created_post['id']}")

Fiken API (OAuth2)
----------------

`Fiken <https://fiken.no/>`_ is a Norwegian accounting system with an OAuth2 API. Here's how to use ``apiconfig`` with it:

.. code-block:: python

   import os
   import httpx
   from apiconfig import ClientConfig, BearerAuth, EnvProvider

   # Load configuration from environment variables
   env = EnvProvider()
   config_dict = env.load()

   # Get access token from environment or use a default
   access_token = config_dict.get("FIKEN_ACCESS_TOKEN") or os.environ.get("FIKEN_ACCESS_TOKEN")
   base_url = config_dict.get("FIKEN_BASE_URL") or os.environ.get("FIKEN_BASE_URL") or "https://api.fiken.no/api/v2"

   # Set up authentication strategy if token is available
   auth_strategy = BearerAuth(access_token) if access_token else None

   # Create the API client configuration
   client_config = ClientConfig(
       hostname=base_url,
       auth_strategy=auth_strategy,
   )

   # Prepare request headers using the auth strategy
   headers = {}
   if client_config.auth_strategy is not None:
       headers.update(client_config.auth_strategy.prepare_request_headers())

   # Make a request to get a list of companies
   with httpx.Client(timeout=10) as client:
       response = client.get(f"{client_config.base_url}/companies", headers=headers)

       if response.status_code == 200:
           companies = response.json()
           print(f"Found {len(companies)} companies")

           # Print company names
           for company in companies:
               print(f"Company: {company['name']}")
       else:
           print(f"Error: {response.status_code} - {response.text}")

Tripletex API (API Key + Token)
-----------------------------

`Tripletex <https://tripletex.no/>`_ is a Norwegian accounting system with an API that uses a combination of API tokens and session tokens. Here's how to use ``apiconfig`` with it:

.. code-block:: python

   import os
   import httpx
   from apiconfig import ClientConfig, CustomAuth, EnvProvider

   # Load configuration from environment variables
   env = EnvProvider()
   config_dict = env.load()

   # Get credentials from environment
   consumer_token = config_dict.get("TRIPLETEX_CONSUMER_TOKEN") or os.environ.get("TRIPLETEX_CONSUMER_TOKEN")
   employee_token = config_dict.get("TRIPLETEX_EMPLOYEE_TOKEN") or os.environ.get("TRIPLETEX_EMPLOYEE_TOKEN")
   base_url = config_dict.get("TRIPLETEX_BASE_URL") or os.environ.get("TRIPLETEX_BASE_URL") or "https://tripletex.no/v2"

   # Create a session token first
   def create_session_token():
       url = f"{base_url}/token/session/:create"
       params = {
           "consumerToken": consumer_token,
           "employeeToken": employee_token,
           "expirationDate": "2025-04-23",  # Tomorrow
       }

       response = httpx.put(url, params=params)
       if response.status_code == 200:
           data = response.json()
           return data["value"]["token"]
       else:
           raise Exception(f"Failed to create session token: {response.text}")

   # Get a session token
   session_token = create_session_token()

   # Create a custom auth strategy for Tripletex
   def tripletex_auth():
       return {
           "Authorization": f"Basic {consumer_token}:{session_token}"
       }

   auth_strategy = CustomAuth(auth_callable=tripletex_auth)

   # Create the API client configuration
   client_config = ClientConfig(
       hostname=base_url,
       auth_strategy=auth_strategy,
   )

   # Prepare request headers using the auth strategy
   headers = {}
   if client_config.auth_strategy is not None:
       headers.update(client_config.auth_strategy.prepare_request_headers())

   # Make a request to get company information
   with httpx.Client(timeout=10) as client:
       response = client.get(f"{client_config.base_url}/company", headers=headers)

       if response.status_code == 200:
           company = response.json()
           print(f"Company: {company['value']['name']}")
       else:
           print(f"Error: {response.status_code} - {response.text}")

OneFlow API (API Key)
-------------------

`OneFlow <https://oneflow.com/>`_ is a contract management platform with an API that uses API keys. Here's how to use ``apiconfig`` with it:

.. code-block:: python

   import os
   import httpx
   from apiconfig import ClientConfig, ApiKeyAuth, EnvProvider

   # Load configuration from environment variables
   env = EnvProvider()
   config_dict = env.load()

   # Get API key from environment
   api_key = config_dict.get("ONEFLOW_API_KEY") or os.environ.get("ONEFLOW_API_KEY")
   base_url = config_dict.get("ONEFLOW_BASE_URL") or os.environ.get("ONEFLOW_BASE_URL") or "https://api.oneflow.com/v1"

   # Set up authentication strategy
   auth_strategy = ApiKeyAuth(api_key=api_key, header_name="X-API-KEY")

   # Create the API client configuration
   client_config = ClientConfig(
       hostname=base_url,
       auth_strategy=auth_strategy,
   )

   # Prepare request headers using the auth strategy
   headers = {}
   if client_config.auth_strategy is not None:
       headers.update(client_config.auth_strategy.prepare_request_headers())

   # Make a request to get a list of contracts
   with httpx.Client(timeout=10) as client:
       response = client.get(f"{client_config.base_url}/contracts", headers=headers)

       if response.status_code == 200:
           contracts = response.json()
           print(f"Found {len(contracts['data'])} contracts")

           # Print contract names
           for contract in contracts['data']:
               print(f"Contract: {contract['name']}")
       else:
           print(f"Error: {response.status_code} - {response.text}")

Creating a Reusable API Client
----------------------------

Here's an example of creating a reusable API client class using ``apiconfig``:

.. code-block:: python

   import httpx
   from typing import Dict, Any, Optional, List
   from apiconfig import ClientConfig, BearerAuth

   class MyApiClient:
       """A reusable API client for MyAPI."""

       def __init__(
           self,
           hostname: str = "api.example.com",
           version: str = "v1",
           token: Optional[str] = None,
          timeout: int = 30,
          retries: int = 2,
       ):
           """Initialize the API client.

           Args:
               hostname: The API hostname
               version: The API version
               token: Optional bearer token for authentication
               timeout: Request timeout in seconds
               retries: Number of retries for failed requests
           """
           # Set up authentication if token is provided
           auth_strategy = BearerAuth(token) if token else None

           # Create the configuration
           self.config = ClientConfig(
               hostname=hostname,
               version=version,
               auth_strategy=auth_strategy,
               timeout=timeout,
               retries=retries,
           )

           # Create a persistent HTTP client
           self.client = httpx.Client(timeout=self.config.timeout)

       def __del__(self):
           """Close the HTTP client when the API client is destroyed."""
           if hasattr(self, 'client'):
               self.client.close()

       def _get_headers(self) -> Dict[str, str]:
           """Get request headers including authentication."""
           headers = {}
           if self.config.auth_strategy:
               headers.update(self.config.auth_strategy.prepare_request_headers())
           return headers

       def get_users(self) -> List[Dict[str, Any]]:
           """Get a list of users."""
           response = self.client.get(
               f"{self.config.base_url}/users",
               headers=self._get_headers(),
           )
           response.raise_for_status()
           return response.json()

       def get_user(self, user_id: str) -> Dict[str, Any]:
           """Get a specific user by ID."""
           response = self.client.get(
               f"{self.config.base_url}/users/{user_id}",
               headers=self._get_headers(),
           )
           response.raise_for_status()
           return response.json()

       def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
           """Create a new user."""
           response = self.client.post(
               f"{self.config.base_url}/users",
               headers=self._get_headers(),
               json=user_data,
           )
           response.raise_for_status()
           return response.json()

   # Usage example
   if __name__ == "__main__":
       # Create the API client
       client = MyApiClient(
           hostname="api.example.com",
           version="v1",
           token="my-auth-token",
       )

       # Get all users
       users = client.get_users()
       print(f"Found {len(users)} users")

       # Get a specific user
       user = client.get_user("user123")
       print(f"User: {user['name']}")

       # Create a new user
       new_user = client.create_user({
           "name": "John Doe",
           "email": "john@example.com",
       })
       print(f"Created user with ID: {new_user['id']}")
