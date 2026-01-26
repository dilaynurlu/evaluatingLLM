import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from requests.structures import CaseInsensitiveDict

def test_rebuild_auth_ignores_netrc_when_untrusted():
    """
    Test that rebuild_auth does NOT query or apply .netrc credentials 
    if trust_env is False, even if credentials would otherwise exist.
    """
    session = Session()
    session.trust_env = False
    
    new_request = PreparedRequest()
    new_request.url = "http://api.example.com/data"
    new_request.headers = CaseInsensitiveDict({})
    
    response = Response()
    old_request = PreparedRequest()
    old_request.url = "http://api.example.com/login"
    response.request = old_request
    
    with patch("requests.sessions.get_netrc_auth") as mock_netrc:
        # Configure mock to return credentials if called (though it shouldn't matter)
        mock_netrc.return_value = ("user", "pass")
        
        session.rebuild_auth(new_request, response)
        
        # If the implementation strictly checks trust_env before calling, 
        # mock might not be called. Even if called, result should be ignored.
        # But requests.sessions code: `new_auth = get_netrc_auth(url) if self.trust_env else None`
        # implies it won't be called.
        
        assert "Authorization" not in new_request.headers