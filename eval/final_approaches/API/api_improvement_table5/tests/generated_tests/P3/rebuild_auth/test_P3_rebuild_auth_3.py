import pytest
from requests import Session, PreparedRequest, Response

def test_rebuild_auth_ignores_netrc_when_trust_env_is_false(tmp_path, monkeypatch):
    """
    Test that rebuild_auth does NOT apply .netrc credentials 
    if the session's trust_env is False.
    """
    # Setup .netrc (should be ignored)
    netrc_content = "machine example.com login myuser password mypass"
    netrc_file = tmp_path / ".netrc"
    netrc_file.write_text(netrc_content, encoding="utf-8")
    monkeypatch.setenv("NETRC", str(netrc_file))

    session = Session()
    session.trust_env = False  # Explicitly disable

    p_req = PreparedRequest()
    p_req.prepare(method="GET", url="http://example.com/resource")

    response = Response()
    response.request = PreparedRequest()
    response.request.url = "http://origin.com"

    # Execute
    session.rebuild_auth(p_req, response)

    # Assert no Authorization header added
    assert "Authorization" not in p_req.headers