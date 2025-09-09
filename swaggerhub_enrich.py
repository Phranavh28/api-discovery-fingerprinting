import json
import csv

# File paths
input_file = 'C:\\Users\\LEGION\\Desktop\\Securin\\output.txt'
output_file = 'C:\\Users\\LEGION\\Desktop\\Securin\\output.csv'

def parse_json_objects(file_content):
    """
    Generator to parse multiple JSON objects in a file.
    """
    decoder = json.JSONDecoder()
    idx = 0

    while idx < len(file_content):
        try:
            obj, idx_new = decoder.raw_decode(file_content, idx)
            yield obj
            idx = file_content.find('{', idx_new)
            if idx == -1:  # No more JSON object found
                break
        except json.JSONDecodeError as e:
            print(f"JSON decode error at index {idx}: {e}")
            break

# Read the text file content
with open(input_file, 'r') as file:
    file_content = file.read()

# Open the CSV file for writing
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)

    # Write the header
    headers = ['Name', 'Description', 'URL', 'Version', 'Created', 'Modified', 'Published', 'Versions', 'Private', 'OASVersion', 'Specification', 'Notifications', 'Standardization', 'CreatedBy']
    csvwriter.writerow(headers)

    # Parse each JSON object and write the data
    for data in parse_json_objects(file_content):
        for api in data.get('apis', []):
            name = api.get('name', '')
            description = api.get('description', '')
            url = next((prop['url'] for prop in api['properties'] if prop['type'] == 'Swagger'), '')
            version = next((prop['value'] for prop in api['properties'] if prop['type'] == 'X-Version'), '')
            created = next((prop['value'] for prop in api['properties'] if prop['type'] == 'X-Created'), '')
            modified = next((prop['value'] for prop in api['properties'] if prop['type'] == 'X-Modified'), '')
            published = next((prop['value'] for prop in api['properties'] if prop['type'] == 'X-Published'), '')
            versions = next((prop['value'] for prop in api['properties'] if prop['type'] == 'X-Versions'), '')
            private = next((prop['value'] for prop in api['properties'] if prop['type'] == 'X-Private'), '')
            oasversion = next((prop['value'] for prop in api['properties'] if prop['type'] == 'X-OASVersion'), '')
            specification = next((prop['value'] for prop in api['properties'] if prop['type'] == 'X-Specification'), '')
            notifications = next((prop['value'] for prop in api['properties'] if prop['type'] == 'X-Notifications'), '')
            standardization = next((prop['value'] for prop in api['properties'] if prop['type'] == 'X-Standardization'), '')
            createdby = next((prop['value'] for prop in api['properties'] if prop['type'] == 'X-CreatedBy'), '')

            csvwriter.writerow([name, description, url, version, created, modified, published, versions, private, oasversion, specification, notifications, standardization, createdby])
