import requests
import json
import pandas as pd
import os

# Define custom headers
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}

# Replace this URL with the URL of your JSON file
url = "https://smaato.com/sellers.json"

try:
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    # Assuming the response contains JSON data
    json_data = response.json()

    """
json_file_path = '/Users/oliver/Desktop/rubiconproject.json'

try:
    # Open and read the JSON file
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)"""

    # Initialize empty lists to store the data
    seller_ids = []
    domains = []

    # Filter the sellers list to include only PUBLISHERs and extract data into the lists
    if "sellers" in json_data:
        for seller in json_data['sellers']:
            if seller.get('seller_type') == 'PUBLISHER':
                seller_id = seller.get('seller_id')
                domain = seller.get('domain')
                seller_ids.append(seller_id)
                domains.append(domain)
        for domain, id in zip(domains, seller_ids):
            try:
                url1 = "http://" + domain + "/ads.txt"
                url2 = "http://" + domain + "/app-ads.txt"
                url3 = "http://" + domain
                response1 = requests.get(url1, headers=HEADERS, timeout=20)
                response2 = requests.get(url2, headers=HEADERS, timeout=20)
                response3 = requests.get(url3, headers=HEADERS, timeout=20)
                check1 = str(id) in response1.text
                check2 = str(id) in response2.text
                check3 = "manga" in response3.text
                print(id, "#", domain, "#", check1, "#", response1.status_code, "#", check2, "#", response2.status_code, "#", check3)
                # Append data to CSV file
                with open('sellers_data.csv', mode='a') as file:
                    file.write(f"{id}#{domain}#{check1}#{response1.status_code}#{check2}#{response2.status_code}#{check3}\n")
            except Exception as e:
                print(id, "#", domain, "#", e)
except requests.exceptions.RequestException as e:
    print(f"Error fetching the JSON from the URL: {e}")
except ValueError as e:
    print(f"Error parsing the JSON data: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
