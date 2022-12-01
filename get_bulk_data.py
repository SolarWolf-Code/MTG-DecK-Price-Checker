import requests
import json
import sqlite3



def get_bulk_data(download_url, timestamp):
    data = requests.get(download_url).json()
    conn = sqlite3.connect(f"./card_db/all-cards-{timestamp}.db")
    c = conn.cursor()
    # we want the card name, language, set, collector number, usd, usd_foil, usd_etched
    c.execute('''CREATE TABLE cards (name text, lang text, set_code text, collector_number text, usd real, usd_foil real, usd_etched real)''')
    for card in data:
        name = card["name"]
        lang = card["lang"]
        set_code = card["set"]
        collector_number = card["collector_number"]
        usd = card["prices"]["usd"]
        usd_foil = card["prices"]["usd_foil"]
        usd_etched = card["prices"]["usd_etched"]
        c.execute("INSERT INTO cards VALUES (?, ?, ?, ?, ?, ?, ?)", (name, lang, set_code, collector_number, usd, usd_foil, usd_etched))
    conn.commit()
    conn.close()