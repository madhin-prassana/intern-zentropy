import os
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

load_dotenv()

def load_parsed_pdf(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

pdf_context = load_parsed_pdf("output_data/amalgamation(llama).md")

client = ChatCompletionsClient(
    endpoint="https://models.github.ai/inference",
    credential=AzureKeyCredential(os.getenv("GITHUB_TOKEN")),
)

model = "openai/gpt-4.1"
system_prompt = "You are a helpful assistant that answers questions taking the provided document as context."

def ask_question(question):
    messages = [
        SystemMessage(system_prompt),
        UserMessage(f"This is the document:\n{pdf_context[:12000]}"),
        UserMessage(f"Answer questions based on the above:\n{question}")
    ]
    response = client.complete(
        messages=messages,
        temperature=0.7,
        top_p=1,
        model=model
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    print("Ask questions about the document (type 'exit' to quit):\n")
    while True:
        q = input("> Madhin: ")
        if q.lower() in ["exit", "quit"]:
            break
        answer = ask_question(q)
        print("> ChatGPT:", answer)