import requests
import pandas as pd

# Cargo API endpoint for structured Dustloop data
api_url = "https://www.dustloop.com/wiki/api.php"

# 'input' is required to catch names like 5P, 2K, etc.
params = {
    "action": "cargoquery",
    "tables": "MoveData_GGST",
    "fields": "name, input, damage, guard, startup, active, recovery, onBlock, invuln",
    "where": 'chara="Sol Badguy"',
    "format": "json",
    "limit": "500" 
}

headers = {'User-Agent': 'Mozilla/5.0'}

try:
    response = requests.get(api_url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()
    raw_results = data.get('cargoquery', [])
    moves = [item['title'] for item in raw_results]

    if moves:
        df_moves = pd.DataFrame(moves)
        
        # FIX: Replace empty 'name' strings with 'input' strings (e.g., 5P)
        df_moves['name'] = df_moves['name'].replace('', None)
        df_moves['name'] = df_moves['name'].fillna(df_moves['input'])
        
        # Mapping to your desired column format
        column_map = {
            "name": "Move",
            "damage": "Damage",
            "guard": "Guard",
            "startup": "Startup",
            "active": "Active",
            "recovery": "Recovery",
            "onBlock": "On-Block",
            "invuln": "Invuln"
        }
        df_moves = df_moves.rename(columns=column_map)
        
        # Clean up the extra 'input' column and sort for readability
        df_moves = df_moves.drop(columns=['input'])
        df_moves = df_moves.sort_values('Move')

        # Display the full table
        pd.set_option('display.max_rows', None)
        print(df_moves.to_string(index=False))
    else:
        print("No move data found in the database.")

except Exception as e:
    print(f"Error fetching data: {e}")
