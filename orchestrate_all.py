#1. This code automates and checks for all the api DOCS in the Postman API website .
# Import necessary modules from the selenium package
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define the URL template for the website we're scraping, where {page_num} will be replaced with the actual page number during the loop
URL_TEMPLATE = "https://www.postman.com/explore/collections?sort=forkCount&page={page_num}&filter="

# Setting up the browser options.
options = webdriver.ChromeOptions()
options.headless = False  # Setting the browser to non-headless mode. If set to True, the browser will run in the background.

# Define the web driver, in this case, Chrome.
driver = webdriver.Chrome(options=options)

# Define a wait object to utilize explicit waits, which will wait for a maximum of 10 seconds for conditions to be met.
wait = WebDriverWait(driver, 10)

# Loop through the pages specified in the range.
for page_num in range(1, 34964):  # Loop through page numbers from 1 to 34963.
    driver.get(URL_TEMPLATE.format(page_num=page_num))  # Navigate to the page.
    
    # Wait for the API workspaces to load, then get all their links.
    api_workspace_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.entity-heading')))
    api_workspace_links = [elem.get_attribute('href') for elem in api_workspace_elements]

    # Loop through each workspace link collected.
    for link in api_workspace_links:
        driver.get(link)  # Navigate to the workspace link.
        
        try:
            # Wait for the documentation element to load and then get its link.
            documentation_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".documentation-overview-footer")))
            documentation_link = documentation_element.get_attribute('href')
            print(f"API Documentation Link: {documentation_link}")  # Print the documentation link.
        except:
            # If there's an error (e.g., documentation link missing), print an error message and continue to the next link.
            print(f"Skipping {link} due to error or missing documentation link.")
            continue

# Once all pages have been processed, close the browser.
driver.quit()


#2. The collection IDs were extracted using a Selenium script, with each ID representing a unique API collection in Postman.

# Import necessary modules from the selenium package.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define the URL template for the website we're scraping.
URL_TEMPLATE = "https://www.postman.com/explore/collections?sort=forkCount&page={page_num}&filter="

# Setting up the browser options.
options = webdriver.ChromeOptions()
options.headless = False  # If set to True, the browser will run in the background.

# Initialize the Chrome web driver with the given options.
driver = webdriver.Chrome(options=options)

# Define a wait object to utilize explicit waits, which will wait for a maximum of 10 seconds for conditions to be met.
wait = WebDriverWait(driver, 10)

# Open a file for writing to save the collection IDs.
with open('collection3_ids.txt', 'w') as file:

    # Loop through the specified range of pages.
    for page_num in range(1, 34000): 
        driver.get(URL_TEMPLATE.format(page_num=page_num))
        
        try:
            # Wait for the API workspaces to load and then capture their links.
            api_workspace_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.entity-heading')))
            api_workspace_links = [elem.get_attribute('href') for elem in api_workspace_elements]

            # Loop through each workspace link.
            for link in api_workspace_links:
                if link:
                    # Modify the link to get detailed info about the collection.
                    info_link = link + "?ctx=info"
                    driver.get(info_link)
                    
                    try:
                        # Extract the collection ID from the URL and save it to the file.
                        collection_id = driver.current_url.split("/collection/")[1].split("?")[0]
                        file.write(collection_id + '\n')
                    except IndexError:
                        # If unable to extract the collection ID, print an error and continue.
                        print(f"Collection ID not found for link: {link}. Skipping...")
                else:
                    # If the link is empty, print an error and continue.
                    print(f"Found an empty link on page {page_num}. Skipping...")
        except Exception as e:
            # If there's any error while processing a page, print an error message and continue.
            print(f"Error processing page {page_num}. Error message: {e}")

# Once all pages have been processed, close the browser.
driver.quit()

# Print a completion message.
print("Task completed successfully!")

#3.This script reads collection IDs from a file, uses the Postman API to get the data for each collection, and then saves the data as a JSON file in the specified directory.

import requests
import json
import os

# Read collection IDs from the text file into a list.
with open("collection_ids.txt", "r") as file:
    collection_ids = [line.strip() for line in file.readlines()]

# Define the directory where the exported JSON files will be saved.
output_dir = "C:\\Users\\LEGION\\Desktop\\Securin\\API JSON"
# Check if the directory exists, if not, create it.
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Define a function to export a collection using its ID.
def export_collection(api_key, collection_id):
    # Define the URL for the Postman API endpoint.
    url = f'https://api.getpostman.com/collections/{collection_id}'

    # Set up the headers, including the API key.
    headers = {
        'X-Api-Key': api_key,
    }

    # Make the GET request to fetch the collection data.
    response = requests.get(url, headers=headers)

    # Check if the request was successful.
    if response.status_code == 200:
        # Construct the path where the JSON file will be saved.
        file_path = os.path.join(output_dir, f"{collection_id}.json")
        # Write the response data to the JSON file.
        with open(file_path, 'w') as file:
            json.dump(response.json(), file, indent=4)
        return True, f"Collection {collection_id} exported successfully."
    else:
        # If the request was not successful, return a failure message.
        return False, f"Failed to export the collection {collection_id}. Check your API key."

# Insert your Postman API Key here.
api_key = ''

success_count = 0
failure_messages = []

# Check if 'collection_ids' variable exists, is a list, and is not empty.
if 'collection_ids' in locals() and isinstance(collection_ids, list) and collection_ids:
    # Loop through each collection ID.
    for current_id in collection_ids:
        try:
            # Try to export the collection using its ID.
            success, message = export_collection(api_key, current_id)
            if success:
                success_count += 1
            else:
                # If the export was not successful, save the failure message.
                failure_messages.append(message)
        except Exception as e:
            # If there was an exception, save the error message.
            failure_messages.append(f"Error for collection ID {current_id}: {str(e)}")
else:
    # If the 'collection_ids' variable is not defined, not a list, or empty, save the failure message.
    failure_messages.append("No collection IDs found or they couldn't be read.")

# Print the number of successfully exported collections.
print(f"Successfully exported {success_count} collections.")
# Print each failure message.
for msg in failure_messages:
    print(msg)


# 4.This script processes JSON files from a specified directory, extracts API endpoints from them, and saves the unique endpoints to a text file.

import json
import os

def extract_api_endpoints(json_data):
    """Extract API endpoints from the provided JSON data."""
    endpoints = set()  # Use a set to ensure unique endpoints.
    # Iterate over items in the collection.
    for item in json_data.get("collection", {}).get("item", []):
        request = item.get("request", {})
        # Extract the raw URL of the endpoint.
        url = request.get("url", {}).get("raw", "")
        if url:
            endpoints.add(url)
    return endpoints

def main():
    """Main function to process all JSON files and extract API endpoints."""
    directory_path = "C:\\Users\\LEGION\\Desktop\\Securin\\API JSON"
    # Define the path for the output text file.
    output_file_path = os.path.join(directory_path, "extracted_endpoints.txt")
    
    all_endpoints = set()
    
    # Loop over all files in the specified directory.
    for filename in os.listdir(directory_path):
        # Check if the file has a .json extension.
        if filename.endswith(".json"):
            with open(os.path.join(directory_path, filename), "r", encoding="utf-8") as f:
                try:
                    # Load JSON data from the file.
                    data = json.load(f)
                    # Extract endpoints from the JSON data.
                    endpoints = extract_api_endpoints(data)
                    # Update the set with the extracted endpoints.
                    all_endpoints.update(endpoints)
                except json.JSONDecodeError:
                    # If there's an error decoding the JSON, print an error message and continue.
                    print(f"Error parsing {filename}. Skipping...")
    
    # Write all extracted endpoints to the output text file.
    with open(output_file_path, "w", encoding="utf-8") as out_file:
        for endpoint in sorted(all_endpoints):
            out_file.write(endpoint + "\n")
    
    # Print a completion message.
    print(f"Extracted endpoints saved to {output_file_path}")

# Run the main function if the script is executed as the main module.
if __name__ == "__main__":
    main()
    
# 5. This script fetches data from Postman's API for a range of pages and saves the responses to a file. It handles rate-limiting by checking for a 429 status code and waiting the specified amount of time before retrying.

import requests
import json
import time  # Imported for adding delays

# Initialize the base details for the API request.
base_url = "https://www.postman.com/_api/ws/proxy"
headers = {
    "Host": "www.postman.com",
    "Cookie": "cookie_value",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
    # ... (other headers)
}
limit = 12
DEFAULT_DELAY = 60  # Default delay between requests in seconds. Adjust if necessary.

# Define the range of pages you want to scrape.
start_page = 1
end_page = 30000

# Open a file to save the output data.
with open("output_responses3.txt", "w") as file:
    # Loop through each page in the specified range.
    for page in range(start_page - 1, end_page):  # Subtract 1 from start_page for zero-based indexing.
        offset = page * limit
        path = f"/v1/api/networkentity?limit={limit}&type=public&referrer=explore&entityType=collection&flattenAPIVersions=true&category=&sort=latest&offset={offset}"
        body = {"service": "publishing", "method": "get", "path": path}
        
        # Make the API request.
        response = requests.post(base_url, headers=headers, json=body)
        
        # Handle rate limiting (status code 429).
        if response.status_code == 429:
            # If rate-limited, check how long to wait before retrying.
            retry_after = int(response.headers.get('Retry-After', DEFAULT_DELAY))
            print(f"Rate limit exceeded. Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
            # Make the request again after waiting.
            response = requests.post(base_url, headers=headers, json=body)
            
        # Check if the request was successful.
        if response.status_code == 200:
            # Save the JSON response to the output file.
            file.write(json.dumps(response.json(), indent=4))
            file.write("\n")
        else:
            # If not successful, print an error message.
            print(f"Failed to retrieve data for page {page + 1} with status code {response.status_code}")
        
        # Introduce a delay between requests to be respectful to the server and avoid rate limits.
        time.sleep(1)  # Adjust the delay as needed.

# 6. The script reads from a text file containing multiple JSON objects, extracts relevant information from these objects, and then writes the extracted data to a CSV file.

import json
import csv

# Paths for the input text file and the output CSV file.
input_file_path = r'C:\Users\LEGION\Desktop\Securin\output_responses1.txt'
output_csv_file = 'Exceldata4.csv'

# This list will store the extracted data from the input file.
extracted_data = []

def process_data(data):
    """Process the data dictionary and extract the required fields."""
    
    # Check if the "data" key exists in the provided data.
    if "data" in data:
        # Iterate through each item in the "data" list.
        for item in data["data"]:
            
            # Extract individual fields from the item.
            id_ = item.get('id', '')
            entity_id = item.get('entityId', '')
            entity_type = item.get('entityType', '')
            name = item.get('name', '')
            summary = item.get('summary', '')
            description = item.get('description', '')
            type_ = item.get('type', '')
            
            # Extract specific metrics from the "metrics" list inside the item.
            view_count = next((metric['metricValue'] for metric in item.get('metrics', []) if metric['metricName'] == 'viewCount'), 0)
            fork_count = next((metric['metricValue'] for metric in item.get('metrics', []) if metric['metricName'] == 'forkCount'), 0)
            watch_count = next((metric['metricValue'] for metric in item.get('metrics', []) if metric['metricName'] == 'watchCount'), 0)
            
            # Continue extracting other fields.
            publisher_type = item.get('publisherType', '')
            publisher_id = item.get('publisherId', '')
            created_at = item.get('createdAt', '')
            updated_at = item.get('updatedAt', '')
            
            # Extract and process categories and tags (which can be strings or dictionaries).
            categories = ', '.join([str(cat) if isinstance(cat, (str, int)) else ' '.join(map(str, cat.values())) for cat in item.get('categories', [])])
            tags = ', '.join([str(tag) if isinstance(tag, (str, int)) else ' '.join(map(str, tag.values())) for tag in item.get('tags', [])])
            
            redirect_url = item.get('redirectURL', '')
            
            # Add the extracted fields to the extracted_data list.
            extracted_data.append([id_, entity_id, entity_type, name, summary, description, type_, view_count, fork_count, watch_count, publisher_type, publisher_id, created_at, updated_at, categories, tags, redirect_url])

def main():
    """Main function to process the input text file and create an output CSV."""
    
    # This variable will hold chunks of JSON data as we read from the input file.
    json_string = ''
    
    # Open the input file and read it line by line.
    with open(input_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            
            # Continuously append lines to form a complete JSON string.
            json_string += line.strip()
            
            # If the current string forms a complete JSON object, process it.
            if json_string.endswith('}'):
                try:
                    # Convert the string to a Python dictionary.
                    data = json.loads(json_string)
                    
                    # Process this dictionary to extract required data.
                    process_data(data)
                    
                    # Reset the json_string for the next JSON object in the input file.
                    json_string = ''
                except json.JSONDecodeError:
                    # If there's an error in decoding, continue to the next line to complete the JSON object.
                    continue
    
    # Now, write the extracted data to the output CSV file.
    with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # Define the header for the CSV.
        header = ['ID', 'EntityID', 'EntityType', 'Name', 'Summary', 'Description', 'Type', 'ViewCount', 'ForkCount', 'WatchCount', 'PublisherType', 'PublisherId', 'CreatedAt', 'UpdatedAt', 'Categories', 'Tags', 'RedirectURL']
        
        # Write the header to the CSV.
        csvwriter.writerow(header)
        
        # Write each row of extracted data to the CSV.
        csvwriter.writerows(extracted_data)

# Execute the main function when this script is run.
if __name__ == "__main__":
    main()

