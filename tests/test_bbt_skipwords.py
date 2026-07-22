import papis.config
import pytest

from papis_bbt_formatter import BBTFormatter


@pytest.fixture
def formatter():
    return BBTFormatter()


class TestSkipWordsEdgeCases:
    """Tests for SKIP_WORDS fixes: multi-word phrases, special chars, and edge cases."""

    def test_multi_word_phrase_out_of(self, formatter, bbt_defaults):
        """Multi-word phrase 'out of' should be skipped."""
        papis.config.set("title-words", -1, "plugins.bbt")
        doc = {
            "author": "Smith",
            "title": "Out of Africa",
            "year": "1985",
            "author_list": [{"family": "Smith"}],
        }
        result = formatter.format("any", doc)
        assert result == "Smith1985Africa"

    def test_multi_word_phrase_due_to(self, formatter, bbt_defaults):
        """Multi-word phrase 'due to' should be skipped."""
        papis.config.set("title-words", -1, "plugins.bbt")
        doc = {
            "author": "Jones",
            "title": "Failure Due to Error",
            "year": "2010",
            "author_list": [{"family": "Jones"}],
        }
        result = formatter.format("any", doc)
        assert result == "Jones2010FailureError"

    def test_multi_word_phrase_such_as(self, formatter, bbt_defaults):
        """Multi-word phrase 'such as' should be skipped."""
        papis.config.set("title-words", -1, "plugins.bbt")
        doc = {
            "author": "Brown",
            "title": "Animals Such as Dogs",
            "year": "2020",
            "author_list": [{"family": "Brown"}],
        }
        result = formatter.format("any", doc)
        assert result == "Brown2020AnimalsDogs"

    def test_special_char_vs_without_dot(self, formatter, bbt_defaults):
        """'vs' (without dot) should be skipped."""
        papis.config.set("title-words", -1, "plugins.bbt")
        doc = {
            "author": "Lee",
            "title": "Cats vs Dogs",
            "year": "2015",
            "author_list": [{"family": "Lee"}],
        }
        result = formatter.format("any", doc)
        assert result == "Lee2015CatsDogs"

    def test_special_char_v_without_dot(self, formatter, bbt_defaults):
        """'v' (without dot) should be skipped."""
        papis.config.set("title-words", -1, "plugins.bbt")
        doc = {
            "author": "Clark",
            "title": "Roe v Wade",
            "year": "1973",
            "author_list": [{"family": "Clark"}],
        }
        result = formatter.format("any", doc)
        assert result == "Clark1973RoeWade"

    def test_thru_without_leading_space(self, formatter, bbt_defaults):
        """'thru' should be skipped (no leading space)."""
        papis.config.set("title-words", -1, "plugins.bbt")
        doc = {
            "author": "White",
            "title": "Monday Thru Friday",
            "year": "2018",
            "author_list": [{"family": "White"}],
        }
        result = formatter.format("any", doc)
        assert result == "White2018MondayFriday"

    def test_and_is_skipped(self, formatter, bbt_defaults):
        """'and' should be skipped."""
        papis.config.set("title-words", -1, "plugins.bbt")
        doc = {
            "author": "Green",
            "title": "Cats and Dogs",
            "year": "2019",
            "author_list": [{"family": "Green"}],
        }
        result = formatter.format("any", doc)
        assert result == "Green2019CatsDogs"

    def test_visavis_with_special_chars(self, formatter, bbt_defaults):
        """'visavis' (cleaned from 'vis-à-vis') should be skipped."""
        papis.config.set("title-words", -1, "plugins.bbt")
        doc = {
            "author": "Black",
            "title": "Relations Vis-à-vis Power",
            "year": "2021",
            "author_list": [{"family": "Black"}],
        }
        result = formatter.format("any", doc)
        assert result == "Black2021RelationsPower"

    def test_accented_characters_in_title(self, formatter, bbt_defaults):
        """Accented characters should be normalized to ASCII."""
        papis.config.set("title-words", -1, "plugins.bbt")
        doc = {
            "author": "Dupont",
            "title": "Café Culture in Paris",
            "year": "2019",
            "author_list": [{"family": "Dupont"}],
        }
        result = formatter.format("any", doc)
        assert result == "Dupont2019CafeCultureParis"

    def test_naive_with_dieresis(self, formatter, bbt_defaults):
        """'naïve' should normalize to 'naive'."""
        papis.config.set("title-words", -1, "plugins.bbt")
        doc = {
            "author": "Smith",
            "title": "Naïve Approaches to Problem Solving",
            "year": "2020",
            "author_list": [{"family": "Smith"}],
        }
        result = formatter.format("any", doc)
        assert result == "Smith2020NaiveApproachesProblemSolving"

    def test_resume_with_accents(self, formatter, bbt_defaults):
        """'résumé' should normalize to 'resume'."""
        papis.config.set("title-words", -1, "plugins.bbt")
        doc = {
            "author": "Jones",
            "title": "Building a Résumé",
            "year": "2018",
            "author_list": [{"family": "Jones"}],
        }
        result = formatter.format("any", doc)
        assert result == "Jones2018BuildingResume"
