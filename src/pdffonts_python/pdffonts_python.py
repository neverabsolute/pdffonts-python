import subprocess
from typing import Union


class PDFFonts:
    """
    A class to parse the output of the `pdffonts` command-line tool.
    The `pdffonts` command is part of the Poppler utilities and is used to list
    the fonts used in a PDF file.
    """

    def __init__(self):
        # The set of possible PDF font type strings.
        self.__pdf_font_types = [
            "Type 1",
            "Type 1C",
            "Type 1C (OT)",
            "Type 3",
            "TrueType",
            "TrueType (OT)",
            "CID Type 0",
            "CID Type 0C",
            "CID Type 0C (OT)",
            "CID TrueType",
            "CID TrueType (OT)",
        ]

        # Store them also in a list of token lists (for matching from the right).
        self.__pdf_font_types_tokenized = [t.split() for t in self.__pdf_font_types]
        # Sort to match the longest possible type first:
        # e.g. ["CID", "Type", "0C", "(OT)"] is 4 tokens
        # before e.g. ["CID", "Type", "0C"] which is 3 tokens.
        self.__pdf_font_types_tokenized.sort(key=lambda x: len(x), reverse=True)

    def __parse_pdffonts_line(self, line: str) -> Union[dict, None]:
        """
        Parse a single non-header line from pdffonts output into a dict:

            {
                "name": str or None,
                "type": str,
                "encoding": str,
                "emb": str,
                "sub": str,
                "uni": str,
                "object": str,
                "id": str
            }

        Returns None if the line is malformed.
        """
        tokens = line.split()
        if len(tokens) < 8:
            return None

        # Parse from the right for columns that are always "single-token" columns:
        id_field = tokens[-1]
        object_field = tokens[-2]
        uni_field = tokens[-3]
        sub_field = tokens[-4]
        emb_field = tokens[-5]
        encoding_field = tokens[-6]

        # The tokens left (up to -6) represent [ name... , type... ]
        left_tokens = tokens[:-6]
        if not left_tokens:
            return None

        # Next find the correct "type" from the right side of `left_tokens`.
        # Because "CID Type 0C (OT)" has 4 tokens, "TrueType (OT)" has 2, etc.
        # Try to match the largest possible known type from the right.
        found_type = None
        found_type_tokens_count = 0

        for candidate_tokens in self.__pdf_font_types_tokenized:
            n = len(candidate_tokens)
            # if left_tokens ends with those candidate tokens, we have a match
            if left_tokens[-n:] == candidate_tokens:
                found_type = " ".join(candidate_tokens)
                found_type_tokens_count = n
                break

        if not found_type:
            # If we didn't match any multi-token type, fallback to the last single token as type
            # This is a "best effort" fallback.
            found_type = left_tokens[-1]
            found_type_tokens_count = 1

        # Everything before that is the name
        name_tokens = left_tokens[:-found_type_tokens_count]
        name_field = " ".join(name_tokens)
        if name_field.strip() == "[none]":
            name_field = None

        return {
            "name": name_field,
            "type": found_type,
            "encoding": encoding_field,
            "embedded": emb_field,
            "subset": sub_field,
            "unicode": uni_field,
            "object": object_field,
            "id": id_field,
        }

    def get_pdf_fonts(self, pdf_path: str) -> list[dict]:
        """
        Runs pdffonts on pdf_path, parses the output lines,
        and returns a list of font-info dictionaries.
        Raises CalledProcessError if pdffonts fails.
        """
        proc = subprocess.run(["pdffonts", pdf_path], capture_output=True, text=True)
        if proc.returncode != 0:
            raise subprocess.CalledProcessError(
                proc.returncode, proc.args, output=proc.stdout, stderr=proc.stderr
            )

        lines = proc.stdout.splitlines()
        # Lines[0] is the header, lines[1] is the dashed separator.
        # Actual font data lines start from lines[2].
        data_lines = lines[2:]

        results = []
        for line in data_lines:
            line = line.strip()
            if not line:
                continue
            row_data = self.__parse_pdffonts_line(line)
            if row_data:
                results.append(row_data)

        return results
