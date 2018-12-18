1 Data collection
The file “General_data_collection.py” gathers data from the official Develop API. It requests certain URL and stores them as json files.
2 Heat map
The file “Data_extraction.py” takes the raw json data file and extract death/weapon/medicine name and location information and stores them in separate csv files.
The file “general_heatmap.py” takes two input parameters: map and item. The first parameter indicates the map kind: 0 as Erangel, 1 as Miramar and 2 as Savage. The second parameter indicates the item kind: 0 as death, 1 as weapon and 2 as medicine.
3 Rank Prediction
The file “create_csv.py” takes in the raw data “match.json” file and outputs a csv file which contains the data during one game of each player. 
After getting csv file containing data during one game of each player, you can use the 3 python notebook files named Random_Forest, adbboost, and linear_model to do regression. 
4 Dynamic Match Visualization
Run “Preprocess_DynamicMatch.py” to generate data of players' positions and zones' positions in a match for each map: Savage_position.csv, Savage_zone.csv, Erangel_position.csv, Erangel_zone.csv, Desert_position.csv, Desert_zone.csv.
After generate the csv files, enter the command to start up local server in this DynamicMatch directory:
$ python3 -m http.server 5000
Go to the server by opening localhost:5000 in your browser.
matchErangel.html presents the dynamic process of a PUBG game on Erangel map.
matchSavage.html presents the dynamic process of a game on Savage map.
matchDesert.html presents the dynamic process of a game on Desert map. 