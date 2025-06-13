import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("OPENAI_API_KEY")

def chat(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=50
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    while True:
        user_input = input("> Madhin: ")
        if user_input.lower() in ("quit", "exit"):
            break
        response = chat(user_input)
        print("> ChatGPT:", response)