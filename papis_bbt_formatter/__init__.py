import re
import sys
import unicodedata
from typing import Any, ClassVar

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

import papis.config
import papis.document
import papis.format
import papis.logging

logger = papis.logging.get_logger(__name__)

OPTIONS_SECTION = "plugins.bbt"
DEFAULT_OPTIONS = {
    OPTIONS_SECTION: {
        "title-words": 3,
        "title-chars": -1,
        "full-year": True,
        "author-case": "capitalize",
        "title-case": "capitalize",
    }
}
papis.config.register_default_settings(DEFAULT_OPTIONS)


class BBTFormatter(papis.format.Formatter):
    """Provides zotero better-bibtex-like keys."""

    name: ClassVar[str] = "bbt"

    @override
    def format(
        self,
        fmt: str,
        doc: papis.document.DocumentLike,
        doc_key: str = "",
        additional: dict[str, Any] | None = None,  # pyright: ignore[reportExplicitAny]
        default: str | None = None,
    ) -> str:
        if fmt.startswith("bbt:"):
            logger.warning("""The 'ref-format = bbt:' setting is deprecated and no longer required.
You can safely remove it from your config.
Setting 'formatter = bbt' is sufficient to enable BBT key generation.""")
        return self.format_with_bbt(doc)

    def format_with_bbt(self, doc: papis.document.DocumentLike) -> str:
        author = self.get_author(
            doc["author_list"][0]["family"]
            if "author_list" in doc
            else str(doc["author"]).split(maxsplit=1)[0]  # pyright: ignore[reportAny]
            if "author" in doc
            else "UNKNOWN"
        )
        year = self.get_year(
            doc["year"] if "year" in doc else doc["date"] if "date" in doc else ""
        )
        title = self.get_title(doc["title"] if "title" in doc else "NO TITLE")
        return f"{author}{year}{title}"

    def get_author(self, author: str) -> str:
        author = re.sub("[^a-zA-Z]+", "", author)
        author_case = papis.config.getstring("author-case", OPTIONS_SECTION)
        return self._case_str(author, author_case)

    def get_year(self, date: str) -> str:
        """Returns year string according to set year display options.

        Returns either the full 4-digit year or a shortened 2-digit
        version depending on the plugin year options.
        
        Supports three modes:
        - True: always return 4-digit year
        - False: always return 2-digit year
        - int threshold: return 2-digit year if year >= threshold, else 4-digit
        """
        date_match = re.search(r"\d{4}", date)
        if not date_match:
            return "0000"
        date_str = date_match[0]
        year = int(date_str)
        
        full_year_config = papis.config.get("full-year", OPTIONS_SECTION)
        
        if isinstance(full_year_config, bool):
            return date_str if full_year_config else date_str[-2:]
        
        if isinstance(full_year_config, str):
            if full_year_config.lower() == "true":
                return date_str
            elif full_year_config.lower() == "false":
                return date_str[-2:]
            else:
                try:
                    threshold = int(full_year_config)
                    return date_str[-2:] if year >= threshold else date_str
                except ValueError:
                    return date_str
        
        if isinstance(full_year_config, int):
            return date_str[-2:] if year >= full_year_config else date_str
        
        return date_str

    def get_title(self, title: str) -> str:
        """Returns cleaned and shortened title.

        Removes skip-words, cleans any punctuation and spaces and trims
        the title length to that set in plugin length options."""
        title = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
        title = re.sub("[^0-9a-zA-Z ]+", "", title)
        for phrase in SKIP_PHRASES:
            title = re.sub(r"\b" + re.escape(phrase) + r"\b", " ", title, flags=re.IGNORECASE)
        title_case = papis.config.getstring("title-case", OPTIONS_SECTION)
        title_words = [
            self._case_str(word, title_case)
            for word in title.split()
            if word.lower() not in SKIP_WORDS
        ]

        wlen = papis.config.getint("title-words", OPTIONS_SECTION)
        clen = papis.config.getint("title-chars", OPTIONS_SECTION)
        wlen = None if wlen == -1 else wlen
        clen = None if clen == -1 else clen

        title = "".join(title_words[:wlen])[:clen]
        return title

    def _case_str(self, s: str, case: str) -> str:
        if case == "lower":
            return s.lower()
        elif case == "capitalize":
            return s.capitalize()
        elif case == "upper":
            return s.upper()
        return s


SKIP_PHRASES = {
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
}

SKIP_WORDS = {
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
    "and",
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
    "c",
    "ca",
    "circa",
    "d",
    "de",
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
    "nor",
    "notwithstanding",
    "of",
    "off",
    "on",
    "onto",
    "or",
    "out",
    "over",
    "per",
    "plus",
    "pro",
    "qua",
    "sans",
    "since",
    "so",
    "than",
    "thru",
    "through",
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
    "v",
    "versus",
    "via",
    "visavis",
    "von",
    "vs",
    "with",
    "within",
    "without",
    "yet",
    "a",
    "an",
    "the",
    "van",
}
