import requests
import os
from get_bulk_data import get_bulk_data
import time
import sys
import shutil

if __name__ == "__main__":
    while True:
        script_location = os.path.dirname(os.path.realpath(__file__))
        # check if tmp dir exists
        tmp_dir = f'{script_location}/tmp'
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        try:
            # create logs dir
            logs_dir = f'{script_location}/logs'
            if not os.path.exists(logs_dir):
                os.makedirs(logs_dir)

            try_count = 0
            bulk_data_links = requests.get("https://api.scryfall.com/bulk-data")
            if bulk_data_links.status_code == 200:
                try_count = 0
                bulk_data_links = bulk_data_links.json()
                all_cards_download_link = bulk_data_links["data"][3]["download_uri"]
                timestamp = str(all_cards_download_link).split("-")[-1].split(".")[0]
                
                
                if os.path.exists(f"{script_location}/card_db/all-cards-{timestamp}.db"):
                    print("File already exists")
                    with open(f"{script_location}/logs/log.txt", "a") as add_log:
                        add_log.write(f"\n+ [{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}] - File already exists, waiting 10 minutes before trying again")
                    # wait 10 minutes
                    time.sleep(600)
                else:
                    print("Create a new db save")
                    with open(f"{script_location}/logs/log.txt", "a") as add_log:
                        add_log.write(f"\n+ [{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}] - Attempting to create a new db save")
                    get_bulk_data(all_cards_download_link, timestamp)
            else:
                if str(bulk_data_links.status_code).startswith("5"):
                    print("test")
                print("Status code:", bulk_data_links.status_code)

                print("Error: Status code is not 200, waiting 5 seconds before trying again...")
                time.sleep(5)
                if try_count != 10: # This will indicate the requests has failed 10 times in a row
                    try_count += 1
                else:
                    with open(f"{script_location}/logs/log.txt", "a") as error_log:
                        # write that the timestamp and the status code
                        error_log.write(f"\n! [{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}] - Status code: {bulk_data_links.status_code}")
                        # exit the program
                        sys.exit()
        except:
            # check if error was related to connection error
            if "ConnectionError" in str(sys.exc_info()[0]):
                print("Connection error, waiting 5 seconds before trying again...")
                time.sleep(5)
                # try again
                with open(f"{script_location}/logs/log.txt", "a") as error_log:
                    # write that the timestamp and the error
                    error_log.write(f"\n! [{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}] - {sys.exc_info()[0]}")
            else:
                with open(f"{script_location}/logs/log.txt", "a") as error_log:
                    # write that the timestamp and the error
                    error_log.write(f"\n! [{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}] - {sys.exc_info()[0]}")
                # exit the program
                sys.exit()