import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"

class FlightSearch:
    def __init__(self):
        self._api_key = os.getenv("AMADEUS_API_KEY")
        self._api_secret = os.getenv("AMADEUS_SECRET")
        self._token = self._get_new_token()

    def _get_new_token(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }
        response = requests.post(TOKEN_ENDPOINT, headers=headers, data=data)

        if response.status_code == 200:
            token = response.json()['access_token']
            print(f"New token obtained: {token}")
            print(f"Token expires in {response.json()['expires_in']} seconds")
            return token
        else:
            print(f"Failed to retrieve token. Status code: {response.status_code}")
            print("Response Text:", response.text)
            return None

    def get_destination_code(self, city_name):
        headers = {"Authorization": f"Bearer {self._token}"}
        params = {
            "keyword": city_name,
            "max": "2",
            "include": "AIRPORTS",
        }
        response = requests.get(IATA_ENDPOINT, headers=headers, params=params)

        if response.status_code == 200:
            try:
                return response.json()["data"][0]['iataCode']
            except (IndexError, KeyError):
                print(f"Error extracting IATA code for {city_name}")
                return "Not Found"
        else:
            print(f"Failed to get IATA code. Status code: {response.status_code}")
            print("Response Text:", response.text)
            return "Not Found"

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        headers = {"Authorization": f"Bearer {self._token}"}
        params = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",
            "currencyCode": "GBP",
            "max": "10",
        }

        response = requests.get(FLIGHT_ENDPOINT, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get flight offers. Status code: {response.status_code}")
            print("Response Text:", response.text)
            return None
