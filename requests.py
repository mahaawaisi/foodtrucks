import requests
import sys

response = requests.get('http://localhost:5000/data')
print(response.json())  # Assuming the response contains JSON data
