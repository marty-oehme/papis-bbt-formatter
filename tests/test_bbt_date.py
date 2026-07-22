import pytest
import papis.config
from papis_bbt_formatter import BBTFormatter


@pytest.fixture
def formatter():
    return BBTFormatter()


class TestGetYearExtraction:
    def test_year_only(self, formatter):
        papis.config.set("full-year", True, "plugins.bbt")
        assert formatter.get_year("2005") == "2005"

    def test_full_date_iso(self, formatter):
        papis.config.set("full-year", True, "plugins.bbt")
        assert formatter.get_year("2005-03-15") == "2005"

    def test_full_date_with_time(self, formatter):
        papis.config.set("full-year", True, "plugins.bbt")
        assert formatter.get_year("2005-03-15T10:30:00") == "2005"

    def test_year_embedded_in_text(self, formatter):
        papis.config.set("full-year", True, "plugins.bbt")
        assert formatter.get_year("Published in 1997 by MIT Press") == "1997"

    def test_empty_string(self, formatter):
        papis.config.set("full-year", True, "plugins.bbt")
        assert formatter.get_year("") == "0000"

    def test_no_digits(self, formatter):
        papis.config.set("full-year", True, "plugins.bbt")
        assert formatter.get_year("no year here") == "0000"

    def test_less_than_four_digits(self, formatter):
        papis.config.set("full-year", True, "plugins.bbt")
        assert formatter.get_year("99") == "0000"


class TestFullYearBool:
    def test_true_returns_four_digit(self, formatter):
        papis.config.set("full-year", True, "plugins.bbt")
        assert formatter.get_year("2005") == "2005"

    def test_false_returns_two_digit(self, formatter):
        papis.config.set("full-year", False, "plugins.bbt")
        assert formatter.get_year("2005") == "05"

    def test_false_year_2000(self, formatter):
        papis.config.set("full-year", False, "plugins.bbt")
        assert formatter.get_year("2000") == "00"

    def test_false_year_1999(self, formatter):
        papis.config.set("full-year", False, "plugins.bbt")
        assert formatter.get_year("1999") == "99"


class TestFullYearString:
    def test_string_true(self, formatter):
        papis.config.set("full-year", "true", "plugins.bbt")
        assert formatter.get_year("2005") == "2005"

    def test_string_false(self, formatter):
        papis.config.set("full-year", "false", "plugins.bbt")
        assert formatter.get_year("2005") == "05"

    def test_string_True_capitalized(self, formatter):
        papis.config.set("full-year", "True", "plugins.bbt")
        assert formatter.get_year("2005") == "2005"

    def test_string_False_capitalized(self, formatter):
        papis.config.set("full-year", "False", "plugins.bbt")
        assert formatter.get_year("2005") == "05"


class TestFullYearThreshold:
    def test_int_threshold_newer(self, formatter):
        papis.config.set("full-year", 2000, "plugins.bbt")
        assert formatter.get_year("2005") == "05"

    def test_int_threshold_older(self, formatter):
        papis.config.set("full-year", 1900, "plugins.bbt")
        assert formatter.get_year("1751") == "1751"

    def test_int_threshold_exact(self, formatter):
        papis.config.set("full-year", 2005, "plugins.bbt")
        assert formatter.get_year("2005") == "05"

    def test_int_threshold_one_below(self, formatter):
        papis.config.set("full-year", 1900, "plugins.bbt")
        assert formatter.get_year("1899") == "1899"

    def test_string_threshold_newer(self, formatter):
        papis.config.set("full-year", "1900", "plugins.bbt")
        assert formatter.get_year("2005") == "05"

    def test_string_threshold_older(self, formatter):
        papis.config.set("full-year", "1900", "plugins.bbt")
        assert formatter.get_year("1751") == "1751"

    def test_string_threshold_exact(self, formatter):
        papis.config.set("full-year", "2005", "plugins.bbt")
        assert formatter.get_year("2005") == "05"

    def test_invalid_string_falls_back_to_full(self, formatter):
        papis.config.set("full-year", "garbage", "plugins.bbt")
        assert formatter.get_year("2005") == "2005"
