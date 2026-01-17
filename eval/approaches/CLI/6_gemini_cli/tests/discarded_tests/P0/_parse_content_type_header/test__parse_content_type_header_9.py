
import pytest
from requests.utils import _parse_content_type_header

def test__parse_content_type_header_semicolon_in_quotes():
    # This is a bit tricky. The implementation uses split(";") first.
    # So "foo; bar='baz;qux'" will be split into ["foo", " bar='baz", "qux'"]
    # This is a known limitation/behavior of simple split.
    # But let's verify what it does.
    header = 'text/html; title="foo;bar"'
    ct, params = _parse_content_type_header(header)
    assert ct == "text/html"
    # Expected behavior based on code:
    # tokens: ["text/html", ' title="foo', 'bar"']
    # param 1: 'title="foo' -> key="title", val='"foo'
    # param 2: 'bar"' -> key='bar"', val=True
    # This test documents CURRENT behavior, even if arguably incorrect for full RFC parsing.
    assert params.get("title") == '"foo'
    assert params.get('bar"') is True
