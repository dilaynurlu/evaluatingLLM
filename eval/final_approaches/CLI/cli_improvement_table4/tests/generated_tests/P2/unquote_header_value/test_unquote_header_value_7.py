from requests.utils import unquote_header_value

def test_unquote_header_value_not_filename_unc_mangled():
    value = '"\\server\\share"'
    # is_filename=False -> replace \\ with \
    # Input inner: \server\share
    # Replace \ -> \ implies \\ -> \\
    assert unquote_header_value(value, is_filename=False) == "\\server\\share"

