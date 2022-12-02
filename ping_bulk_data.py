import requests
import json
import os
from get_bulk_data import get_bulk_data
import time


if __name__ == "__main__":
    while True:
        bulk_data_links = requests.get("https://api.scryfall.com/bulk-data").json()
        all_cards_download_link = bulk_data_links["data"][3]["download_uri"]
        timestamp = str(all_cards_download_link).split("-")[-1].split(".")[0]
        
        script_location = os.path.dirname(os.path.realpath(__file__))
        
        if os.path.exists(f"{script_location}/card_db/all-cards-{timestamp}.db"):
            print("File already exists")
            # wait 10 minutes
            time.sleep(600)
        else:
            print("Create a new db save")
            get_bulk_data(all_cards_download_link, timestamp)