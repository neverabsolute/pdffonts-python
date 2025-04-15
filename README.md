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
fonts = pdffonts.get_pdf_fonts('example.pdf')
print(fonts)
```

## Example Output

```json
[
  {
    "name": "F1",
    "type": "Type 1",
    "encoding": "WinAnsiEncoding",
    "embedded": false,
    "subtype": "Type1"
  },
  {
    "name": "F2",
    "type": "TrueType",
    "encoding": "Identity-H",
    "embedded": true,
    "subtype": "TrueType"
  }
]
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
