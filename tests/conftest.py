import papis.config
import pytest


@pytest.fixture
def bbt_defaults():
    papis.config.set("title-words", 3, "plugins.bbt")
    papis.config.set("title-chars", -1, "plugins.bbt")
    papis.config.set("full-year", True, "plugins.bbt")
    papis.config.set("author-case", "capitalize", "plugins.bbt")
    papis.config.set("title-case", "capitalize", "plugins.bbt")
