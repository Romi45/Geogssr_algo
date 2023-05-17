# Geogssr_algo

Geogssr is a geography game built on tkinter with the help of the tkintermapview package developped by Tom Schimansky 
and the geopy package. It uses carto basempas in both light and dark modes.

IMPORTANT:
    This means you need to install tkintermapview and geopy. To do so:
    Using pip ==> open cmd and run "python3 pip install tkintermapview" and "python3 pip install geopy"
    Using conda ==> pip should be installed on conda so just run "pip install tkintermapview" and "pip install geopy"

    
The main file of our program is geogssr_main.py . This is the file that contains the game; the flags folder, the countries.csv and country_neighbours.json
are all data files that will be used by the program to display information and/or to run the game.

request_country.py is a file that we used to build a dataset, it is in the folder only as a code demonstrator and should not be ran.

Once the program starts, the user will be prompted with an intro screen that will explain how to handle and play the game. 

An internet connection is required to play as the game makes api calls to identify the geographical location of a click.

To start playing, just run geogssr_main.py. Have fun with our project !
