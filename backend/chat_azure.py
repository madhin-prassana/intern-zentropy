import os
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

load_dotenv(dotenv_path="/Users/madhinprassana/PycharmProjects/PDF_parsing/.env")

pdf_context = ""

def load_parsed_pdf(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def set_pdf_context(file_path):
    global pdf_context
    pdf_context = load_parsed_pdf(file_path)
    print(f"Context updated from: {file_path}")

default_path = "output_data/amalgamation(llama).md"
if os.path.exists(default_path):
    set_pdf_context(default_path)

client = ChatCompletionsClient(
    endpoint="https://models.github.ai/inference",
    credential=AzureKeyCredential(os.getenv("GITHUB_TOKEN")),
)

model = "openai/gpt-4.1"
system_prompt = "You are a helpful assistant that answers questions based on the provided document context."

def ask_question(question):
    messages = [
        SystemMessage(system_prompt),
        UserMessage(f"This is the document:\n{pdf_context[:12000]}"),
        UserMessage(f"Answer this question based on the above:\n{question}")
    ]
    response = client.complete(
        messages=messages,
        temperature=0.7,
        top_p=1,
        model=model
    )
    return response.choices[0].message.content.strip()