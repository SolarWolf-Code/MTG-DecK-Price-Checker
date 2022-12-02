import sqlite3
import sys
import re
import time
import os

def main(deck_filename):
    script_location = os.path.dirname(os.path.realpath(__file__))
    # open the deck file
    with open(deck_filename, "r") as deck_file:
        deck = deck_file.read().splitlines()

    # ask the user for input on how far back they want to see a price difference for
    days = int(input("How many days back do you want to check? "))
    print("\n\n")
    requested_days = days

    # we want to search for the db that is closest to the requested days
    files = os.listdir(f"{script_location}/card_db")
    db_found = False
    while db_found == False:
        date = time.strftime("%Y%m%d", time.localtime(time.time() - (days * 86400)))
        for file in files:
            if date in file:
                db_found = True
                requested_db = file
                # if the date found is not the exact date requested, let the user know
                if date != time.strftime("%Y%m%d", time.localtime(time.time() - (requested_days * 86400))):
                    # make data 2022-11-29 instead of 20221129
                    formatted_date = date[:4] + "-" + date[4:6] + "-" + date[6:]
                    requested_date = time.strftime("%Y%m%d", time.localtime(time.time() - (requested_days * 86400)))
                    requested_formatted_date = requested_date[:4] + "-" + requested_date[4:6] + "-" + requested_date[6:]
                    print(f"{requested_formatted_date} not found. Closest date found: {formatted_date}")
                break
        days -= 1
        if db_found == True:
            break
        if days == 0:
            print("No db found for that many days back!")
            sys.exit()

    def get_price(requested_db):
        total_price = 0
        db = sqlite3.connect(f"{script_location}/card_db/{requested_db}")
        for card in deck:
            card_count = card.split(" ")[0]
            card_name = " ".join(card.split(" ")[1:-1]).split(" (")[0]
            card_set = card.split(" (")[1].split(")")[0]
            card_cn = card.split(" (")[1].split(")")[1].split(" ")[1].split(" ")[0]

            # check for languages using regex. Example is {FR} or {ZHS}
            # the regex is looking for a { followed by 2 or more characters followed by }

            # if there is a match, then the card is in a language other than english
            if re.search(r"{\w{2,}}", card):
                card_lang = re.search(r"{\w{2,}}", card).group().replace("{", "").replace("}", "")
            else:
                card_lang = "en"

            if "{F}" in card:
                card_type = "Foil"
            elif "{E}" in card:
                card_type = "Etched"
            else:
                card_type = "Normal"

            # do a search in the db
            c = db.cursor()
            c.execute("SELECT * FROM cards WHERE name=? AND lang=? AND set_code=? AND collector_number=?", (card_name, card_lang, card_set, card_cn))
            card_data = c.fetchone()
            if len(card_data) == 0:
                #print("Card not found")
                raise Exception("Card not found")
            if card_type == "Normal":
                card_price = card_data[4]
            elif card_type == "Foil":
                card_price = card_data[5]
            elif card_type == "Etched":
                card_price = card_data[6]
            else:
                raise Exception("Card type not found")

            if card_price == None:
                print("Card price not found, you may need to update your decklist")
                card_price = 0

            total_price += float(card_price) * int(card_count)

        db.close()
        #print(f"Total price: {total_price:.2f}")
        return total_price
    
    
    past_price = get_price(requested_db)
    # get the most recent db by sorting the files list by date
    files = sorted(files, key=lambda x: x.split("-")[-1].split(".")[0])
    most_recent_db = files[-1]
    current_price = get_price(most_recent_db)

    print()
    if past_price == 0 and current_price == 0:
        print("No price data found for this deck")
    elif past_price < current_price:
        # calculate percentage increase
        percent_increase = (current_price - past_price) / past_price * 100
        print(f"Current price: ${current_price:.2f}.Price increased by {percent_increase:.2f}%")
    elif past_price > current_price:
        # calculate percentage decrease
        percent_decrease = (current_price - past_price) / current_price * 100
        print(f"Current price: ${current_price:.2f}. Price decreased by {percent_decrease:.2f}%")
    else:
        print(f"Current price: ${current_price:.2f}. Price has not changed")


if __name__ == "__main__":
    main(sys.argv[1])
