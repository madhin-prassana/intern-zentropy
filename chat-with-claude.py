import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def chat(prompt):
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        temperature=0.7,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text.strip()

if __name__ == "__main__":
    while True:
        user_input = input("> Madhin: ")
        if user_input.lower() in ("quit", "exit"):
            break
        response = chat(user_input)
        print("> Claude:", response)