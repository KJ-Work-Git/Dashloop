import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.dustloop.com/w/GGST/Sol_Badguy"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

moves = []
containers = soup.find_all("div", class_="attack-container")

for container in containers:
    name_section = container.find_previous("h3")
    move_name = name_section.text.strip() if name_section else "Unknown Move"
    
    # Target the row containing the actual data values
    grid = container.find("div", class_="frameDataGridRow")
    if grid:
        # Extract all text from individual divs within the row
        cells = [cell.text.strip() for cell in grid.find_all("div")]
        
        # Mapping based on Dustloop's standard CSS Grid order:
        # 0: Damage | 1: Guard | 2: Startup | 3: Active | 4: Recovery | 5: On-Block | 6: Invuln
        if len(cells) >= 7:
            moves.append({
                "Move": move_name,
                "Damage": cells[0],
                "Guard": cells[1],      # Added
                "Startup": cells[2],
                "Active": cells[3],     # Added
                "Recovery": cells[4],   # Added
                "On-Block": cells[5],
                "Invuln": cells[6]      # Added
            })

# Create DataFrame
df_moves = pd.DataFrame(moves)

# Display the result
print(df_moves.to_string(index=False))
