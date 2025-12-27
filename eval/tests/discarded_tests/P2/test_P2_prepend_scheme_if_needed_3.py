import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_with_auth_credentials():
    """
    Test that a URL containing authentication credentials (user:pass) without a scheme
    is correctly reconstructed with the new scheme and the credentials preserved.
    This exercises the manual reconstruction of netloc with auth.
    """
    url = "user:password@db.internal"
    new_scheme = "postgresql"
    expected = "postgresql://user:password@db.internal"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == expected


'''
Assertion failed:


expected = "postgresql://user:password@db.internal"
    
        result = prepend_scheme_if_needed(url, new_scheme)
    
>       assert result == expected
E       AssertionError: assert 'user:///password@db.internal' == 'postgresql:/...d@db.internal'
E         
E         - postgresql://user:password@db.internal
E         ? -------------
E         + user:///password@db.internal
E         ?      +++

eval/tests/generated_tests/P2/prepend_scheme_if_needed/test_P2_prepend_scheme_if_needed_3.py:16: AssertionError
'''