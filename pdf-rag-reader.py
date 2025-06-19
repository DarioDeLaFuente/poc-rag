import pymupdf4llm
import pathlib

# Create markdown_docs folder if it doesn't exist
markdown_folder = pathlib.Path("markdown_docs")
markdown_folder.mkdir(exist_ok=True)

# Convert PDF to markdown
md_text = pymupdf4llm.to_markdown("Pristilbud.pdf")

# Save the markdown file in the markdown_docs folder
output_path = markdown_folder / "Pristilbud.md"
output_path.write_bytes(md_text.encode())