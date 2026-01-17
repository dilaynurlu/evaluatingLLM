import pytest
from requests import Session, Request, Response
from unittest.mock import patch

def test_rebuild_auth_skips_netrc_when_trust_env_is_false():
    with patch("requests.sessions.get_netrc_auth") as mock_netrc:
        # Even if netrc has credentials...
        mock_netrc.return_value = ("user", "pass")
        
        session = Session()
        session.trust_env = False  # ... we do not trust environment
        
        orig_req = Request("GET", "http://start.com")
        orig_prep = orig_req.prepare()
        
        response = Response()
        response.request = orig_prep
        
        new_req = Request("GET", "http://target.com")
        new_prep = new_req.prepare()
        
        session.rebuild_auth(new_prep, response)
        
        # Should not have called netrc logic (or at least not applied it)
        # Because trust_env is false, get_netrc_auth is skipped.
        mock_netrc.assert_not_called()
        
        assert "Authorization" not in new_prep.headers