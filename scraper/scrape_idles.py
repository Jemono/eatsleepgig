import json
import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")  # Adjust if needed
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def get_data_path(filename):
    return os.path.join(DATA_DIR, filename)


# ---------- Utility Functions ----------
def load_json(filename):
    filepath = get_data_path(filename)
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return [] if filename == "gigs.json" else {}


def save_json(filename, data):
    filepath = get_data_path(filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def normalize_address(city, country, venue):
    return f"{venue}, {city}, {country}"

def add_venue(address, venue, city, country, venues_db):
    if address not in venues_db:
        venues_db[address] = {
            "venue": venue,
            "city": city,
            "country": country,
            "latitude": None,
            "longitude": None
        }

def add_gig(gigs_list, band, date_str, time_str, venue, address):
    gigs_list.append({
        "name": band,
        "date": date_str,
        "time": time_str,
        "venue": venue,
        "address": address
    })

# ---------- Scraping Logic ----------
def scrape_idles_events():
    url = "https://www.idlesband.com/live/"
    band = "IDLES"
    gigs = load_json("gigs.json")

    # ✅ Sanity check to ensure gigs is a list
    if not isinstance(gigs, list):
        print("⚠️ gigs.json is not a list. Resetting to empty list.")
        gigs = []

    print(f"Loaded gigs: {type(gigs)}")

    venues = load_json("venues.json")

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # run without GUI
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Get the full rendered page
    driver.get("https://www.idlesband.com/live/")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    event_blocks = soup.select(".bit-event")
    print(f"Found {len(event_blocks)} event blocks")  # sanity check



    for event in event_blocks:
        date_text = event.select_one(".bit-date").get_text(strip=True)
        time_el = event.select_one(".bit-startTime")
        time_text = time_el.get_text(strip=True) if time_el else "Time not listed"

        if not time_el:
            print("⚠️ No start time found for an event block.")

        venue_text = event.select_one(".bit-venue").get_text(strip=True)
        location_text = event.select_one(".bit-location-under-desktop").get_text(strip=True)


        # Convert date to ISO format
        try:
            date_obj = datetime.strptime(date_text, "%d %b %Y")
            date_str = date_obj.strftime("%Y-%m-%d")
        except ValueError:
            date_str = None

        time_str = time_text if time_text else None

    # Parse city and country
        try:
            city, country = location_text.split(", ")
        except ValueError:
            city = location_text
            country = ""

        address = normalize_address(city, country, venue_text)

        add_gig(gigs, band, date_str, time_str, venue_text, address)
        add_venue(address, venue_text, city, country, venues)


    # Save results
    save_json("gigs.json", gigs)
    save_json("venues.json", venues)
    print(f"Scraped {len(event_blocks)} events for {band} 🎉")

# ---------- Run the Scraper ----------
if __name__ == "__main__":
    scrape_idles_events()
