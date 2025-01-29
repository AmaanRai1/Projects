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
    # Lookup the pitcher by name
    player_info = playerid_lookup(last_name, first_name)
    if not player_info.empty:
        return player_info.iloc[0]['key_mlbam']  # Return the MLBAM ID
    else:
        return None

# Column layout
col1, col2 = st.columns([2, 1])  # Two columns: 2 parts for main content, 1 for the sidebar

with col1:
    st.title("MLB Pitcher Arsenal")
    st.write("Analyze pitch locations, outcomes, and trends.")

    # Input fields
    with st.expander("Enter Pitcher and Date Details"):
        first_name = st.text_input("Pitcher's First Name:", value="Paul")
        last_name = st.text_input("Pitcher's Last Name:", value="Skenes")
        start_date = st.text_input("Start Date (YYYY-MM-DD):", value="2024-01-01")
        end_date = st.text_input("End Date (YYYY-MM-DD):", value="2024-12-31")


if first_name and last_name:
    # Get pitcher ID from name
    pitcher_id = get_player_id(first_name, last_name)
    
    if pitcher_id:
        st.success(f"Pitcher ID found: {pitcher_id}")
        
        if start_date and end_date:
            # Load and preprocess data
            data = load_pitcher_data(pitcher_id, start_date, end_date)

            if not data.empty:
                # Filter and clean data
                pitch_data = data[['pitch_type', 'plate_x', 'plate_z', 'description']].dropna()
                
                # Remove bad plate_x or plate_z values
                pitch_data = pitch_data[(pitch_data['plate_x'].between(-3, 3)) & (pitch_data['plate_z'].between(-2, 6))]

                pitch_data = pitch_data.copy()  # No view issues
                pitch_data['pitch_type'] = pitch_data['pitch_type'].replace({
                    'FF': 'Four Seamer',
                    'SI': 'Sinker',
                    'CU': 'Curveball',
                    'SL': 'Slider',
                    'CH': 'Changeup',
                    'SW': 'Sweeper'
                })

                # Check for unique pitch types and display
                pitch_types = pitch_data['pitch_type'].unique()
                selected_pitch = st.selectbox("Select a pitch type:", pitch_types)
                    
                if selected_pitch:
                    filtered_data = pitch_data[pitch_data['pitch_type'] == selected_pitch]
                    plt.figure(figsize=(8, 6))
                    # Heatmap
                    sns.kdeplot(
                        x=filtered_data['plate_x'], 
                        y=filtered_data['plate_z'], 
                        cmap="coolwarm", fill=True, thresh=0.05
                        )
                    # Shaded strike zone
                    plt.fill_betweenx([1.5, 3.5], -0.83, 0.83, color='black', alpha=0.3, label="Strike Zone")
                    # Strike zone
                    plt.axvline(x=-0.83, color='black', linestyle='-', linewidth=1.5)  # Left boundary
                    plt.axvline(x=0.83, color='black', linestyle='-', linewidth=1.5)   # Right boundary
                    plt.axhline(y=1.5, color='black', linestyle='-', linewidth=1.5)    # Bottom boundary
                    plt.axhline(y=3.5, color='black', linestyle='-', linewidth=1.5)    # Top boundary

                    # Labels and title
                    plt.title(f"{selected_pitch} Heatmap with Strike Zone", fontsize=16)
                    plt.xlabel("Horizontal Location")
                    plt.ylabel("Vertical Location")
                    plt.xlim(-2.49, 2.49)
                    plt.ylim(0, 5)

                    # Legend for strike zone
                    plt.legend(loc="upper left")
                


                    # Plot
                    st.pyplot(plt.gcf())

                    # Outcome analysis
                    st.write("### Pitch Outcome Analysis")

                    # Frequency of each pitch outcome
                    outcome_counts = filtered_data['description'].value_counts()

                    # Bar chart for pitch outcomes
                    st.bar_chart(outcome_counts)

                    # Percentages
                    outcome_percentages = (outcome_counts / outcome_counts.sum() * 100).round(2)
                    st.write("#### Outcome Percentages")
                    st.dataframe(outcome_percentages)

                    plt.figure(figsize=(6, 6))

                    # Pie chart
                    outcome_counts.plot.pie(
                        autopct=lambda p: f'{p:.1f}%' if p > 5 else '',  # Only show percentages > 5%
                        startangle=90,
                        colormap="viridis",
                        legend=False,
                        labels=None
                    )

                    # Title and layout
                    plt.title(f"{selected_pitch} Outcome Distribution")
                    plt.tight_layout()
                    st.pyplot(plt.gcf())

                    # Pitch percentages
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
