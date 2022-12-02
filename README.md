# MTG-Deck-Price-Checker

## Script Setup
Requirements 
```
pip3 install ijson
```

To use, setup a cronjob on your server to start ping_bulk_data.py
This will provide you with the most up-to-date bulk data provided by [Scryfall API](https://scryfall.com/docs/api/bulk-data).

Next, anytime you wish to check a deck/collections run this command:
```
python3 path/to/check_deck_price.py path/to/deck.txt
```
You will be asked how many days you would like to look back and you will be returned a percent difference between the most up-to-date data and that requested date.
##### NOTE: If the requested data is not present for whatever reason, it will look for the next closest day

Each new database should be around 15.5mb of data and you will be required to download a 1.5gb json file (this is a temporary file). If your server has low storage, consider upping the total time that you should wait.

##### You can freely search any amount of cards


## Deck file Setup
Navigate to your Moxfield deck page and find the More button:

![image](https://user-images.githubusercontent.com/54452723/205231730-35bc335c-52bd-40de-a814-125e635c8e3b.png)

Select Export:

![image](https://user-images.githubusercontent.com/54452723/205231797-ae1ea87e-a6a7-48bf-a6dd-aa68f367f77c.png)

Click Copy Full List:

![image](https://user-images.githubusercontent.com/54452723/205232015-e0caf9d3-a9d3-48b4-9c93-53186caf1c53.png)

Paste the contents into a txt file inside the decks folder:

![image](https://user-images.githubusercontent.com/54452723/205232340-7174cc85-2ad5-4657-a3cd-d799d01ea5fa.png)

![image](https://user-images.githubusercontent.com/54452723/205232411-4044e88c-f12c-4576-a922-9917aa16fbd7.png)

![image](https://user-images.githubusercontent.com/54452723/205232467-d30a7850-7c8f-4f8c-968d-83eaf7221b55.png)

Most decks will be fine just like this but for decks with foil/foil-etched cards and cards with different languages, some additional steps are required.

### Card Types (Normal, Foil, Foil-Etched)
#### Adding Foil cards by adding a {F} to the end of the line:
```
1 Example Foil Card (exa) 999 {F}
```
#### Adding Foil-Etched cards by adding a {F} to the end of the line:
```
1 Example Foil-Etched Card (exa) 999 {E}
```
### Card Lanuage
#### Note: Some cards may not have price data for a language requested. If this become a problem, open a issue and I can look into it.
#### Adding Languages to cards by adding a {LANG} to the end of the line:
##### All languages so far are 2-3 characters. See below for supported languages
```
1 Example Foreign Card (exa) 999 {FR}
```
##### Example above is French

#### Example of Foil+Foreign Card:
```
1 Example Foreign Card (exa) 999 {F}{FR}
```


#### Supported Languages:
```
en - English
fr - French
pt - Portuguese
ja - Japanese
ru - Russian
de - German
es - Spanish
ko - Korean
it - Italian
zhs - Mandarin Chinese (Simplified)
zht - Mandarin Chinese (Traditional)
ph - Taglog ?
sa - Sanskrit ?
he - Hebrew
ar - Arabic
grc - Greek
la - Latin ?
```
The above are my best guesses at the languages that appear in the database.

"In addition to English, Magic: The Gathering has been printed in French, German, Italian, Portuguese, Spanish, Russian, Korean, Japanese, Simplified Chinese and Traditional Chinese." - [TCGPlayer Help](https://help.tcgplayer.com/hc/en-us/articles/204524213-How-do-I-identify-Magic-The-Gathering-languages-#:~:text=In%20addition%20to%20English%2C%20Magic,Simplified%20Chinese%20and%20Traditional%20Chinese.)
