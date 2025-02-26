import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

# Web Scraping from Basketball Reference
def scrape_player_game_log(player_id):
    url = f"https://www.basketball-reference.com/players/{player_id[0]}/{player_id}/gamelog/2025/"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data for {player_id}")
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find("table", {"id": "pgl_basic"})
    
    if not table:
        print(f"No game log found for {player_id}")
        return None
    
    df = pd.read_html(str(table))[0]
    df = df.dropna(how='all')
    df = df[df["G"] != "G"]
    
    return df

# List of players I want
players = {
    "Jalen Brunson": "brunsja01",
    "Karl-Anthony Towns": "townska01",
    "Nikola Jokic": "jokicni01",
    "Shai Gilgeous-Alexander": "gilgesh01",
    "Damian Lillard": "lillada01",
    "Kyrie Irving": "irvinky01",
    "Giannis Antetokounmpo": "antetgi01",
    "LeBron James": "jamesle01",
    "Jayson Tatum": "tatumja01",
    "Jaylen Brown": "brownja02"
}

for player, player_id in players.items():
    print(f"Fetching data for {player}...")
    game_log = scrape_player_game_log(player_id)
    
    if game_log is not None:
        file_name = f"{player.replace(' ', '_')}_GameLog_2025.csv"
        game_log.to_csv(file_name, index=False)
        print(f"Saved {player}'s game log to {file_name}")
    
print("Data scraping complete!")
