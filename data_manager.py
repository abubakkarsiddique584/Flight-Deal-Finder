import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SHEETY_USERNAME = os.getenv("SHEETY_USERNAME")
SHEETY_PASSWORD = os.getenv("SHEETY_PASSWORD")
SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/ff9b6de90f095761e72ab421e4ee6079/flight/prices"

class DataManager:
    def __init__(self):
        self._authorization = HTTPBasicAuth(SHEETY_USERNAME, SHEETY_PASSWORD)
        self.destination_data = {}

    def get_destination_data(self):
        try:
            response = requests.get(url=SHEETY_PRICES_ENDPOINT, auth=self._authorization)
            print("Request Headers:", response.request.headers)  # Debug header
            print("Request URL:", response.request.url)  # Debug URL

            if response.status_code == 200:
                data = response.json()
                if "prices" in data:
                    self.destination_data = data["prices"]
                else:
                    print("Key 'prices' not found in the response.")
                    self.destination_data = []
            else:
                print(f"Failed to retrieve data. Status code: {response.status_code}")
                print("Response Text:", response.text)
        except Exception as e:
            print(f"Exception occurred: {e}")

        return self.destination_data

    def update_destination_codes(self):
        try:
            for city in self.destination_data:
                new_data = {
                    "price": {
                        "iataCode": city["iataCode"]
                    }
                }
                response = requests.put(
                    url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                    json=new_data,
                    auth=self._authorization
                )
                print("PUT Request URL:", response.request.url)  # Debug URL
                print("PUT Request Headers:", response.request.headers)  # Debug header
                if response.status_code == 200:
                    print("Update successful:", response.text)
                else:
                    print("Failed to update. Status code:", response.status_code)
                    print("Response Text:", response.text)
        except Exception as e:
            print(f"Exception occurred: {e}")
