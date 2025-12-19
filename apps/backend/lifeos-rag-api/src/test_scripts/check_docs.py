import httpx
import asyncio

async def check_docs_endpoint():
    API_BASE_URL = "http://localhost:8001"
API_DOCS_URL = f"{API_BASE_URL}/docs"
    print(f"Attempting to fetch {API_DOCS_URL}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(API_DOCS_URL)
            response.raise_for_status()
            print(f"Successfully fetched /docs endpoint. Status Code: {response.status_code}")
            # print(response.text[:500]) # Print first 500 characters of the HTML
    except httpx.HTTPStatusError as e:
        print(f"Error fetching /docs endpoint: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(check_docs_endpoint())