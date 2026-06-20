
import asyncio
import aiohttp
import ssl
from config import Config

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

async def test_xbit_search(config, query):
    print(f"\n--- Testing Xbit Search for '{query}' ---")
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
            params = {
                "api_key": config.XBIT_API_KEY,
                "q": query
            }
            # Common endpoints: let's try search first
            async with session.get(f"{config.XBIT_API_URL}/search", params=params) as resp:
                print(f"Xbit Search Status: {resp.status}")
                if resp.status == 200:
                    data = await resp.json()
                    print(f"Xbit Search Results: {len(data) if isinstance(data, list) else type(data)}")
                    return data
    except Exception as e:
        print(f"Xbit Search Error: {e}")
    return None

async def test_xbit_download(config, video_id):
    print(f"\n--- Testing Xbit Download for '{video_id}' ---")
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
            params = {
                "api_key": config.XBIT_API_KEY,
                "id": video_id
            }
            async with session.get(f"{config.XBIT_API_URL}/download", params=params) as resp:
                print(f"Xbit Download Status: {resp.status}")
                if resp.status == 200:
                    data = await resp.json()
                    print(f"Xbit Download Response keys: {list(data.keys()) if isinstance(data, dict) else type(data)}")
                    return data
    except Exception as e:
        print(f"Xbit Download Error: {e}")
    return None

async def test_nexgen_search(config, query):
    print(f"\n--- Testing NexGenBots Search for '{query}' ---")
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
            params = {
                "token": config.NEXGENBOTS_API_TOKEN,
                "q": query
            }
            # Try common search endpoints
            for endpoint in ["/search", "/ytsearch"]:
                url = f"{config.NEXGENBOTS_API_URL}{endpoint}"
                print(f"Trying {url}")
                async with session.get(url, params=params) as resp:
                    print(f"NexGen Search Status (endpoint {endpoint}): {resp.status}")
                    if resp.status == 200:
                        data = await resp.json()
                        print(f"NexGen Search Results: {len(data) if isinstance(data, list) else type(data)}")
                        return data
    except Exception as e:
        print(f"NexGen Search Error: {e}")
    return None

async def test_nexgen_download(config, video_id):
    print(f"\n--- Testing NexGenBots Download for '{video_id}' ---")
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
            params = {
                "token": config.NEXGENBOTS_API_TOKEN,
                "id": video_id
            }
            for endpoint in ["/download", "/ytdl"]:
                url = f"{config.NEXGENBOTS_API_URL}{endpoint}"
                print(f"Trying {url}")
                async with session.get(url, params=params) as resp:
                    print(f"NexGen Download Status (endpoint {endpoint}): {resp.status}")
                    if resp.status == 200:
                        data = await resp.json()
                        print(f"NexGen Download Response keys: {list(data.keys()) if isinstance(data, dict) else type(data)}")
                        return data
    except Exception as e:
        print(f"NexGen Download Error: {e}")
    return None

async def test_video_api_search(config, query):
    print(f"\n--- Testing Video API Search for '{query}' ---")
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
            params = {
                "token": config.NEXGENBOTS_API_TOKEN,
                "q": query
            }
            for endpoint in ["/search", "/ytsearch"]:
                url = f"{config.VIDEO_API_URL}{endpoint}"
                print(f"Trying {url}")
                async with session.get(url, params=params) as resp:
                    print(f"Video API Search Status (endpoint {endpoint}): {resp.status}")
                    if resp.status == 200:
                        data = await resp.json()
                        print(f"Video API Search Results: {len(data) if isinstance(data, list) else type(data)}")
                        return data
    except Exception as e:
        print(f"Video API Search Error: {e}")
    return None

async def main():
    config = Config()
    test_query = "love story"
    
    await test_xbit_search(config, test_query)
    await test_nexgen_search(config, test_query)
    await test_video_api_search(config, test_query)
    
    print("\n--- All tests complete ---")

if __name__ == "__main__":
    asyncio.run(main())
