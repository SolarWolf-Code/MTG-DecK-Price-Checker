import ijson
import sqlite3
import shutil
import os
import requests
import time
import sys

def get_bulk_data(download_url, timestamp):
    try:
        # get script location
        script_location = os.path.dirname(os.path.realpath(__file__))

        # create a tmp dir
        tmp_dir = f'{script_location}/tmp'
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)

        dst = f'{script_location}/tmp/all-cards-{timestamp}.json'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
        r = requests.get(download_url, stream=True, headers=headers)
        if r.status_code == 200:
            with open(dst, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)


        with open(f'{script_location}/tmp/all-cards-{timestamp}.json', 'r') as f:
            objects = ijson.items(f, 'item')
            db = sqlite3.connect(f'{script_location}/tmp/all-cards-{timestamp}.db')
            cursor = db.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS cards (name text, lang text, set_code text, collector_number text, usd real, usd_foil real, usd_etched real)''')
            for obj in objects:
                # insert into database
                name = obj["name"]
                lang = obj["lang"]
                set_code = obj["set"]
                collector_number = obj["collector_number"]
                usd = obj["prices"]["usd"]
                usd_foil = obj["prices"]["usd_foil"]
                usd_etched = obj["prices"]["usd_etched"]
                cursor.execute("INSERT INTO cards VALUES (?, ?, ?, ?, ?, ?, ?)", (name, lang, set_code, collector_number, usd, usd_foil, usd_etched))
            db.commit()
            db.close()
        # delete the tmp dir and all of its contents
        # write to the log
        with open(f"{script_location}/logs/log.txt", "a") as add_log:
            add_log.write(f"\n+ [{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}] - Successfully created a new .db file")

        
        # create a gob_db dir
        gob_db_dir = f'{script_location}/gob_db'
        if not os.path.exists(gob_db_dir):
            os.makedirs(gob_db_dir)

        # call the db_to_gob executable to convert the .db file to a .gob file
        os.system(f"{script_location}/db_to_gob {script_location}/tmp/all-cards-{timestamp}.db {script_location}/gob_db/all-cards-{timestamp}.gob")
        shutil.rmtree(tmp_dir)

    except:
        # write to error log
        with open(f"{script_location}/logs/log.txt", "a") as error_log:
            error_log.write(f"\n! [{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}] - {sys.exc_info()[0]}")
        # exit the program
        sys.exit()