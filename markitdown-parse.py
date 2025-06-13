from markitdown import MarkItDown

md = MarkItDown(enable_plugins=False)
result = md.convert("sample_data/apple_data.pdf")
output_path = "output_data/markitdown-parse(apple).md"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(result.text_content)

print(f"Markdown saved to {output_path}")