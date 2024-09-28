from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from datetime import datetime, timedelta

def main():
    data_manager = DataManager()
    flight_search = FlightSearch()

    # Get destination data
    destination_data = data_manager.get_destination_data()
    print("Destination Data:", destination_data)

    # Update destination codes
    data_manager.update_destination_codes()

    # Example usage for finding cheapest flights
    origin_city_code = flight_search.get_destination_code("New York")
    destination_city_code = flight_search.get_destination_code("London")

    from_time = datetime.now() + timedelta(days=30)
    to_time = from_time + timedelta(days=7)

    flight_data = flight_search.check_flights(origin_city_code, destination_city_code, from_time, to_time)
    cheapest_flight = find_cheapest_flight(flight_data)
    print(f"Cheapest Flight: {cheapest_flight.price} from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport} on {cheapest_flight.out_date} returning on {cheapest_flight.return_date}")

if __name__ == "__main__":
    main()
