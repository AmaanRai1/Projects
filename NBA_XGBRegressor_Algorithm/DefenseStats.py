from nba_api.stats.endpoints import leaguedashteamstats
import pandas as pd

# NBA API
df = leaguedashteamstats.LeagueDashTeamStats(
    per_mode_detailed='PerGame',  
    measure_type_detailed_defense='Opponent'
).get_data_frames()[0]
df_defense = df[['TEAM_NAME', 'OPP_PTS', 'OPP_FG_PCT', 'OPP_FG3_PCT', 'OPP_TOV', 'OPP_STL', 'OPP_BLK', 'OPP_OREB']]

team_abbreviations = {
    "Atlanta Hawks": "ATL",
    "Boston Celtics": "BOS",
    "Brooklyn Nets": "BKN",
    "Charlotte Hornets": "CHA",
    "Chicago Bulls": "CHI",
    "Cleveland Cavaliers": "CLE",
    "Dallas Mavericks": "DAL",
    "Denver Nuggets": "DEN",
    "Detroit Pistons": "DET",
    "Golden State Warriors": "GSW",
    "Houston Rockets": "HOU",
    "Indiana Pacers": "IND",
    "Los Angeles Clippers": "LAC",
    "Los Angeles Lakers": "LAL",
    "Memphis Grizzlies": "MEM",
    "Miami Heat": "MIA",
    "Milwaukee Bucks": "MIL",
    "Minnesota Timberwolves": "MIN",
    "New Orleans Pelicans": "NOP",
    "New York Knicks": "NYK",
    "Oklahoma City Thunder": "OKC",
    "Orlando Magic": "ORL",
    "Philadelphia 76ers": "PHI",
    "Phoenix Suns": "PHX",
    "Portland Trail Blazers": "POR",
    "Sacramento Kings": "SAC",
    "San Antonio Spurs": "SAS",
    "Toronto Raptors": "TOR",
    "Utah Jazz": "UTA",
    "Washington Wizards": "WAS"
}
df_defense['TEAM_NAME'] = df_defense['TEAM_NAME'].map(team_abbreviations)
df_defense.to_csv('team_defense_stats.csv', index = False)
