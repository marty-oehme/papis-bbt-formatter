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
        assert result == "Harvey2005BriefHistoryNeoliberalism"


class TestTitleWords:
    def test_title_words_3(self, formatter, sample_doc):
        papis.config.set("title-words", 3, "plugins.bbt")
        papis.config.set("title-chars", -1, "plugins.bbt")
        papis.config.set("full-year", True, "plugins.bbt")
        papis.config.set("author-case", "capitalize", "plugins.bbt")
        papis.config.set("title-case", "capitalize", "plugins.bbt")

        result = formatter.format("bbt:", sample_doc)
        assert result == "Harvey2005BriefHistoryNeoliberalism"

    def test_title_words_5(self, formatter, sample_doc_long_title):
        papis.config.set("title-words", 5, "plugins.bbt")
        papis.config.set("title-chars", -1, "plugins.bbt")
        papis.config.set("full-year", True, "plugins.bbt")
        papis.config.set("author-case", "capitalize", "plugins.bbt")
        papis.config.set("title-case", "capitalize", "plugins.bbt")

        result = formatter.format("bbt:", sample_doc_long_title)
        assert result == "Shepherd2022HistoryDelusionsGlassKingSubstitute"

    def test_title_words_infinite(self, formatter, sample_doc_long_title):
        papis.config.set("title-words", -1, "plugins.bbt")
        papis.config.set("title-chars", -1, "plugins.bbt")
        papis.config.set("full-year", True, "plugins.bbt")
        papis.config.set("author-case", "capitalize", "plugins.bbt")
        papis.config.set("title-case", "capitalize", "plugins.bbt")

        result = formatter.format("bbt:", sample_doc_long_title)
        assert (
            result
            == "Shepherd2022HistoryDelusionsGlassKingSubstituteHusbandWalkingCorpse"
        )


class TestTitleChars:
    def test_title_chars_20(self, formatter, sample_doc):
        papis.config.set("title-words", -1, "plugins.bbt")
        papis.config.set("title-chars", 20, "plugins.bbt")
        papis.config.set("full-year", True, "plugins.bbt")
        papis.config.set("author-case", "capitalize", "plugins.bbt")
        papis.config.set("title-case", "capitalize", "plugins.bbt")

        result = formatter.format("bbt:", sample_doc)
        assert result == "Harvey2005BriefHistoryNeoliber"
        assert len(result) - len("Harvey2005") == 20

    def test_title_chars_infinite(self, formatter, sample_doc):
        papis.config.set("title-words", -1, "plugins.bbt")
        papis.config.set("title-chars", -1, "plugins.bbt")
        papis.config.set("full-year", True, "plugins.bbt")
        papis.config.set("author-case", "capitalize", "plugins.bbt")
        papis.config.set("title-case", "capitalize", "plugins.bbt")

        result = formatter.format("bbt:", sample_doc)
        assert result == "Harvey2005BriefHistoryNeoliberalism"


class TestFullYear:
    def test_full_year_true(self, formatter, sample_doc):
        papis.config.set("title-words", 3, "plugins.bbt")
        papis.config.set("title-chars", -1, "plugins.bbt")
        papis.config.set("full-year", True, "plugins.bbt")
        papis.config.set("author-case", "capitalize", "plugins.bbt")
        papis.config.set("title-case", "capitalize", "plugins.bbt")

        result = formatter.format("bbt:", sample_doc)
        assert result == "Harvey2005BriefHistoryNeoliberalism"

    def test_full_year_false(self, formatter, sample_doc_old):
        papis.config.set("title-words", 3, "plugins.bbt")
        papis.config.set("title-chars", -1, "plugins.bbt")
        papis.config.set("full-year", False, "plugins.bbt")
        papis.config.set("author-case", "capitalize", "plugins.bbt")
        papis.config.set("title-case", "capitalize", "plugins.bbt")

        result = formatter.format("bbt:", sample_doc_old)
        assert result == "Fielding51Amelia"

    def test_full_year_threshold_newer(self, formatter, sample_doc):
        """Year >= threshold should return 2-digit version."""
        papis.config.set("title-words", 3, "plugins.bbt")
        papis.config.set("title-chars", -1, "plugins.bbt")
        papis.config.set("full-year", 2000, "plugins.bbt")
        papis.config.set("author-case", "capitalize", "plugins.bbt")
        papis.config.set("title-case", "capitalize", "plugins.bbt")

        result = formatter.format("bbt:", sample_doc)
        assert result == "Harvey05BriefHistoryNeoliberalism"

    def test_full_year_threshold_older(self, formatter, sample_doc_old):
        """Year < threshold should return 4-digit version."""
        papis.config.set("title-words", 3, "plugins.bbt")
        papis.config.set("title-chars", -1, "plugins.bbt")
        papis.config.set("full-year", 1900, "plugins.bbt")
        papis.config.set("author-case", "capitalize", "plugins.bbt")
        papis.config.set("title-case", "capitalize", "plugins.bbt")

        result = formatter.format("bbt:", sample_doc_old)
        assert result == "Fielding1751Amelia"

    def test_full_year_threshold_exact(self, formatter, sample_doc):
        """Year == threshold should return 2-digit version (>=)."""
        papis.config.set("title-words", 3, "plugins.bbt")
        papis.config.set("title-chars", -1, "plugins.bbt")
        papis.config.set("full-year", 2005, "plugins.bbt")
        papis.config.set("author-case", "capitalize", "plugins.bbt")
        papis.config.set("title-case", "capitalize", "plugins.bbt")

        result = formatter.format("bbt:", sample_doc)
        assert result == "Harvey05BriefHistoryNeoliberalism"


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
        assert "BriefHistoryNeoliberalism" in result

    def test_title_case_lower(self, formatter, sample_doc):
        papis.config.set("title-words", 3, "plugins.bbt")
        papis.config.set("title-chars", -1, "plugins.bbt")
        papis.config.set("full-year", True, "plugins.bbt")
        papis.config.set("author-case", "capitalize", "plugins.bbt")
        papis.config.set("title-case", "lower", "plugins.bbt")

        result = formatter.format("bbt:", sample_doc)
        assert "briefhistoryneoliberalism" in result

    def test_title_case_upper(self, formatter, sample_doc):
        papis.config.set("title-words", 3, "plugins.bbt")
        papis.config.set("title-chars", -1, "plugins.bbt")
        papis.config.set("full-year", True, "plugins.bbt")
        papis.config.set("author-case", "capitalize", "plugins.bbt")
        papis.config.set("title-case", "upper", "plugins.bbt")

        result = formatter.format("bbt:", sample_doc)
        assert "BRIEFHISTORYNEOLIBERALISM" in result


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
        assert result == "Harvey2005BriefHistoryNeoliberalism"

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

        assert result == "Harvey2005BriefHistoryNeoliberalism"
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
        assert result == "Harvey2005BriefHistoryNeoliberalism"


class TestSkipWordsEdgeCases:
    """Tests for SKIP_WORDS fixes: multi-word phrases, special chars, and edge cases."""

    def _set_defaults(self):
        papis.config.set("title-words", -1, "plugins.bbt")
        papis.config.set("title-chars", -1, "plugins.bbt")
        papis.config.set("full-year", True, "plugins.bbt")
        papis.config.set("author-case", "capitalize", "plugins.bbt")
        papis.config.set("title-case", "capitalize", "plugins.bbt")

    def test_multi_word_phrase_out_of(self, formatter):
        """Multi-word phrase 'out of' should be skipped."""
        self._set_defaults()
        doc = {
            "author": "Smith",
            "title": "Out of Africa",
            "year": "1985",
            "author_list": [{"family": "Smith"}],
        }
        result = formatter.format("any", doc)
        assert result == "Smith1985Africa"

    def test_multi_word_phrase_due_to(self, formatter):
        """Multi-word phrase 'due to' should be skipped."""
        self._set_defaults()
        doc = {
            "author": "Jones",
            "title": "Failure Due to Error",
            "year": "2010",
            "author_list": [{"family": "Jones"}],
        }
        result = formatter.format("any", doc)
        assert result == "Jones2010FailureError"

    def test_multi_word_phrase_such_as(self, formatter):
        """Multi-word phrase 'such as' should be skipped."""
        self._set_defaults()
        doc = {
            "author": "Brown",
            "title": "Animals Such as Dogs",
            "year": "2020",
            "author_list": [{"family": "Brown"}],
        }
        result = formatter.format("any", doc)
        assert result == "Brown2020AnimalsDogs"

    def test_special_char_vs_without_dot(self, formatter):
        """'vs' (without dot) should be skipped."""
        self._set_defaults()
        doc = {
            "author": "Lee",
            "title": "Cats vs Dogs",
            "year": "2015",
            "author_list": [{"family": "Lee"}],
        }
        result = formatter.format("any", doc)
        assert result == "Lee2015CatsDogs"

    def test_special_char_v_without_dot(self, formatter):
        """'v' (without dot) should be skipped."""
        self._set_defaults()
        doc = {
            "author": "Clark",
            "title": "Roe v Wade",
            "year": "1973",
            "author_list": [{"family": "Clark"}],
        }
        result = formatter.format("any", doc)
        assert result == "Clark1973RoeWade"

    def test_thru_without_leading_space(self, formatter):
        """'thru' should be skipped (no leading space)."""
        self._set_defaults()
        doc = {
            "author": "White",
            "title": "Monday Thru Friday",
            "year": "2018",
            "author_list": [{"family": "White"}],
        }
        result = formatter.format("any", doc)
        assert result == "White2018MondayFriday"

    def test_and_is_skipped(self, formatter):
        """'and' should be skipped."""
        self._set_defaults()
        doc = {
            "author": "Green",
            "title": "Cats and Dogs",
            "year": "2019",
            "author_list": [{"family": "Green"}],
        }
        result = formatter.format("any", doc)
        assert result == "Green2019CatsDogs"

    def test_visavis_without_special_chars(self, formatter):
        """'visavis' (cleaned from 'vis-à-vis') should be skipped."""
        self._set_defaults()
        doc = {
            "author": "Black",
            "title": "Relations Visavis Power",
            "year": "2021",
            "author_list": [{"family": "Black"}],
        }
        result = formatter.format("any", doc)
        assert result == "Black2021RelationsPower"
