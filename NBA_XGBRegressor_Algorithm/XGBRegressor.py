import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Change name of player (e.g. Jayson Tatum)
df = pd.read_csv("Jayson_Tatum_Full_Stats.csv")

features = [
    'H/A', 'OPP_PTS', 'Def_Rating', 
    'Rolling_MP', 'Rolling_FGA', 'Rolling_FGM', 'Rolling_FG_Perc',
    'Rolling_3PA', 'Rolling_3PM', 'Rolling_3P_Perc', 
    'Rolling_FT', 'Rolling_FTA', 'Rolling_FT_Perc'
]

target = 'PTS'

df = df.dropna(subset=features + [target])

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# XGBRegressor
model = XGBRegressor(n_estimators=100, learning_rate=0.05, max_depth=5, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"Root Mean Squared Error (RMSE): {rmse}")

# Fill in info for upcoming game
upcoming_games = pd.DataFrame({
    'H/A': [0], 'OPP_PTS': [113.3], 'Def_Rating': [112.4],
    'Rolling_MP': [2246.2], 'Rolling_FGA': [20.4], 'Rolling_FGM': [9], 'Rolling_FG_Perc': [0.43],
    'Rolling_3PA': [11], 'Rolling_3PM': [3.2], 'Rolling_3P_Perc': [.291],
    'Rolling_FT': [3.6], 'Rolling_FTA': [4.4], 'Rolling_FT_Perc': [0.900]
})

predicted_points = model.predict(upcoming_games)
print(f"Predicted Points: {predicted_points[0]}")
