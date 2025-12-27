from requests.utils import _parse_content_type_header

def test_parse_content_type_header_quoted_param():
    # Refined: Covers quoted values and quoted separators (Critique: Quoted Separators)
    # This tests if the parser correctly handles semicolons inside quotes
    header = 'application/xml; title="foo;bar"'
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/xml"
    # If the parser splits naively on ';', this assertion will fail, highlighting the gap.
    # The correct RFC behavior is to preserve the semicolon within quotes.
    assert params == {"title": "foo;bar"}



'''
Assertion failed:


 # If the parser splits naively on ';', this assertion will fail, highlighting the gap.
        # The correct RFC behavior is to preserve the semicolon within quotes.
>       assert params == {"title": "foo;bar"}
E       assert {'bar"': True, 'title': 'foo'} == {'title': 'foo;bar'}
E         
E         Differing items:
E         {'title': 'foo'} != {'title': 'foo;bar'}
E         Left contains 1 more item:
E         {'bar"': True}
E         Use -v to get more diff

eval/tests/generated_tests/P3/_parse_content_type_header/test_P3__parse_content_type_header_3.py:12: AssertionError
'''