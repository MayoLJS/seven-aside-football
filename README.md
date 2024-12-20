
# Team Assignment App

This project is a Python-based application designed to create balanced teams from a list of players and their assigned positions. It uses **Streamlit** to provide a user-friendly interface for inputting player data and generating team assignments.

---

## Features
- Creates **balanced teams** based on predefined position ratios:
  - 2 attackers (`ATT`)
  - 3 midfielders (`MID`)
  - 2 defenders (`DEF`)
- Handles **random distribution** of players.
- Ensures no team exceeds the maximum size of 7 players.
- Allows users to:
  - Input player names and positions in the format `Name - Position` (e.g., `Tony - ATT`).
  - Specify the desired number of teams.
- Displays the teams in a table format on the app.
- Exports the team assignments to an **Excel file** for download.

---

## Installation

1. Clone this repository or download the project files.
2. Install the required libraries using pip:

   ```bash
   pip install pandas streamlit
   ```

3. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

---

## How to Use

1. Launch the app by running the command: `streamlit run app.py`.
2. Enter the player data in the **text area** in the format: `Name - Position`. For example:
   ```
   Tony - ATT
   Mayo - DEF
   Jane - MID
   ```
3. Specify the number of teams you want to create.
4. View the generated teams directly in the app.
5. Download the team assignments as an Excel file by clicking the **Download Teams as Excel** button.

---

## Code Breakdown

### Libraries Used
- **pandas**: For handling tabular data.
- **math**: For calculations like rounding numbers.
- **random**: To shuffle the players for random distribution.
- **defaultdict**: For easier dictionary handling.
- **streamlit**: To create the interactive web app.

### Core Functionality

#### **`create_balanced_teams`**
This function takes a list of players and their positions, along with the number of teams, to generate balanced teams based on predefined ratios.

#### Key Steps:
1. Counts available players for each position.
2. Shuffles players for randomness.
3. Assigns players to teams based on position ratios.
4. Handles leftover players by distributing them evenly.

#### Streamlit Integration
- Provides a **text area** for player input.
- Allows specifying the number of teams.
- Displays team assignments in a table.
- Exports teams to an Excel file for download.

---

## Example Input and Output

### Input
- Player Data:
  ```
  Tony - ATT
  Mayo - DEF
  Jane - MID
  Bob - ATT
  Alice - MID
  Chris - DEF
  ```
- Number of Teams: `2`

### Output (Displayed in App and Downloadable)
#### **Team 1**
| Name  | Position |
|-------|----------|
| Tony  | ATT      |
| Jane  | MID      |
| Chris | DEF      |

#### **Team 2**
| Name   | Position |
|--------|----------|
| Bob    | ATT      |
| Alice  | MID      |
| Mayo   | DEF      |

---

## Error Handling
- Warns if invalid positions are entered (only `ATT`, `MID`, `DEF` are allowed).
- Displays user-friendly error messages if something goes wrong.

---

## Contributing
If you'd like to contribute to this project, feel free to submit a pull request or raise an issue!

---

## License
This project is licensed under the MIT License.

---

## Contact
For questions or feedback, feel free to reach out!

