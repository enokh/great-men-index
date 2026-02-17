import pandas as pd
import os 
import random

def get_person(keep_track = True):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    PERSON_FILE = os.path.join(script_dir, 'files', '1000Highest_hpi_2025.csv')
    SEEN_FILE = os.path.join(script_dir, 'files', 'seen_list.txt')
    
    try:
        person_df = pd.read_csv(PERSON_FILE)
        all_people = person_df['name'].tolist()
    except FileNotFoundError:
        print(f"Error: Could not find {PERSON_FILE}")
        return None
    except KeyError:
        print("Error: CSV file does not have a 'name' column")
        return None

    if not keep_track:
        return random.choice(all_people)

    seen_people = set()
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, 'r') as f:
            seen_people = set(line.strip() for line in f)

    unseen_people = [person for person in all_people if person not in seen_people]

    if not unseen_people:
        print("All people have been seen!")
        return None
    
    selected_person = random.choice(unseen_people)

    os.makedirs(os.path.dirname(SEEN_FILE), exist_ok=True)
    with open(SEEN_FILE, 'a', encoding='utf-8') as f:
        f.write(selected_person + '\n')
    
    return selected_person

def get_person_photo(name):
    return None