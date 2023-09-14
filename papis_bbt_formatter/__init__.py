import re
from typing import Any
import papis.format
import papis.config
import papis.document

import papis.logging

logger = papis.logging.get_logger(__name__)

DEFAULT_TITLE_LENGTH_WORDS = 3
DEFAULT_TITLE_LENGTH_CHARS = -1


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
                else "UNKNOWN"
            )
            title_unfmt = doc["title"] if "title" in doc else "NO TITLE"
            year_unfmt = str(doc["year"]) if "year" in doc else "0000"

            author = re.sub("[^a-z]+", "", author_unfmt.lower())
            year = year_unfmt[-2:]
            title = self.get_title(title_unfmt, fmt)
            return f"{author}{year}{title}"
        else:
            return papis.format.PythonFormater().format(fmt, doc, doc_key, additional)

    def get_title(self, title: str, fmt: str) -> str:
        title = re.sub("[^0-9a-z ]+", "", title.lower())
        title_words = list(
            map(
                str.capitalize,
                filter(lambda word: word and word not in SKIP_WORDS, title.split()),
            )
        )
        wlen = self._title_length_words(fmt)
        clen = self._title_length_chars(fmt)
        wlen = None if wlen == -1 else wlen
        clen = None if clen == -1 else clen
        title = "".join(title_words[:wlen])[:clen]
        return title

    def _title_length_words(self, fmt: str) -> int:
        """Returns the length (in words) the title should be shortened to."""
        if match := re.search(r"\[title-words=(-?\d+)\]", fmt):
            logger.debug(f"Found title length: {match.group(1)} words.")
            return int(match.group(1))
        return DEFAULT_TITLE_LENGTH_WORDS

    def _title_length_chars(self, fmt: str) -> int:
        """Returns the length (in characters) the title should be shortened to."""
        if match := re.search(r"\[title-chars=(-?\d+)\]", fmt):
            logger.debug(f"Found title length: {match.group(1)} chars.")
            return int(match.group(1))
        return DEFAULT_TITLE_LENGTH_CHARS


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
