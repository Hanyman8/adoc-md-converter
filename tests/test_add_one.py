import pytest
from adoc_md_converter import example


data = [(x, x+1) for x in range(10)]


@pytest.mark.parametrize("test_input,expected", data)
def test_add_one(test_input, expected):
    assert example.add_one(test_input) == expected


@pytest.mark.parametrize("test_input,expected", data)
def test_false_add_one(test_input, expected):
    assert example.add_one(test_input) != expected + 1
