Static analysis for `_parse_content_type_header`:

- **Conditional Branch (Splitting):** `header.split(";")` determines if there are parameters to process.
    - *Trigger:* Header with no semicolons (e.g., `"text/plain"`) vs header with semicolons.
- **Loop (Parameters):** `for param in params` iterates over the split tokens (excluding the first).
    - *Trigger:* Header with multiple semicolons (e.g., `"a;b;c"`).
- **Conditional Branch (Empty Param):** `if param:` checks if the stripped parameter segment is non-empty.
    - *Trigger:* Consecutive semicolons in header (e.g., `"text/plain;;charset=utf-8"`) creates an empty string token.
- **Conditional Branch (Parsing Key/Value):** `if index_of_equals != -1:` checks if an `=` sign exists in the parameter.
    - *Trigger (True):* Standard parameter (e.g., `"charset=utf-8"`).
    - *Trigger (False):* Flag parameter (e.g., `"text/plain; secure"`), results in `value=True`.
- **String Manipulation (Stripping):** Keys and values are stripped of characters `"' ` (space, single quote, double quote).
    - *Trigger:* Parameters with quoted values or padding spaces (e.g., `; type="text" `).
- **Dictionary Assignment:** `params_dict[key.lower()] = value` implies last-write-wins for duplicate case-insensitive keys.
    - *Trigger:* Header with duplicate keys (e.g., `; a=1; A=2`).