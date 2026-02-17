from get_person import get_person
from read_wiki import get_wiki_article 

def main():
    person = get_person(keep_track=True)

    print(f"Person Seleted: {person}")

    page = get_wiki_article(person)
    
    if page.exists():
        title = page.title
        content = page.text
        summary = page.summary
        print(f"Title: {title}\n")
        print(f"Summary: {summary}\n")
        
if __name__ == "__main__":


    main()