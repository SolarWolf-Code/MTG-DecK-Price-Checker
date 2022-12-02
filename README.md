# MTG-Deck-Price-Checker

## Script Setup
To use, setup a cronjob on your server to start ping_bulk_data.py
This will provide you with the most up-to-date bulk data provided by Scryfall API [Scryfall API](https://scryfall.com/docs/api/bulk-data).

Next, anytime you wish to check a deck/collections run this command:
```
python3 path/to/check_deck_price.py path/to/deck.txt
```
You will be asked how many days you would like to look back and you will be returned a percent difference between the most up-to-date data and that requested date.
##### NOTE: If the requested data is not present for whatever reason, it will look for the next closest day

Each new database should be around 15.5mb of data. If your server has low stoarge, consider upping the total time that you should wait.

##### You can freely search any amount of cards


## Deck file Setup
# !README needs updating
### Add how to get data from Moxfield
### Add how to add foil/foil-etched cards
### Add how to change langauge. Leave not note that most cards have a market for USD so some prices may appear empty
