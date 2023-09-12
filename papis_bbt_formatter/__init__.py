# adapted from https://github.com/hrdl-github/papis/commit/b9b9c6eaa3de159e1b210174ef49e90a89271eb8
# with much gratitude.
import re
from typing import Any
import papis.format
import papis.config
import papis.document

import papis.logging

logger = papis.logging.get_logger(__name__)

DEFAULT_TITLE_LENGTH=4

class BBTFormatter(papis.format.Formater):
    """Provides zotero better-bibtex-like keys."""

    def format(
        self,
        fmt: str,
        doc: papis.format.FormatDocType,
        doc_key: str = "",
        additional: dict[str, Any] = {},
    ) -> str:
        if fmt.startswith("bbt"):
            author_unfmt = (
                doc["author_list"][0]["family"]
                if "author_list" in doc
                else doc["author"].split(maxsplit=1)[0]
                if "author" in doc
                else "Unkown"
            )
            title_unfmt = doc["title"] if "title" in doc else "No title"
            year_unfmt = str(doc["year"]) if "year" in doc else "0000"

            author = re.sub("[^a-z]+", "", author_unfmt.lower())
            year = year_unfmt[-2:]
            title = re.sub("-", " ", title_unfmt.lower())
            title = re.sub("[^0-9a-z ]+", "", title)
            title = list(
                map(
                    str.capitalize,
                    filter(lambda word: word and word not in SKIP_WORDS, title.split()),
                )
            )
            title_len = self._title_length(fmt)
            title = "".join(title[:title_len])
            return f"{author}{year}_{title}"
        else:
            return papis.format.PythonFormater().format(fmt, doc, doc_key, additional)

    def _title_length(self, fmt: str) -> int:
        """Returns the length (in words) the title should be shortened to."""
        if match:=re.match(r'^bbt\[(\d+)\]', fmt):
            return int(match.group(1))
        return DEFAULT_TITLE_LENGTH

SKIP_WORDS = set(
    [
        "about",
        "above",
        "across",
        "afore",
        "after",
        "against",
        "al",
        "along",
        "alongside",
        "amid",
        "amidst",
        "among",
        "amongst",
        "anenst",
        "apropos",
        "apud",
        "around",
        "as",
        "aside",
        "astride",
        "at",
        "athwart",
        "atop",
        "barring",
        "before",
        "behind",
        "below",
        "beneath",
        "beside",
        "besides",
        "between",
        "beyond",
        "but",
        "by",
        "circa",
        "despite",
        "down",
        "during",
        "et",
        "except",
        "for",
        "forenenst",
        "from",
        "given",
        "in",
        "inside",
        "into",
        "lest",
        "like",
        "modulo",
        "near",
        "next",
        "notwithstanding",
        "of",
        "off",
        "on",
        "onto",
        "out",
        "over",
        "per",
        "plus",
        "pro",
        "qua",
        "sans",
        "since",
        "than",
        "through",
        " thru",
        "throughout",
        "thruout",
        "till",
        "to",
        "toward",
        "towards",
        "under",
        "underneath",
        "until",
        "unto",
        "up",
        "upon",
        "versus",
        "vs.",
        "v.",
        "vs",
        "v",
        "via",
        "vis-à-vis",
        "with",
        "within",
        "without",
        "according to",
        "ahead of",
        "apart from",
        "as for",
        "as of",
        "as per",
        "as regards",
        "aside from",
        "back to",
        "because of",
        "close to",
        "due to",
        "except for",
        "far from",
        "inside of",
        "instead of",
        "near to",
        "next to",
        "on to",
        "out from",
        "out of",
        "outside of",
        "prior to",
        "pursuant to",
        "rather than",
        "regardless of",
        "such as",
        "that of",
        "up to",
        "where as",
        "or",
        "yet",
        "so",
        "for",
        "and",
        "nor",
        "a",
        "an",
        "the",
        "de",
        "d'",
        "von",
        "van",
        "c",
        "ca",
    ]
)