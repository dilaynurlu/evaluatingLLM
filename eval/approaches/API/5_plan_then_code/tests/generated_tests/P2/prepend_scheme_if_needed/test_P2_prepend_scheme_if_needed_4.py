from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_path_swap_logic():
    """
    Test the specific logic branch where a URL parsed with no netloc has its path
    swapped to netloc. This typically happens for paths starting with '/', which
    prevents implicit 'http://' prefixing during parsing.
    """
    # An input starting with '/' typically parses as path='/var/run', netloc=None.
    # The function detects missing netloc and swaps path -> netloc.
    # Resulting netloc is '/var/run'. urlunparse formats this as 'scheme:///var/run'.
    url = "/var/run/socket"
    new_scheme = "http"
    expected = "http:///var/run/socket"
    
    assert prepend_scheme_if_needed(url, new_scheme) == expected