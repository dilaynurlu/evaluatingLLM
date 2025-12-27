from requests.utils import _parse_content_type_header

def test_parse_content_type_header_complex_stripping():
    # Refined: Covers mixed quoting and spacing (Critique: Escaped Characters/Quotes)
    # Checks if surrounding single/double quotes are stripped correctly
    header = "multipart/form-data; boundary=' \"abc\" '"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "multipart/form-data"
    # Should strip outer single quotes, preserving inner double quotes
    assert params == {"boundary": '"abc"'}


'''
Assertion failed:

 assert content_type == "multipart/form-data"
        # Should strip outer single quotes, preserving inner double quotes
>       assert params == {"boundary": '"abc"'}
E       assert {'boundary': 'abc'} == {'boundary': '"abc"'}
E         
E         Differing items:
E         {'boundary': 'abc'} != {'boundary': '"abc"'}
E         Use -v to get more diff

eval/tests/generated_tests/P3/_parse_content_type_header/test_P3__parse_content_type_header_8.py:11: AssertionError
'''