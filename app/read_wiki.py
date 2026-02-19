import wikipediaapi
import requests
from io import BytesIO
from PIL import Image


def get_wiki_article(page_name = "Napoleon"):
    wiki = wikipediaapi.Wikipedia(
        user_agent='Great Man Index/1.0 (enoch.kharchuk@example.com)',
        language='en'
    )
    page = wiki.page(page_name)
    return page


def get_wiki_image(name):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{name.replace(' ', '_')}"
    response = requests.get(url, headers={"User-Agent": "Great Man Index/1.0"})

    if response.status_code != 200:
        return None

    data = response.json()

    if "thumbnail" not in data:
        return None

    img_response = requests.get(data["thumbnail"]["source"])
    if img_response.status_code != 200:
        return None

    return Image.open(BytesIO(img_response.content))