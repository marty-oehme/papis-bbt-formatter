import re
from typing import Any
import papis.format
import papis.config
import papis.document

import papis.logging

logger = papis.logging.get_logger(__name__)

DEFAULT_OPTIONS = {
    "plugins.bbt-formatter": {
        "fallback": "python",
        "title-words": 3,
        "title-chars": -1,
    }
}
papis.config.register_default_settings(DEFAULT_OPTIONS)


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
            author = re.sub("[^a-z]+", "", author_unfmt.lower())
            year = self.get_year(int(doc["year"]) if "year" in doc else 0000)
            title = self.get_title(doc["title"] if "title" in doc else "NO TITLE")
            return f"{author}{year}{title}"
        else:
            # TODO find less hacky way of calling another formatter?
            papis.format._FORMATER = None
            fallback_formatter = papis.config.getstring(
                "fallback", "plugins.bbt-formatter"
            )
            formatter = papis.format.get_formater(fallback_formatter).format(
                fmt, doc, doc_key=doc_key, additional=additional
            )
            papis.format._FORMATER = None
            return formatter

    def get_year(self, year: int) -> str:
        """Returns year string according to set year display options.

        Returns either the full 4-digit year or a shortened 2-digit 
        version depending on the plugin year options. """
        if papis.config.getboolean("full-year", "plugins.bbt-formatter"):
            return str(year)
        return str(year)[-2:]

    def get_title(self, title: str) -> str:
        """Returns cleaned and shortened title.

        Removes skip-words, cleans any punctuation and spaces and trims
        the title length to that set in plugin length options."""
        title = re.sub("[^0-9a-z ]+", "", title.lower())
        title_words = list(
            map(
                str.capitalize,
                filter(lambda word: word and word not in SKIP_WORDS, title.split()),
            )
        )
        wlen = papis.config.getint("title-words", "plugins.bbt-formatter")
        clen = papis.config.getint("title-chars", "plugins.bbt-formatter")
        wlen = None if wlen == -1 else wlen
        clen = None if clen == -1 else clen
        title = "".join(title_words[:wlen])[:clen]
        return title


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
