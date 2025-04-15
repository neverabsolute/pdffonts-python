# PDFFont Python Wrapper

This is a Python wrapper for the [PDFFonts](https://www.xpdfreader.com/pdffonts-man.html) command line tool, which provides functionality for working with PDF fonts. The wrapper allows you to quickly list out the fonts in a PDF file along with their properties, such as font name, type, and encoding.

## Installation

To install the PDFFonts Python wrapper, you can use pip:

```bash
pip install pdffonts-python
```

## Usage

```python
from pdffonts-python import PDFFonts

# Create an instance of PDFFonts
pdffonts = PDFFonts()

# List fonts in a PDF file
fonts = pdffonts.get_pdf_fonts("example.pdf")
print(fonts)
```

## Example Output

```json
[
  {
    "name": "AAAAAJ+Connections_Medium_CZEX0A80",
    "type": "Type 1C",
    "encoding": "Custom",
    "embedded": "yes",
    "subset": "yes",
    "unicode": "yes",
    "object": "12",
    "id": "0"
  },
  {
    "name": "AAAAAH+ConnectionsIta_CZEX0AC0",
    "type": "Type 1C",
    "encoding": "Custom",
    "embedded": "yes",
    "subset": "yes",
    "unicode": "yes",
    "object": "23",
    "id": "0"
  }
]
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
