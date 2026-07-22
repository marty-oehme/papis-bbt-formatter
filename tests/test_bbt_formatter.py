import papis.config
import papis.document
import pytest

from papis_bbt_formatter import BBTFormatter


@pytest.fixture
def formatter():
    return BBTFormatter()


@pytest.fixture
def sample_doc():
    return {
        "author": "David Harvey",
        "title": "A Brief History of Neoliberalism",
        "year": "2005",
        "author_list": [{"family": "Harvey", "given": "David"}],
    }


@pytest.fixture
def sample_doc_long_title():
    return {
        "author": "Victoria Shepherd",
        "title": "A History of Delusions: The Glass King, a Substitute Husband and a Walking Corpse",
        "year": "2022",
        "author_list": [{"family": "Shepherd", "given": "Victoria"}],
    }


@pytest.fixture
def sample_doc_old():
    return {
        "author": "Henry Fielding",
        "title": "Amelia",
        "year": "1751",
        "author_list": [{"family": "Fielding", "given": "Henry"}],
    }


class TestDefaultOptions:
    def test_default_formatting(self, formatter, sample_doc):
        papis.config.set("default-formatter", "python", "plugins.bbt")
        papis.config.set("title-words", 3, "plugins.bbt")
        papis.config.set("title-chars", -1, "plugins.bbt")
        papis.config.set("full-year", True, "plugins.bbt")
        papis.config.set("author-case", "capitalize", "plugins.bbt")
        papis.config.set("title-case", "capitalize", "plugins.bbt")

        result = formatter.format("bbt:", sample_doc)
        assert result == "Harvey2005ABriefHistory"


class TestTitleWords:
    def test_title_words_3(self, formatter, sample_doc):
        papis.config.set("title-words", 3, "plugins.bbt")
        papis.config.set("title-chars", -1, "plugins.bbt")
        papis.config.set("full-year", True, "plugins.bbt")
        papis.config.set("author-case", "capitalize", "plugins.bbt")
        papis.config.set("title-case", "capitalize", "plugins.bbt")

        result = formatter.format("bbt:", sample_doc)
        assert result == "Harvey2005ABriefHistory"

    def test_title_words_5(self, formatter, sample_doc_long_title):
        papis.config.set("title-words", 5, "plugins.bbt")
        papis.config.set("title-chars", -1, "plugins.bbt")
        papis.config.set("full-year", True, "plugins.bbt")
        papis.config.set("author-case", "capitalize", "plugins.bbt")
        papis.config.set("title-case", "capitalize", "plugins.bbt")

        result = formatter.format("bbt:", sample_doc_long_title)
        assert result == "Shepherd2022AHistoryDelusionsTheGlass"

    def test_title_words_infinite(self, formatter, sample_doc_long_title):
        papis.config.set("title-words", -1, "plugins.bbt")
        papis.config.set("title-chars", -1, "plugins.bbt")
        papis.config.set("full-year", True, "plugins.bbt")
        papis.config.set("author-case", "capitalize", "plugins.bbt")
        papis.config.set("title-case", "capitalize", "plugins.bbt")

        result = formatter.format("bbt:", sample_doc_long_title)
        assert (
            result
            == "Shepherd2022AHistoryDelusionsTheGlassKingSubstituteHusbandWalkingCorpse"
        )


class TestTitleChars:
    def test_title_chars_20(self, formatter, sample_doc):
        papis.config.set("title-words", -1, "plugins.bbt")
        papis.config.set("title-chars", 20, "plugins.bbt")
        papis.config.set("full-year", True, "plugins.bbt")
        papis.config.set("author-case", "capitalize", "plugins.bbt")
        papis.config.set("title-case", "capitalize", "plugins.bbt")

        result = formatter.format("bbt:", sample_doc)
        assert result == "Harvey2005ABriefHistoryNeolibe"
        assert len(result) - len("Harvey2005") == 20

    def test_title_chars_infinite(self, formatter, sample_doc):
        papis.config.set("title-words", -1, "plugins.bbt")
        papis.config.set("title-chars", -1, "plugins.bbt")
        papis.config.set("full-year", True, "plugins.bbt")
        papis.config.set("author-case", "capitalize", "plugins.bbt")
        papis.config.set("title-case", "capitalize", "plugins.bbt")

        result = formatter.format("bbt:", sample_doc)
        assert result == "Harvey2005ABriefHistoryNeoliberalism"


class TestFullYear:
    def test_full_year_true(self, formatter, sample_doc):
        papis.config.set("title-words", 3, "plugins.bbt")
        papis.config.set("title-chars", -1, "plugins.bbt")
        papis.config.set("full-year", True, "plugins.bbt")
        papis.config.set("author-case", "capitalize", "plugins.bbt")
        papis.config.set("title-case", "capitalize", "plugins.bbt")

        result = formatter.format("bbt:", sample_doc)
        assert result == "Harvey2005ABriefHistory"

    def test_full_year_false(self, formatter, sample_doc_old):
        papis.config.set("title-words", 3, "plugins.bbt")
        papis.config.set("title-chars", -1, "plugins.bbt")
        papis.config.set("full-year", False, "plugins.bbt")
        papis.config.set("author-case", "capitalize", "plugins.bbt")
        papis.config.set("title-case", "capitalize", "plugins.bbt")

        result = formatter.format("bbt:", sample_doc_old)
        assert result == "Fielding51Amelia"


class TestCapitalization:
    def test_author_case_capitalize(self, formatter, sample_doc):
        papis.config.set("title-words", 3, "plugins.bbt")
        papis.config.set("title-chars", -1, "plugins.bbt")
        papis.config.set("full-year", True, "plugins.bbt")
        papis.config.set("author-case", "capitalize", "plugins.bbt")
        papis.config.set("title-case", "capitalize", "plugins.bbt")

        result = formatter.format("bbt:", sample_doc)
        assert result.startswith("Harvey")

    def test_author_case_lower(self, formatter, sample_doc):
        papis.config.set("title-words", 3, "plugins.bbt")
        papis.config.set("title-chars", -1, "plugins.bbt")
        papis.config.set("full-year", True, "plugins.bbt")
        papis.config.set("author-case", "lower", "plugins.bbt")
        papis.config.set("title-case", "capitalize", "plugins.bbt")

        result = formatter.format("bbt:", sample_doc)
        assert result.startswith("harvey")

    def test_author_case_upper(self, formatter, sample_doc):
        papis.config.set("title-words", 3, "plugins.bbt")
        papis.config.set("title-chars", -1, "plugins.bbt")
        papis.config.set("full-year", True, "plugins.bbt")
        papis.config.set("author-case", "upper", "plugins.bbt")
        papis.config.set("title-case", "capitalize", "plugins.bbt")

        result = formatter.format("bbt:", sample_doc)
        assert result.startswith("HARVEY")

    def test_title_case_capitalize(self, formatter, sample_doc):
        papis.config.set("title-words", 3, "plugins.bbt")
        papis.config.set("title-chars", -1, "plugins.bbt")
        papis.config.set("full-year", True, "plugins.bbt")
        papis.config.set("author-case", "capitalize", "plugins.bbt")
        papis.config.set("title-case", "capitalize", "plugins.bbt")

        result = formatter.format("bbt:", sample_doc)
        assert "ABriefHistory" in result

    def test_title_case_lower(self, formatter, sample_doc):
        papis.config.set("title-words", 3, "plugins.bbt")
        papis.config.set("title-chars", -1, "plugins.bbt")
        papis.config.set("full-year", True, "plugins.bbt")
        papis.config.set("author-case", "capitalize", "plugins.bbt")
        papis.config.set("title-case", "lower", "plugins.bbt")

        result = formatter.format("bbt:", sample_doc)
        assert "abriefhistory" in result

    def test_title_case_upper(self, formatter, sample_doc):
        papis.config.set("title-words", 3, "plugins.bbt")
        papis.config.set("title-chars", -1, "plugins.bbt")
        papis.config.set("full-year", True, "plugins.bbt")
        papis.config.set("author-case", "capitalize", "plugins.bbt")
        papis.config.set("title-case", "upper", "plugins.bbt")

        result = formatter.format("bbt:", sample_doc)
        assert "ABRIEFHISTORY" in result


class TestRefFormatRequirement:
    """Regression tests to ensure BBT formatting works regardless of ref-format value."""

    def test_formatting_without_ref_format_set(self, formatter, sample_doc):
        """BBT formatting should work when no ref-format is configured."""
        papis.config.set("title-words", 3, "plugins.bbt")
        papis.config.set("title-chars", -1, "plugins.bbt")
        papis.config.set("full-year", True, "plugins.bbt")
        papis.config.set("author-case", "capitalize", "plugins.bbt")
        papis.config.set("title-case", "capitalize", "plugins.bbt")

        result = formatter.format("any-format-string", sample_doc)
        assert result == "Harvey2005ABriefHistory"

    def test_formatting_with_bbt_prefix(self, formatter, sample_doc, caplog):
        """BBT formatting should work when ref-format is set to bbt: (backward compat)."""
        import logging

        papis.config.set("title-words", 3, "plugins.bbt")
        papis.config.set("title-chars", -1, "plugins.bbt")
        papis.config.set("full-year", True, "plugins.bbt")
        papis.config.set("author-case", "capitalize", "plugins.bbt")
        papis.config.set("title-case", "capitalize", "plugins.bbt")

        with caplog.at_level(logging.WARNING):
            result = formatter.format("bbt:", sample_doc)

        assert result == "Harvey2005ABriefHistory"
        assert "ref-format = bbt:" in caplog.text
        assert "deprecated" in caplog.text

    def test_formatting_with_arbitrary_format_string(self, formatter, sample_doc):
        """BBT formatting should work with any arbitrary format string."""
        papis.config.set("title-words", 3, "plugins.bbt")
        papis.config.set("title-chars", -1, "plugins.bbt")
        papis.config.set("full-year", True, "plugins.bbt")
        papis.config.set("author-case", "capitalize", "plugins.bbt")
        papis.config.set("title-case", "capitalize", "plugins.bbt")

        result = formatter.format("python:{doc[author]}", sample_doc)
        assert result == "Harvey2005ABriefHistory"
