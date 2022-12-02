import ijson
import sqlite3
import shutil
import os
import requests

def get_bulk_data(download_url, timestamp):
    # create a tmp dir
    tmp_dir = './tmp'
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    dst = f'./tmp/all-cards-{timestamp}.json'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
    r = requests.get(download_url, stream=True, headers=headers)
    if r.status_code == 200:
        with open(dst, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

    with open(f'./tmp/all-cards-{timestamp}.json', 'r') as f:
        objects = ijson.items(f, 'item')
        db = sqlite3.connect(f'./card_db/all-cards-{timestamp}.db')
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
    shutil.rmtree(tmp_dir)