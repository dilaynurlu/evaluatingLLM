You are operating inside a Docker container with a mounted repository at `/workspace`.

## Goal
Generate standalone pytest test files for multiple Requests functions by reading the source code directly from the repository. 
The Python version is 3.11. 
The pytest version is 8.4.2.

## Strategy
From the command line, you will receive a prompt constructed by a specific prompt strategy. 
These strategies will differ between P0-P3. 
BEFORE you do any action, WAIT for this prompt strategy to be provided through the command line.  
For now, `<STRATEGY>` is a placeholder that will later be resolved to one of: P0, P1, P2, or P3.


## Target functions
The target functions are located across `utils.py`, `auth.py`, and `sessions.py` in `requests/src/requests/`:

1. `_basic_auth_str`
2. `_parse_content_type_header`
3. `get_auth_from_url`
4. `HTTPDigestAuth`
5. `prepend_scheme_if_needed`
6. `rebuild_auth`
7. `resolve_redirects`
8. `select_proxy`
9. `should_strip_auth`
10. `unquote_header_value`

## General Rules
- You are allowed to read source files under: `requests/src/requests/`
- You are allowed to create new test files **only** under: `eval/tests/generated_tests/<STRATEGY>/`
- Do NOT modify, delete, or rename any existing files anywhere in the repository
- Do NOT touch `/workspace/venv`
- Do NOT run `pip install` or any dependency installation
- Tests must be deterministic
- Tests must NOT perform real network calls

## Per-Function Instructions
For **each function F** in the target list:

- Locate and read the implementation of `F` in `requests/src/requests/`
- Inspect direct dependencies used by `F` as needed
- Create the directory (if missing): `eval/tests/generated_tests/<STRATEGY>/F/`
- Generate as many standalone pytest test files for `F` as needed to cover meaningful behaviors and edge cases. Name them sequentially using this pattern:
  - `test_F_1.py`
  - `test_F_2.py`
  - `test_F_3.py`
  - …


## Test File Requirements
Each generated test file MUST:

- Import the real function under test (e.g. `from requests.utils import F`)
- Define **exactly one** test function (`def test_...`)
- Test **exactly one** scenario
- Avoid real network calls
- Be runnable independently (no reliance on other generated tests)
- Prefer real Requests objects created via public APIs
- Mock only external side effects when necessary

## Descriptive Context (Not Strict Requirements)
- The human-written test suite for the selected subset of Requests functions contains 72 tests total (≈7 tests per function on average, unevenly distributed)
- When executed in isolation, these human-written tests achieve approximately 62% coverage measured against the entire library
- Human-written tests cover on average ~19 executable lines per test

These values are provided for calibration only.
