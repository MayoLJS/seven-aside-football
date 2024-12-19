import pandas as pd
import math
import random
from collections import defaultdict
import streamlit as st
import openpyxl

# Function to create teams with balanced ratios
def create_balanced_teams(data):
    RATIO = {'ATT': 2, 'MID': 3, 'DEF': 2}
    TOTAL_RATIO = sum(RATIO.values())
    MAX_TEAM_SIZE = 7

    position_counts = data['Position'].value_counts().to_dict()
    total_players = len(data)
    min_teams = max(1, math.ceil(total_players / MAX_TEAM_SIZE))
    max_possible_teams = min(position_counts[pos] // RATIO[pos] for pos in RATIO)
    num_teams = min(min_teams, max_possible_teams)

    team_size = total_players // num_teams
    extra_players = total_players % num_teams

    shuffled_data = data.sample(frac=1, random_state=random.randint(1, 1000)).reset_index(drop=True)

    players_by_position = {
        pos: shuffled_data[shuffled_data['Position'] == pos]['Name'].tolist()
        for pos in RATIO
    }

    teams = defaultdict(list)
    for team_idx in range(1, num_teams + 1):
        for pos, count in RATIO.items():
            for _ in range(math.floor(count / TOTAL_RATIO * team_size)):
                if players_by_position[pos]:
                    teams[team_idx].append((players_by_position[pos].pop(), pos))

    remaining_players = []
    for pos, players in players_by_position.items():
        remaining_players.extend([(player, pos) for player in players])

    for idx, player in enumerate(remaining_players):
        team_idx = (idx % num_teams) + 1
        teams[team_idx].append(player)

    return teams

# Streamlit App
st.title("Team Assignment App")
st.write("Upload a spreadsheet with columns `Name` and `Position` (ATT, MID, DEF) to create balanced teams.")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])
if uploaded_file:
    try:
        # Load the uploaded file
        data = pd.read_excel(uploaded_file)
        if 'Name' not in data.columns or 'Position' not in data.columns:
            st.error("Spreadsheet must contain `Name` and `Position` columns.")
        else:
            # Create teams
            teams = create_balanced_teams(data)

            # Display the teams in the app
            for team_idx, members in teams.items():
                st.subheader(f"Team {team_idx}")
                df = pd.DataFrame(members, columns=['Name', 'Position'])
                st.dataframe(df)

            # Save the output to a downloadable Excel file
            output_file = "teams_output.xlsx"
            with pd.ExcelWriter(output_file) as writer:
                for team_idx, members in teams.items():
                    df = pd.DataFrame(members, columns=['Name', 'Position'])
                    df.to_excel(writer, sheet_name=f'Team_{team_idx}', index=False)

            with open(output_file, "rb") as file:
                st.download_button(
                    label="Download Teams as Excel",
                    data=file,
                    file_name="teams_output.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    except Exception as e:
        st.error(f"An error occurred: {e}")
