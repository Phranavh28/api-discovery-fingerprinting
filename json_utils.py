import requests
import json
import os

# Read collection IDs from the text file
with open("collection_ids.txt", "r") as file:
    collection_ids = [line.strip() for line in file.readlines()]

# Define the directory to save the exported JSON files
output_dir = "C:\\Users\\LEGION\\Desktop\\Securin\\API JSON"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to export collection based on the given ID
def export_collection(api_key, collection_id):
    # Postman API URL
    url = f'https://api.getpostman.com/collections/{collection_id}'

    # Set up headers with API key
    headers = {
        'X-Api-Key': api_key,
    }

    # Make the GET request to fetch the collection
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Define the path to save the collection as a JSON file
        file_path = os.path.join(output_dir, f"{collection_id}.json")
        with open(file_path, 'w') as file:
            json.dump(response.json(), file, indent=4)
        return True, f"Collection {collection_id} exported successfully."
    else:
        return False, f"Failed to export the collection {collection_id}. Check your API key."

# Your Postman API Key (Note: Make sure to add your API key here)
api_key = 'PMAK-64fecd10f56b5e002a3393c8-763a4db95d2dfb2442bd106fc321d8a5c4'

success_count = 0
failure_messages = []

success_count = 0
failure_messages = []

# Check if collection_ids is defined and not empty
if 'collection_ids' in locals() and isinstance(collection_ids, list) and collection_ids:
    for current_id in collection_ids:
        try:
            success, message = export_collection(api_key, current_id)
            if success:
                success_count += 1
            else:
                failure_messages.append(message)
        except Exception as e:
            failure_messages.append(f"Error for collection ID {current_id}: {str(e)}")
else:
    failure_messages.append("No collection IDs found or they couldn't be read.")

print(f"Successfully exported {success_count} collections.")
for msg in failure_messages:
    print(msg)
