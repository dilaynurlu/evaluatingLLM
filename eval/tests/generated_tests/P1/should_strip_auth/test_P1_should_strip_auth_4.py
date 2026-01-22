import pytest
from requests.sessions import Session

def test_should_strip_auth_handles_default_port_equivalence():
    """
    Test that Authorization header is preserved when the port changes between 
    implicit (None) and explicit default (e.g., 80 for HTTP), provided scheme matches.
    """
    session = Session()
    old_url = "http://example.com/foo"
    new_url = "http://example.com:80/foo"
    
    # Logic:
    # Hostnames match.
    # changed_port is True (None != 80).
    # changed_scheme is False.
    # Default port check: 
    #   old port None in (80, None) -> True
    #   new port 80 in (80, None) -> True
    #   -> returns False (don't strip).
    assert session.should_strip_auth(old_url, new_url) is False