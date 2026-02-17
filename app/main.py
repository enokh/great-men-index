from person_info import get_person
from read_wiki import get_wiki_article
from generative_tools import generate_summary

def main():
    
    person = get_person(keep_track=True)

    print(f"Person Selected: {person}")

    page = get_wiki_article(person)

    if page.exists():
        print(f"\nName: {page.title}\n")
        summary = generate_summary(page)
        print(f"Summary:\n{summary}\n")
        
if __name__ == "__main__":


    main()