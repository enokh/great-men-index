import anthropic
from dotenv import load_dotenv

load_dotenv()


def generate_summary(page) -> str:
    """Generate a 3-paragraph summary of a wikipediaapi page using Claude."""
    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Below is the Wikipedia article for '{page.title}'.\n\n"
                    f"{page.text}\n\n"
                    "Write a concise 4-paragraph summary of this person's life and significance. "
                    "The first paragraph should cover their early life and background. "
                    "The second their major achievements and contributions, "
                    "with speical focus on their majour beliefs and ideals where applicable. "
                    "The third-fourththeir legacy and historical impact."
                ),
            }
        ],
    )

    return message.content[0].text