# evaluatingLLM

A research toolkit to generate, execute, and evaluate LLM-generated
unit tests against the [`requests`](https://github.com/psf/requests)
Python library.

This project supports: 
* **Generating** unit tests using an LLM (Gemini).
* Evaluating **syntactic, execution, and assertion correctness**
of generated tests.
* Measuring **line and branch coverage** against the
local `requests` source code.
* Measuring the quality of generated tests regarding **security** aspects.
* Comparing LLM-generated tests against existing human-written tests.

> **Important design choice**:\
> The `requests` library itself is not vendored in this repository.\
> You must provide a local clone and install it in editable mode.

---
<br>



# Installation & Setup (mainly macOS and Linux based)

## 1. Clone this repository

``` bash
git clone <repo-url>
cd evaluatingLLM
```
<br>



## 2. Create and activate a virtual environment

``` bash
python3 -m venv venv
source venv/bin/activate
```

Verify:

``` bash
which python
```

Output should point to:

    .../evaluatingLLM/venv/bin/python

<br>


## 3. Install required Python packages

Install the core tooling used by the evaluation framework:

``` bash
pip install --upgrade pip
pip install pytest coverage bandit ruff google-genai
```

Verify:

``` bash
pip list
```

You should see (at least): - pytest - coverage - bandit - google-genai

<br>



## 4. Requests Library Setup (Required)



Coverage and test execution **must run against the local Requests
source**, not the published PyPI package. This allows:
* Accurate line & branch coverage
* Inspection of executed functions
* Fair comparison between human and LLM-generated tests


### Recommended: Editable install of Requests

Clone Requests **inside or next to** this project:

``` bash
git clone https://github.com/psf/requests.git
cd requests
pip install -e .
```

This creates an **editable install**, meaning:

``` python
import requests
```

will resolve to your local clone.

Verify: Your `pip list` shows editable installs and locations; confirm `requests` points to your local clone.

For coverage to measure your local copy of `requests`, make sure the local Requests code is the one importable (editable install or PYTHONPATH pointing to the clone).

<br>

>**IMPORTANT**: Install the `requests` development dependencies to run the `requests` tests`
>```
>cd requests
>pip install -r requirements-dev.txt
>```

<br>

### Not recommended (PyPI install)

``` bash
pip install requests
```

This installs Requests into `site-packages` and **breaks coverage
measurement** against local source code.

Use only if you are *not* measuring coverage.

<br>


## 5. Google Gemini API Key Setup

This project uses the `google-genai` client to generate tests.

### Set your API key as an environment variable

``` bash
export GOOGLE_API_KEY="your_api_key_here"
```

(Optional) To make it persistent, add it to your shell config:

``` bash
echo 'export GOOGLE_API_KEY="your_api_key_here"' >> ~/.zshrc
source ~/.zshrc
```



<br> 

## 6. Docker Setup (macOS)

LLM-generated tests may:  execute arbitrary Python code, access the filesystem and attempt network calls.

Docker provides: filesystem isolation, optional network isolation and a clean, reproducible Python environment.

Test generation (LLM calls) can be run locally.  
**Test execution and evaluation is recommended to be run in Docker.**

### Prerequisites

- macOS, Linux, or Windows
- Docker Desktop installed and running  
- Can use the example Dockerfile provided in the repository


<br>

Build the Docker Image (one-time) from the project root:

```bash
docker build -t evaluatingllm-eval -f docker/Dockerfile .
```

Make the Docker wrapper script executable:

```bash
chmod +x eval/scripts/run_in_docker.sh
```



Run any evaluation command via:

```bash
./eval/scripts/run_in_docker.sh <command>
```

All results are written to `eval/results/` on your host system.

#### Examples

```bash
./eval/scripts/run_in_docker.sh python eval/scripts/evaluate_strategy_correctness.py --strategy P0 --csv
```

```bash
./eval/scripts/run_in_docker.sh python eval/scripts/evaluate_strategy_coverage.py --strategy P0 --csv
```



### Network Access

By default, Docker runs with **no network access**.

To enable network access explicitly:

```bash
./eval/scripts/run_in_docker.sh --net python eval/scripts/evaluate_strategy_correctness.py --strategy P0
```


### Notes

- Your local Python virtual environment is **not used** inside Docker.
- The container installs the PyPI requests module for dependencies. The wrapper script exports the PYTHONPATH to point to your local requests clone.
- Docker is the recommended execution mode for this project.


------------------------------------------------------------------------
<br>
<br>

# Project structure (high-level)

    evaluatingLLM/
    ├── venv/                                       # Python virtual environment (not committed)
    ├── reuqests/                                   # Requests Python library to be provided by the user
    │   └── src/
    │   └── tests/
    │   └── (...)
    ├── docker/
    │   └── Dockerfile
    ├── eval/
    │   └── functions/
    │       └── functions_to_test.json              #JSON list of all chosen functions to be tested from request library 
    │   └── prompts/
    │       └── P0_Zero_Shot.txt
    │       └── P1_Zero_CoT.txt
    │       └── ...
    │   └── results/                                 # CSV outputs (correctness & coverage)
    │       └── correctness/  
    │           └── P0/
    │           └── P1/
    │           └── ...
    │       └── coverage/
    │       └── security/
    │   └── scripts/
    │       └── evaluate_strategy_correctness.py
    │       └── evaluate_strategy_coverage.py
    │       └── evaluate_strategy_security.py
    │       └── generate.py
    │   │   └── run_in_docker.sh
    │   └── tests/
    │       └── generated_tests/
    │           └── P0/
    │              └── _basic_auth_str/               #Function from functions_to_test.json
    │                 └── test_P0__basic_auth_str_1.py
    │                 └── test_P0__basic_auth_str_2.py
    │                 └── test_P0__basic_auth_str_3.py
    │              └── _parse_content_type_header/
    │              └── ... (more functions)
    │           └── P1/
    │              └── _basic_auth_str/         
    │                 └── test_P1__basic_auth_str_1.py
    │                 └── test_P1__basic_auth_str_2.py
    │                 └── test_P1__basic_auth_str_3.py
    └── README.md

<br>
<br>

# Generating Tests with generate.py 

#### Purpose
- Build LLM prompts from `eval/functions/functions_to_test.json` and generate test files via Gemini (google-genai).
- Outputs are written to `eval/tests/generated_tests/<STRATEGY>/<FUNCTION>/`.

#### Prerequisites
- Active virtualenv and basic tools installed (pytest/coverage are not required for generation).
- google-genai installed (the script imports `google.genai`).
- Set GEMINI_API_KEY in your environment (the script reads this to create a Gemini client).

#### Command Line Options
- _prompt-strategy_: one of P0, P1, P2, P3 (required).
- _model-name_: Gemini model name (default: gemini-2.5-flash).
- _function-name_: if set, only generate for that function listed in functions_to_test.json.
- _print-prompt_: build and print the prompt only (no LLM call, no output files).

#### Usage Examples: 
```
#Generate P1 tests for all functions in functions_to_test.json:
python eval/scripts/generate.py --prompt-strategy P1 

# Generate P2 (few-shot) tests for a single function:
python eval/scripts/generate.py --prompt-strategy P2 --function-name get_auth_from_url

# Print prompts for one function:
python eval/scripts/generate.py --prompt-strategy P1  --function-name parse_headers --print-prompt
```

#### Notes 
- P3 is a multi-step self-refine flow (step1/2/3). The script prints step1 prompts when --print-prompt is used; full P3 requires live model calls.
- Be mindful of API quotas and token usage when running bulk generation.
- Prompts and function metadata come from eval/prompts/ and eval/functions/functions_to_test.json. Adjust those files to change what is generated.

------------------------------------------------------------------------

<br>
<br>

# Using the Evaluation Scripts

## Correctness evaluation

#### Purpose
- Check generated test files for syntax, count asserts, run pytest on each file. 
- Classify results (pass / assertion failure / execution error). 
- Optionally write a CSV summary.
- Human-readable table printed to stdout.

#### Command Line Options
- _strategy_ : required, one of P0,P1,P2,P3 
- _tests_    : optional, function name for the tests (function/class folder inside the strategy dir). If omitted the whole strategy folder is evaluated.
- _csv_      : optional flag. When provided the script will create CSV at `eval/results/correctness/<strategy>/<tests_or_strategy>/results_<tests_or_strategy>.cs`

#### Usage Examples
```
#Run on an entire strategy:
python eval/scripts/evaluate_strategy_correctness.py --strategy P0 --csv

#Run on a single function folder inside a strategy:
python eval/scripts/evaluate_strategy_correctness.py --strategy P0 --tests get_auth_from_url --csv
```

<br>


## Coverage evaluation

#### Purpose and Behavior
- Run line+branch coverage for a group of tests. 
- The script creates a temporary or persistent `.coverage` data file and runs:
  `coverage run --branch --data-file=<data_file> --source=<sut_root> -m pytest <tests>`  
  If `--requests-functions` is used, the script passes explicit pytest nodeids (built by build_requests_functions_pytest_args()) instead of a test directory.
- Recommended to run this script once per strategy folder. The script is not designed to measure coverage for a single test file. 
- Optionally outputs a CSV file where one row has measurements for the whole test folder. 


#### Command Line Options
- _strategy_ (required unless --requests) : e.g. P0, P1, ...
- _tests_ (optional) : tests folder under the strategy to run (e.g. get_auth_from_url)
- _requests-all_ (flag) : runs all the tests under requests repo at <project_root>/requests/tests
- _reqests-functions_ (flag) : runs only the example reuqests library test cases that were listed on the functions_to_test.json. For fair coverage comparison between generated LLM tests and official requests tests.     
- _sut-root_ (optional) : path to SUT root, default requests/src/requests
- _label_ (optional): friendly label used in CSV/JSON filenames
- _csv_ (flag) : write CSV to eval/results/coverage/<strategy_or_requests>/coverage_results_<label>.csv
- _json-dir_ (flag) : keep coverage JSON/.coverage under eval/results/coverage/<strategy_or_requests>/json_results/

#### Usage Examples
```

#Coverage for LLM generated P0 tests cases for a specific requests function called _basic_auth_str
python ./eval/scripts/evaluate_strategy_coverage.py --strategy P0 --tests _basic_auth_str --csv --json-dir

#Coverage for all LLM generated P0 tests
python ./eval/scripts/evaluate_strategy_coverage.py --strategy P0 --csv 

#Coverage for all requests tests, some are not relevant for the project
python ./eval/scripts/evaluate_strategy_coverage.py --requests --csv

#Coverage for all relevant requests functions
python ./eval/scripts/evaluate_strategy_coverage.py --requests-functions --csv --json-dir

#Coverage for one specific relevant function from requests
python ./eval/scripts/evaluate_strategy_coverage.py --requests-functions --name get_auth_from_url --csv --json-dir
```


#### Notes 
- Keep `functions_to_test.json` nodeids accurate (project-root relative). 
- Use editable install (`pip install -e /path/to/requests`) or set PYTHONPATH so the source under test is the importable `requests` package.
- Use `--json-dir` when you want the JSON and .coverage artifacts for deeper debugging or to build an HTML coverage report later.


<br>



## Security evaluation


------------------------------------------------------------------------

<br>
<br> 

## Notes

-   `venv/`, `.coverage*`, `htmlcov/`, and result artifacts should be
    ignored via `.gitignore`
-   The Requests repo should **not** be committed inside this repository
-   The scripts assume macOS shell paths in examples; adjust activate/unlink commands for other shells/OSes.
-    Keep functions_to_test.json nodeids accurate (path portion must point to existing test files). build_requests_functions_pytest_args() resolves/validates nodeid file paths and will raise if the file does not exist.
