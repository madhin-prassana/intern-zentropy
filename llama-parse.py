from llama_parse import LlamaParse
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("LLAMA_CLOUD_API_KEY")
parser = LlamaParse(result_type="markdown", verbose=True)
pdf_path = "sample_data/apple_data.pdf"
documents = parser.load_data(pdf_path)
output_file = "output_data/llama-parse(apple).md"
with open(output_file, "w", encoding="utf-8") as f:
    for doc in documents:
        f.write(doc.text + "\n")

print(f"\nParsed content saved to {output_file}")

#API via LlamaCloud, so far the best at parsing pdf data but online and can't be used for sensitive data.
#Takes a few minutes for larger files, especially involving images.