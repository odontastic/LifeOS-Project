import httpx
import asyncio

async def check_root_endpoint():
    API_BASE_URL = "http://localhost:8001"
API_ROOT_URL = f"{API_BASE_URL}/"
    print(f"Attempting to fetch {API_ROOT_URL}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(API_ROOT_URL)
            response.raise_for_status()
            print(f"Successfully fetched / endpoint. Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
    except httpx.HTTPStatusError as e:
        print(f"Error fetching / endpoint: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(check_root_endpoint())