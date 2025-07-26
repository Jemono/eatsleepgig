import json
import os
import requests
from dotenv import load_dotenv
load_dotenv()
import os

OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY") 

GEOCODE_URL = "https://api.opencagedata.com/geocode/v1/json"

DATA_PATH = os.path.join("..", "data", "gigs.json")

print(f"Loaded API Key: {OPENCAGE_API_KEY}")


def geocode_address(address):
    params = {
        "q": address,
        "key": OPENCAGE_API_KEY,
        "limit": 1
    }
    response = requests.get(GEOCODE_URL, params=params)
    data = response.json()

    if data["results"]:
        geometry = data["results"][0]["geometry"]
        return geometry["lat"], geometry["lng"]
    else:
        print(f"Could not geocode address: {address}")
        return None, None


def add_event(name, date, time, venue, address):
    lat, lng = geocode_address(address)
    
    event = {
        "name": name,
        "date": date,
        "time": time,
        "venue": venue,
        "address": address,
        "latitude": lat,
        "longitude": lng
    }

    # rest of your JSON append logic...


    if not os.path.exists(DATA_PATH):
        with open(DATA_PATH, "w") as f:
            json.dump([event], f, indent=2)
        print(f"Created gigs.json and added: {name} on {date} at {venue}")
    else:
        with open(DATA_PATH, "r+") as f:
            gigs = json.load(f)
            gigs.append(event)
            f.seek(0)
            json.dump(gigs, f, indent=2)
        print(f"Added: {name} on {date} at {venue}")

if __name__ == "__main__":
    print("\n🎶 EatSleepGig Manual Entry 🎶")
    name = input("Band name: ")
    date = input("Date (YYYY-MM-DD): ")
    time = input("Time (HH:MM): ")
    venue = input("Venue name: ")
    address = input("Street address: ")
    add_event(name, date, time, venue, address)

