from pybaseball import statcast_pitcher, playerid_lookup
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Cache the data fetching to avoid repeated API calls
@st.cache_data
def load_pitcher_data(pitcher_id, start_date, end_date):
    try:
        return statcast_pitcher(start_date, end_date, pitcher_id)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

@st.cache_data
def get_player_id(first_name, last_name):
    # Lookup the player's information by name
    player_info = playerid_lookup(last_name, first_name)
    if not player_info.empty:
        return player_info.iloc[0]['key_mlbam']  # Return the MLBAM ID
    else:
        return None

# Streamlit App
st.title("Pitch Arsenal Heatmaps")

# User inputs for pitcher name and date range
first_name = st.text_input("Enter Pitcher's First Name:", value="Paul")  # Example: Paul Skenes
last_name = st.text_input("Enter Pitcher's Last Name:", value="Skenes")
start_date = st.text_input("Start Date (YYYY-MM-DD):", value="2024-01-01")
end_date = st.text_input("End Date (YYYY-MM-DD):", value="2024-12-31")

if first_name and last_name:
    # Fetch the pitcher ID based on the name
    pitcher_id = get_player_id(first_name, last_name)
    
    if pitcher_id:
        st.success(f"Pitcher ID found: {pitcher_id}")
        
        if start_date and end_date:
            # Load and preprocess the data
            data = load_pitcher_data(pitcher_id, start_date, end_date)

            if not data.empty:
                # Filter and clean data
                pitch_data = data[['pitch_type', 'plate_x', 'plate_z', 'description']].dropna()
                
                # Remove invalid plate_x or plate_z values
                pitch_data = pitch_data[(pitch_data['plate_x'].between(-3, 3)) & (pitch_data['plate_z'].between(-2, 6))]

                pitch_data = pitch_data.copy()  # Ensure no view issues
                pitch_data['pitch_type'] = pitch_data['pitch_type'].replace({
                    'FF': 'Four Seamer',
                    'SI': 'Sinker',
                    'CU': 'Curveball',
                    'SL': 'Slider',
                    'CH': 'Changeup',
                    'SW': 'Sweeper'
                })

                # Check for unique pitch types and display selection
                pitch_types = pitch_data['pitch_type'].unique()
                selected_pitch = st.selectbox("Select a pitch type:", pitch_types)
                    
                if selected_pitch:
                    # Plot heatmap for the selected pitch type
                    filtered_data = pitch_data[pitch_data['pitch_type'] == selected_pitch]

                    plt.figure(figsize=(8, 6))

                    # Plot the heatmap
                    sns.kdeplot(
                        x=filtered_data['plate_x'], 
                        y=filtered_data['plate_z'], 
                        cmap="coolwarm", fill=True, thresh=0.05
                        )

                    # Add shaded strike zone
                    plt.fill_betweenx([1.5, 3.5], -0.83, 0.83, color='black', alpha=0.3, label="Strike Zone")

                    # Add strike zone boundaries
                    plt.axvline(x=-0.83, color='black', linestyle='-', linewidth=1.5)  # Left boundary
                    plt.axvline(x=0.83, color='black', linestyle='-', linewidth=1.5)   # Right boundary
                    plt.axhline(y=1.5, color='black', linestyle='-', linewidth=1.5)    # Bottom boundary
                    plt.axhline(y=3.5, color='black', linestyle='-', linewidth=1.5)    # Top boundary

                    # Add labels and title
                    plt.title(f"{selected_pitch} Heatmap with Strike Zone", fontsize=16)
                    plt.xlabel("Horizontal Location (plate_x)")
                    plt.ylabel("Vertical Location (plate_z)")
                    plt.xlim(-2, 2)
                    plt.ylim(-2, 6)

                    # Add legend for strike zone
                    plt.legend(loc="upper left")

                    # Display the plot
                    st.pyplot(plt.gcf())

                    # Outcome analysis
                    st.write("### Pitch Outcome Analysis")

                    # Calculate the frequency of each pitch outcome
                    outcome_counts = filtered_data['description'].value_counts()

                    # Create a bar chart for pitch outcomes
                    st.bar_chart(outcome_counts)

                    # Display percentages
                    outcome_percentages = (outcome_counts / outcome_counts.sum() * 100).round(2)
                    st.write("#### Outcome Percentages")
                    st.dataframe(outcome_percentages)

                    # Create a pie chart for pitch outcomes
                    plt.figure(figsize=(6, 6))
                    outcome_counts.plot.pie(autopct='%1.1f%%', startangle=90, colormap="viridis", legend=False)
                    plt.title(f"{selected_pitch} Outcome Distribution")
                    st.pyplot(plt.gcf())

                    # Calculate and display pitch percentages
                    pitch_counts = pitch_data['pitch_type'].value_counts()
                    pitch_percentages = (pitch_counts / pitch_counts.sum() * 100).round(2)
                    st.write("### Pitch Type Breakdown")
                    st.bar_chart(pitch_percentages)
                else:
                    st.error("No valid pitch types found in the data.")
            else:
                st.error("No data available for the specified pitcher and date range.")
    else:
        st.error(f"No player found with the name {first_name} {last_name}. Please check the spelling.")
