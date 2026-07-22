import pytest
import papis.config
from papis_bbt_formatter import BBTFormatter


@pytest.fixture
def formatter():
    return BBTFormatter()


class TestMissingFields:
    def test_no_author_field(self, formatter, bbt_defaults):
        doc = {
            "title": "Test Title",
            "year": "2005",
        }
        result = formatter.format("bbt:", doc)
        assert result == "Unknown2005TestTitle"

    def test_no_author_list_no_author_string(self, formatter, bbt_defaults):
        doc = {
            "title": "Test Title",
            "year": "2005",
        }
        result = formatter.format("bbt:", doc)
        assert result == "Unknown2005TestTitle"

    def test_no_year_field(self, formatter, bbt_defaults):
        doc = {
            "author": "John Smith",
            "title": "Test Title",
        }
        result = formatter.format("bbt:", doc)
        assert result == "John0000TestTitle"

    def test_no_title_field(self, formatter, bbt_defaults):
        doc = {
            "author": "John Smith",
            "year": "2005",
        }
        result = formatter.format("bbt:", doc)
        assert result == "John2005NoTitle"


class TestDateFieldFallback:
    def test_date_field_used_when_year_missing(self, formatter, bbt_defaults):
        doc = {
            "author": "John Smith",
            "title": "Test Title",
            "date": "2005-03-15",
        }
        result = formatter.format("bbt:", doc)
        assert result == "John2005TestTitle"

    def test_year_field_takes_precedence_over_date(self, formatter, bbt_defaults):
        doc = {
            "author": "John Smith",
            "title": "Test Title",
            "year": "2010",
            "date": "2005-03-15",
        }
        result = formatter.format("bbt:", doc)
        assert result == "John2010TestTitle"

    def test_date_field_with_invalid_format(self, formatter, bbt_defaults):
        doc = {
            "author": "John Smith",
            "title": "Test Title",
            "date": "no year here",
        }
        result = formatter.format("bbt:", doc)
        assert result == "John0000TestTitle"


class TestCaseStrUnknownValue:
    def test_case_str_unknown_value_passthrough(self, formatter, bbt_defaults):
        result = formatter._case_str("TestString", "unknown")
        assert result == "TestString"

    def test_case_str_empty_string(self, formatter, bbt_defaults):
        result = formatter._case_str("TestString", "")
        assert result == "TestString"

    def test_case_str_none_like(self, formatter, bbt_defaults):
        result = formatter._case_str("TestString", "none")
        assert result == "TestString"
