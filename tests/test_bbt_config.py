import papis.config
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
    def test_default_formatting(self, formatter, sample_doc, bbt_defaults):
        result = formatter.format("bbt:", sample_doc)
        assert result == "Harvey2005BriefHistoryNeoliberalism"


class TestTitleWords:
    def test_title_words_3(self, formatter, sample_doc, bbt_defaults):
        result = formatter.format("bbt:", sample_doc)
        assert result == "Harvey2005BriefHistoryNeoliberalism"

    def test_title_words_5(self, formatter, sample_doc_long_title, bbt_defaults):
        papis.config.set("title-words", 5, "plugins.bbt")
        result = formatter.format("bbt:", sample_doc_long_title)
        assert result == "Shepherd2022HistoryDelusionsGlassKingSubstitute"

    def test_title_words_infinite(self, formatter, sample_doc_long_title, bbt_defaults):
        papis.config.set("title-words", -1, "plugins.bbt")
        result = formatter.format("bbt:", sample_doc_long_title)
        assert (
            result
            == "Shepherd2022HistoryDelusionsGlassKingSubstituteHusbandWalkingCorpse"
        )


class TestTitleChars:
    def test_title_chars_20(self, formatter, sample_doc, bbt_defaults):
        papis.config.set("title-words", -1, "plugins.bbt")
        papis.config.set("title-chars", 20, "plugins.bbt")
        result = formatter.format("bbt:", sample_doc)
        assert result == "Harvey2005BriefHistoryNeoliber"
        assert len(result) - len("Harvey2005") == 20

    def test_title_chars_infinite(self, formatter, sample_doc, bbt_defaults):
        papis.config.set("title-words", -1, "plugins.bbt")
        result = formatter.format("bbt:", sample_doc)
        assert result == "Harvey2005BriefHistoryNeoliberalism"


class TestCapitalization:
    def test_author_case_capitalize(self, formatter, sample_doc, bbt_defaults):
        result = formatter.format("bbt:", sample_doc)
        assert result.startswith("Harvey")

    def test_author_case_lower(self, formatter, sample_doc, bbt_defaults):
        papis.config.set("author-case", "lower", "plugins.bbt")
        result = formatter.format("bbt:", sample_doc)
        assert result.startswith("harvey")

    def test_author_case_upper(self, formatter, sample_doc, bbt_defaults):
        papis.config.set("author-case", "upper", "plugins.bbt")
        result = formatter.format("bbt:", sample_doc)
        assert result.startswith("HARVEY")

    def test_title_case_capitalize(self, formatter, sample_doc, bbt_defaults):
        result = formatter.format("bbt:", sample_doc)
        assert "BriefHistoryNeoliberalism" in result

    def test_title_case_lower(self, formatter, sample_doc, bbt_defaults):
        papis.config.set("title-case", "lower", "plugins.bbt")
        result = formatter.format("bbt:", sample_doc)
        assert "briefhistoryneoliberalism" in result

    def test_title_case_upper(self, formatter, sample_doc, bbt_defaults):
        papis.config.set("title-case", "upper", "plugins.bbt")
        result = formatter.format("bbt:", sample_doc)
        assert "BRIEFHISTORYNEOLIBERALISM" in result


class TestRefFormatRequirement:
    """Regression tests to ensure BBT formatting works regardless of ref-format value."""

    def test_formatting_without_ref_format_set(self, formatter, sample_doc, bbt_defaults):
        """BBT formatting should work when no ref-format is configured."""
        result = formatter.format("any-format-string", sample_doc)
        assert result == "Harvey2005BriefHistoryNeoliberalism"

    def test_formatting_with_bbt_prefix(self, formatter, sample_doc, bbt_defaults, caplog):
        """BBT formatting should work when ref-format is set to bbt: (backward compat)."""
        import logging

        with caplog.at_level(logging.WARNING):
            result = formatter.format("bbt:", sample_doc)

        assert result == "Harvey2005BriefHistoryNeoliberalism"
        assert "ref-format = bbt:" in caplog.text
        assert "deprecated" in caplog.text

    def test_formatting_with_arbitrary_format_string(self, formatter, sample_doc, bbt_defaults):
        """BBT formatting should work with any arbitrary format string."""
        result = formatter.format("python:{doc[author]}", sample_doc)
        assert result == "Harvey2005BriefHistoryNeoliberalism"
