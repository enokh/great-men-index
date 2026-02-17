import wikipediaapi


def get_wiki_article(page_name = "Napoleon"):
    wiki = wikipediaapi.Wikipedia(
        user_agent='Great Man Index/1.0 (enoch.kharchuk@example.com)',
        language='en'
    )
    page = wiki.page(page_name)
    return page