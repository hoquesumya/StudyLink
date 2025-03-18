from fastapi import APIRouter
import json

import aiohttp
import asyncio
import time
import requests
import os
#load_dotenv()
urls = [
    {"rel": "user", "href": "http://54.146.201.242:8000/users/jam2492/profile"},
    {"rel": "course", "href": "http://35.174.4.121:8000/users/jam2492/courses"},
    {"rel": "studygroup", "href": "http://127.0.0.1:8000/StudyGroup/1.0/create_group?uni=jam2492&course_id=255667&group_name=StudyLatina"}
]


async def call_get(url, headers=None):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()  # Check if the request was successful
                result = await response.json()  # Return the JSON response
                return result
        except aiohttp.ClientResponseError as err:
            print(f"HTTP error occurred: {err}")
            return None
        except Exception as err:
            print(f"An error occurred: {err}")
            return None

async def get_all_urls(urls):
    """Encapsulates the API call logic to call the API three times asynchronously."""
    tasks = []
    properties = []
    headers_for_course = {
        "accept": "application/json",
        "token": "1396~yFrVF9nYzKV6YyrAtaZccFcLATt84zMcLJehYX7Y26z7RGuCnuAmGQQmCJtN8H6C"
    }

    for u in range(len(urls) - 1):
        properties.append(urls[u]["rel"])
        # Pass headers only for the "course" URL
        if urls[u]["rel"] == "course":
            tasks.append(call_get(urls[u]["href"], headers=headers_for_course))
        else:
            tasks.append(call_get(urls[u]["href"]))

    all_results = await asyncio.gather(*tasks)  # Run tasks concurrently and gather results
    full_result = {}

    for i in range(len(properties)):
        p = properties[i]
        v = all_results[i]
        full_result[p] = v  # Store each result under the rel key

    return full_result

# Run the async function


def put(urls):
    """Encapsulates the API call logic to call the API three times asynchronously."""
    pass
def post(urls):
   pass


def call_post(url, data=None):
    """Make a POST request to the specified URL with optional data."""
    try:
        # Include data in the body of the POST request
        response = requests.post(url, json=data)  # Sending JSON data
        response.raise_for_status()  # Check if the request was successful
        return response.json()  # Return the JSON response
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return None
    except Exception as err:
        print(f"An error occurred: {err}")
        return None


def call_post_urls(urls):
    """Make POST requests for all URLs provided in the list."""
    result = {}

  
        # Prepare the data payload based on the URL's relationship
    data = {
            "uni": urls[2].get("uni"),  # Add any relevant data fields
            "course_id": urls[2].get("course_id"),
            "group_name": urls[2].get("group_name")
    }
    r = call_post(urls[2]["href"], data=data)  # Call the POST function
    t = r.get(urls[2]["rel"], r) if r else None  # Safely handle the response
    result[urls[2]["rel"]] = t
    print(result)
   
async def main():
    '''
    
    load_dotenv()
    url1 = os.getenv("URLUSER")
    url2 = os.getenv("URLClass")
    url3 = os.getenv("URLStudyGroup")
   
    urls = []
    urls.append(url1)
    urls.append(url2)
    urls.append(url3)
    print(urls)
    '''

    start_time = time.time()

    # Call API three times asynchronously
    result = await get_all_urls(urls)

    # Calculate total execution time
    total_time = time.time() - start_time

    print("Full result = ", json.dumps(result, indent=2))

    # Print total execution time
    print(f"Total execution time: {total_time:.2f} seconds")

    start_time = time.time()
    results = call_post_urls(urls)
    total_time = time.time() - start_time
    #print(results)

if __name__ == "__main__":
    asyncio.run(main())


