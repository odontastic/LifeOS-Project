import httpx
import asyncio
import uuid
import datetime
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

API_BASE_URL = "http://localhost:8001" # Base URL for auth endpoints
RESOURCE_API_URL = f"{API_BASE_URL}/resource" # Base URL for resource endpoints

# Define retry settings for HTTPX ReadError
@retry(stop=stop_after_attempt(5), wait=wait_fixed(2), retry=retry_if_exception_type(httpx.ReadError))
async def make_request_with_retry(method: str, url: str, **kwargs):
    async with httpx.AsyncClient() as client:
        if method == "POST":
            response = await client.post(url, **kwargs)
        elif method == "GET":
            response = await client.get(url, **kwargs)
        # Add other methods if needed
        return response

async def test_resource_event_lifecycle():
    print("--- Starting Resource Event Lifecycle Test ---")
    await asyncio.sleep(30) # Increased delay to 30 seconds
    
    test_username = "test_user"
    test_password = "testpassword123" # In a real scenario, use strong passwords and manage securely

    access_token = None
    
    # Try to register
    print(f"Attempting to register user: {test_username}")
    try:
        register_response = await make_request_with_retry(
            "POST",
            f"{API_BASE_URL}/register",
            json={"username": test_username, "password": test_password}
        )
        print(f"Register response status: {register_response.status_code}")
        if register_response.status_code == 400 and "already registered" in register_response.text:
            print(f"User {test_username} already registered, proceeding to login.")
        else:
            register_response.raise_for_status() # This will raise HTTPStatusError for other 4xx/5xx
            print(f"User {test_username} registered successfully.")

        # Log in
        print(f"Attempting to log in user: {test_username}")
        token_response = await make_request_with_retry(
            "POST",
            f"{API_BASE_URL}/token",
            data={"username": test_username, "password": test_password}
        )
        print(f"Login response status: {token_response.status_code}")
        token_response.raise_for_status() # This will raise HTTPStatusError for 4xx/5xx
        token_data = token_response.json()
        access_token = token_data["access_token"]
        print("Successfully obtained access token.")
    except httpx.HTTPStatusError as e:
        print(f"Authentication setup failed: {e.response.status_code} - {e.response.text}")
        return
    except Exception as e:
        print(f"An unexpected error occurred during authentication setup: {e}")
        print(f"Exception details: {e}") # Added more details
        return

    if not access_token:
        print("Failed to obtain access token, cannot proceed with resource tests.")
        return

    headers = {"Authorization": f"Bearer {access_token}"}

    # 1. Create a new Resource
    resource_id = str(uuid.uuid4())
    resource_data = {
        "id": resource_id,
        "username": test_username, # Ensure username matches the authenticated user
        "type": "resource",
        "title": "Test Resource",
        "format": "link",
        "body": "This is a test resource body.",
        "tags": ["test", "resource", "phase3"],
        "related_zettels": [],
        "horizon": "resources"
    }

    print(f"Attempting to create Resource with ID: {resource_id}")
    try:
        async with httpx.AsyncClient(headers=headers) as client:
            response = await client.post(f"{RESOURCE_API_URL}/", json=resource_data, follow_redirects=False)
            print(f"POST response status: {response.status_code}")
            if response.status_code == 307:
                print(f"Redirected to: {response.headers.get('location')}")
                # Manually follow redirect for debugging purposes if needed
                response = await client.post(response.headers['location'], json=resource_data, headers=headers)

            response.raise_for_status()
            created_resource = response.json()
            print(f"Resource created successfully: {created_resource}")
            assert created_resource["id"] == resource_id
            assert created_resource["username"] == test_username # Added username assertion
            assert created_resource["title"] == "Test Resource"
            assert created_resource["format"] == "link" # Corrected format assertion
            assert created_resource["body"] == "This is a test resource body."
            assert created_resource["tags"] == ["test", "resource", "phase3"]
            assert created_resource["horizon"] == "resources"
    except httpx.HTTPStatusError as e:
        print(f"Error creating resource: {e.response.status_code} - {e.response.text}")
        return
    except Exception as e:
        print(f"An unexpected error occurred during resource creation: {e}")
        print(f"Exception details: {e}") # Added more details
        return

    # Debug: List all resources
    print("Attempting to list all resources via debug_all endpoint...")
    try:
        async with httpx.AsyncClient(headers=headers) as client:
            debug_all_response = await client.get(f"{RESOURCE_API_URL}/debug_all", follow_redirects=False)
            debug_all_response.raise_for_status()
            all_resources = debug_all_response.json()
            print(f"All resources from debug_all: {all_resources}")
            found_in_all = any(r["id"] == resource_id for r in all_resources)
            print(f"Resource with ID {resource_id} found in debug_all: {found_in_all}")
            assert found_in_all # Assert that our created resource is in the list
    except httpx.HTTPStatusError as e:
        print(f"Error listing all resources: {e.response.status_code} - {e.response.text}")
        return
    except Exception as e:
        print(f"An unexpected error occurred during listing all resources: {e}")
        print(f"Exception details: {e}")
        return

    # 2. Retrieve the created Resource
    print(f"Attempting to retrieve Resource with ID: {resource_id}")
    try:
        async with httpx.AsyncClient(headers=headers) as client:
            response = await client.get(f"{RESOURCE_API_URL}/{resource_id}", follow_redirects=False)
            print(f"GET response status: {response.status_code}")
            if response.status_code == 307:
                print(f"Redirected to: {response.headers.get('location')}")
                # Manually follow redirect for debugging purposes if needed
                response = await client.get(response.headers['location'], headers=headers)

            response.raise_for_status()
            retrieved_resource = response.json()
            print(f"Resource retrieved successfully: {retrieved_resource}")
            assert retrieved_resource["id"] == resource_id
            assert retrieved_resource["username"] == test_username # Added username assertion
            assert retrieved_resource["title"] == "Test Resource"
            assert retrieved_resource["format"] == "link" # Corrected format assertion
            assert retrieved_resource["body"] == "This is a test resource body."
            assert retrieved_resource["tags"] == ["test", "resource", "phase3"]
            assert retrieved_resource["horizon"] == "resources"
            print("Resource retrieval and verification successful.")
    except httpx.HTTPStatusError as e:
        print(f"Error retrieving resource: {e.response.status_code} - {e.response.text}")
        return
    except Exception as e:
        print(f"An unexpected error occurred during resource retrieval: {e}")
        print(f"Exception details: {e}") # Added more details
        return

    print("--- Resource Event Lifecycle Test Completed Successfully ---")

if __name__ == "__main__":
    asyncio.run(test_resource_event_lifecycle())