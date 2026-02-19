import pandas as pd
import os
from PIL import Image
from read_wiki import get_wiki_image

def get_person(keep_track = True):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    PERSON_FILE = os.path.join(script_dir, 'files', '1000Highest_hpi_2025.csv')
    SEEN_FILE = os.path.join(script_dir, 'files', 'seen_list.txt')

    try:
        person_df = pd.read_csv(PERSON_FILE)
    except FileNotFoundError:
        print(f"Error: Could not find {PERSON_FILE}")
        return None
    except KeyError:
        print("Error: CSV file does not have a 'name' column")
        return None

    if not keep_track:
        row = person_df.sample(1).iloc[0]
        return row['name'], row['occupation']

    seen_people = set()
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, 'r') as f:
            seen_people = set(line.strip() for line in f)

    unseen_df = person_df[~person_df['name'].isin(seen_people)]

    if unseen_df.empty:
        print("All people have been seen!")
        return None

    row = unseen_df.sample(1).iloc[0]
    selected_person = row['name']

    os.makedirs(os.path.dirname(SEEN_FILE), exist_ok=True)
    with open(SEEN_FILE, 'a', encoding='utf-8') as f:
        f.write(selected_person + '\n')

    return selected_person, row['occupation']

def get_person_picture(name, height=300, width=300):
    img = get_wiki_image(name)

    if img is None:
        return None

    img = img.resize((width, height), Image.LANCZOS)

    gray = img.convert('L')
    black = gray.point(lambda _: 0)
    img = Image.merge('RGB', [black, gray, black])

    return img