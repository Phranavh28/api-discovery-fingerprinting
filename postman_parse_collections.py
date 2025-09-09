import requests
import json
import time  # Imported for adding delays

# Initialize the base details for the API request
base_url = "https://www.postman.com/_api/ws/proxy"
headers = {
    "Host": "www.postman.com",
    "Cookie": "cookie_value",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json",
    "X-Entity-Team-Id": "0",
    "Origin": "https://www.postman.com",
    "Connection": "close"
}
limit = 12
DEFAULT_DELAY = 60  # Default delay between requests in seconds, adjust as needed

# Change the start and end pages
start_page = 1
end_page = 2

# Open a file to write the output
with open("output_responses3.txt", "w") as file:
    # Iterate over the desired pages
    for page in range(start_page - 1, end_page):  # Subtracting 1 from start_page to ensure it starts at 30001
        offset = page * limit
        path = f"/v1/api/networkentity?limit={limit}&type=public&referrer=explore&entityType=collection&flattenAPIVersions=true&category=&sort=latest&offset={offset}"
        body = {"service": "publishing", "method": "get", "path": path}
        
        # Send the HTTP POST request
        response = requests.post(base_url, headers=headers, json=body)
        
        # Handling 429 status code
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', DEFAULT_DELAY))
            print(f"Rate limit exceeded. Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
            # Reattempting the same request after waiting
            response = requests.post(base_url, headers=headers, json=body)
            
        if response.status_code == 200:
            # Write the JSON response to the file
            file.write(json.dumps(response.json(), indent=4))
            file.write("\n")
        else:
            print(f"Failed to retrieve data for page {page + 1} with status code {response.status_code}")
        
        # Adding a delay between all requests to avoid hitting the rate limit
        time.sleep(1)  # Adjust the delay as needed
