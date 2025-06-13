from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered

def main():
    pdf_path = "sample_data/apple_data.pdf"
    output_path = "output_data/marker-parse(apple).md"
    converter = PdfConverter(artifact_dict=create_model_dict())
    rendered = converter(pdf_path)
    text, _, _ = text_from_rendered(rendered)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Markdown saved to {output_path}")

if __name__ == "__main__":
    main()

#LLM can be used alongside to best accuracy but has to be configured in the backend.