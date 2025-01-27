from pybaseball import statcast_pitcher
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Fetch data for a specific pitcher (e.g., Player ID 664350 for Paul Skenes in 2024)
start_date = "2024-01-01"
end_date = "2024-12-31"
pitcher_id = 664350  # Replace with the correct player ID
data = statcast_pitcher(start_date, end_date, pitcher_id)

# Preview the data
print(data.head())

# Filter for relevant columns
pitch_data = data[['pitch_type', 'plate_x', 'plate_z']]

pitch_data = pitch_data.copy()  # Ensure it's a full copy, not a view
pitch_data['pitch_type'] = pitch_data['pitch_type'].replace({
    'FF': 'Four Seamer',
    'SI': 'Sinker',
    'CU': 'Curveball',
    'SL': 'Slider',
    'CH': 'Changeup',
    'SW': 'Sweeper'
})


# Drop rows with missing data
pitch_data = pitch_data.dropna()


# Define a function to create heatmaps
def plot_pitch_heatmap(data, pitch_type, cmap):
    filtered_data = data[data['pitch_type'] == pitch_type]
    plt.figure(figsize=(8, 6))
    sns.kdeplot(
        x=filtered_data['plate_x'], 
        y=filtered_data['plate_z'], 
        cmap=cmap, 
        fill=True, 
        thresh=0.05
    )
    plt.title(f'{pitch_type} Heatmap', fontsize=16)
    plt.xlabel('Horizontal Location (plate_x)')
    plt.ylabel('Vertical Location (plate_z)')
    plt.xlim(-2, 2)
    plt.ylim(-2, 6)
    plt.show()

# Plot heatmaps for each pitch type
plot_pitch_heatmap(pitch_data, 'Four Seamer', 'Reds')
plot_pitch_heatmap(pitch_data, 'Sinker', 'Oranges')
plot_pitch_heatmap(pitch_data, 'Curveball', 'Blues')

# Calculate pitch percentages
pitch_counts = pitch_data['pitch_type'].value_counts()
pitch_percentages = pitch_counts / pitch_counts.sum() * 100

# Print the breakdown
print(pitch_percentages)

# Optional: Add to your visualizations
pitch_percentages.plot(kind='bar', color='skyblue', figsize=(8, 4), title='Pitch Type Breakdown')
plt.xlabel('Pitch Type')
plt.ylabel('Percentage')
plt.show()

# Streamlit app
st.title("Pitch Arsenal Heatmaps")
selected_pitch = st.selectbox("Select a pitch type:", pitch_data['pitch_type'].unique())

if selected_pitch:
    plot_pitch_heatmap(pitch_data, selected_pitch, 'coolwarm')
