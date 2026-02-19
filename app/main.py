from person_info import get_person, get_person_picture
from read_wiki import get_wiki_article
from generative_tools import generate_summary
from gui import MatrixWindow


def main(window):
    person, occupation = get_person(keep_track=True)
    print(f"Person Selected: {person}\n")
    print(f"Occupation: {occupation}\n")

    page = get_wiki_article(person)

    if page.exists():
        window.set_mark("retrieving_msg")
        print("Retrieving information...\n")
        summary = generate_summary(page)
        picture = get_person_picture(page.title, height=250, width=200)
        window.delete_from_mark("retrieving_msg")
        if picture:
            window.show_image(picture)
        else:
            print("[NO IMAGE AVAILABLE]\n")
        print(f"Profile:\n\n{summary}\n")
    else:
        print(f"No Information found for '{person}'.\n")


if __name__ == "__main__":
    window = MatrixWindow()
    window.run(main)