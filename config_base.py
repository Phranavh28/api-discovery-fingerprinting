import os
import json
import requests as r

# Directory containing the JSON files
directory = "C:\\Users\\LEGION\\Desktop\\Securin\\API JSON"

# Get all the JSON files from the specified directory
json_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.json')]

api_database = {}

for json_file in json_files:
    with open(json_file, 'r') as file:
        apis = json.load(file)

    for api in apis:
        api_database[api] = {}
        
        try:
            resp = r.get(api)
            
            api_database[api]["status code"] = str(resp.status_code)
            api_database[api]["content_type"] = resp.headers.get("Content-Type", "")
            api_database[api]["content"] = resp.content.decode("utf-8", errors="ignore")
            api_database[api]["content length"] = str(resp.headers.get("Content-Length", ""))
            
            api_database[api]["Methods"] = []
            if "Allow" in resp.headers:
                api_database[api]["Methods"] = resp.headers["Allow"].split(",")
            elif "Access-Control-Allow-Methods" in resp.headers:
                api_database[api]["Methods"] = resp.headers["Access-Control-Allow-Methods"].split(",")
                
            for method in api_database[api]["Methods"]:
                api_database[api][method] = {
                    "Summary": "",
                    "Description": ""
                }

            api_database[api]["Banners"] = dict(resp.headers)
            
        except Exception as e:
            print(f"Error processing API: {api}. Error: {e}")

# Save the results to api_response.json
with open("api_response.json", "w") as out:
    json.dump(api_database, out, indent=4)

print("Processing complete. Results saved in api_response.json.")
