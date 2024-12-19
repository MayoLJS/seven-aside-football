import pandas as pd
import math
import random
from collections import defaultdict
import streamlit as st

# Function to create teams with balanced ratios
def create_balanced_teams(players, num_teams):
    RATIO = {'ATT': 2, 'MID': 3, 'DEF': 2}
    TOTAL_RATIO = sum(RATIO.values())
    MAX_TEAM_SIZE = 7

    # Ensure there are enough players to form teams
    position_counts = {pos: len([p for p in players if p[1] == pos]) for pos in RATIO}
    total_players = len(players)
    
    min_teams = max(1, math.ceil(total_players / MAX_TEAM_SIZE))
    num_teams = min(num_teams, min_teams)
    
    team_size = total_players // num_teams
    extra_players = total_players % num_teams

    # Shuffle the players for random distribution
    random.shuffle(players)

    players_by_position = {pos: [p for p in players if p[1] == pos] for pos in RATIO}

    teams = defaultdict(list)
    for team_idx in range(1, num_teams + 1):
        for pos, count in RATIO.items():
            for _ in range(math.floor(count / TOTAL_RATIO * team_size)):
                if players_by_position[pos]:
                    teams[team_idx].append(players_by_position[pos].pop(0))

    remaining_players = []
    for pos, players_list in players_by_position.items():
        remaining_players.extend([(player, pos) for player in players_list])

    # Distribute remaining players
    for idx, player in enumerate(remaining_players):
        team_idx = (idx % num_teams) + 1
        teams[team_idx].append(player)

    return teams

# Streamlit App
st.title("Team Assignment App")
st.write("Enter player names and positions in the format `Name - Position` (e.g., `Tony - ATT`, `Mayo - DEF`).")

# Text input for player names and positions
input_data = st.text_area("Enter player data (e.g., `Tony - ATT`):")

# Input for number of teams
num_teams = st.number_input("Enter the number of teams you want to create:", min_value=1, step=1)

if input_data:
    try:
        # Parse the input data
        players = []
        lines = input_data.splitlines()
        for line in lines:
            parts = line.split('-')
            if len(parts) == 2:
                name = parts[0].strip()
                position = parts[1].strip().upper()
                if position in ['ATT', 'MID', 'DEF']:
                    players.append((name, position))
                else:
                    st.warning(f"Invalid position '{position}' for player '{name}'. Only 'ATT', 'MID', and 'DEF' are allowed.")
                    players = []  # Reset players list if any invalid position is found
                    break

        if players:
            # Create teams
            teams = create_balanced_teams(players, num_teams)

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
