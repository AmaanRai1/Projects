from pybaseball import statcast_pitcher
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Cache the data fetching to avoid repeated API calls
@st.cache_data
def load_pitcher_data(pitcher_id, start_date, end_date):
    return statcast_pitcher(start_date, end_date, pitcher_id)

# Streamlit App
st.title("Pitch Arsenal Heatmaps")

# User inputs for pitcher and pitch type
pitcher_id = st.text_input("Enter Pitcher ID:", value="664350")  # Example: Paul Skenes
start_date = st.text_input("Start Date (YYYY-MM-DD):", value="2024-01-01")
end_date = st.text_input("End Date (YYYY-MM-DD):", value="2024-12-31")

if pitcher_id and start_date and end_date:
    # Load and preprocess the data
    data = load_pitcher_data(pitcher_id, start_date, end_date)
    
    if not data.empty:
        # Filter and clean data
        pitch_data = data[['pitch_type', 'plate_x', 'plate_z']].dropna()
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
            sns.kdeplot(
                x=filtered_data['plate_x'], 
                y=filtered_data['plate_z'], 
                cmap="coolwarm", fill=True, thresh=0.05
            )
            plt.title(f"{selected_pitch} Heatmap", fontsize=16)
            plt.xlabel("Horizontal Location (plate_x)")
            plt.ylabel("Vertical Location (plate_z)")
            plt.xlim(-2, 2)
            plt.ylim(-2, 6)
            st.pyplot(plt.gcf())  # Display in Streamlit

        # Calculate and display pitch percentages
        pitch_counts = pitch_data['pitch_type'].value_counts()
        pitch_percentages = (pitch_counts / pitch_counts.sum() * 100).round(2)
        st.write("### Pitch Type Breakdown")
        st.bar_chart(pitch_percentages)

    else:
        st.error("No data available for the specified pitcher and date range.")
