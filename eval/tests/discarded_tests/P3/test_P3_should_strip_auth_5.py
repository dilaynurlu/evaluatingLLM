from requests.sessions import Session

def test_should_strip_auth_non_standard_port_upgrade():
    """
    Test that authentication headers are preserved when upgrading scheme (HTTP -> HTTPS)
    on the same non-standard port.
    Refines the port/scheme logic to ensure upgrades work even when ports are explicit and identical.
    """
    session = Session()
    old_url = "http://example.com:8080/resource"
    new_url = "https://example.com:8080/resource"
    
    result = session.should_strip_auth(old_url, new_url)
    
    assert result is False, "Auth should NOT be stripped when upgrading scheme on the same non-standard port"


'''
Assertion failed


 result = session.should_strip_auth(old_url, new_url)
    
>       assert result is False, "Auth should NOT be stripped when upgrading scheme on the same non-standard port"
E       AssertionError: Auth should NOT be stripped when upgrading scheme on the same non-standard port
E       assert True is False

eval/tests/generated_tests/P3/should_strip_auth/test_P3_should_strip_auth_5.py:15: AssertionError
'''