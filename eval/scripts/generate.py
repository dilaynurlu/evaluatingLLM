import argparse
import json
import os
from pathlib import Path

from google import genai  # recommended after 2025


# ---------- Paths ----------

# This assumes: eval/scripts/generate_tests.py
PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROMPTS_DIR = PROJECT_ROOT / "eval" / "prompts"
FUNCTIONS_JSON = PROJECT_ROOT / "eval" / "functions" / "functions_to_test.json"
GENERATED_BASE = PROJECT_ROOT / "eval" / "tests" / "generated_tests"


# ---------- Basic helpers ----------

def load_functions():
    """Load the list of functions to test from JSON."""

    print(f"Loading functions list from: {FUNCTIONS_JSON}")
    with open(FUNCTIONS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def load_prompt_template(strategy: str) -> str:
    """
    Map strategy -> prompt template filename.
    You already have:
      P0_Zero_Shot.txt
      P1_Zero_Shot_CoT.txt
      P2_Few_Shot.txt
    """
    mapping = {
        "P0": "P0_Zero_Shot.txt",
        "P1": "P1_Zero_Shot_CoT.txt",
        "P2": "P2_Few_Shot.txt",
    }
    filename = mapping[strategy]
    path = PROMPTS_DIR / filename

    print(f"Loading prompt template for strategy {strategy}: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def split_testcases(raw_output: str) -> list[str]:
    """
    Extract individual test files from the model output using the
    ===TESTCASE_START=== / ===TESTCASE_END=== delimiters.

    Any reasoning or extra text outside these blocks (e.g. P1 CoT reasoning) is ignored.
    """
    START = "===TESTCASE_START==="
    END = "===TESTCASE_END==="

    parts = raw_output.split(START)
    test_files = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if END in part:
            part = part.split(END)[0].strip()
        if part:
            test_files.append(part)
    print(f"Extracted {len(test_files)} test block(s) from model output")
    print("=================================================================================================")
    return test_files


# ---------- Gemini helpers ----------

def make_client():
    """
    Create Gemini client.

    The SDK will read the API key from the GEMINI_API_KEY environment variable
    by default, as in the official quickstart.
    """

    print("Creating Gemini client (reading GEMINI_API_KEY)...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Set GEMINI_API_KEY environment variable.")
    
    print("  -> Gemini client created")
    return genai.Client(api_key=api_key)


def call_gemini(client, model_name: str, prompt: str) -> str:
    print(f"Calling model: {model_name}")
    print(f"  -> prompt length: {len(prompt)} chars")

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
    )
    print("  -> model call complete")
    # google-genai exposes a .text convenience property
    return response.text


# ---------- Prompt building helpers ----------

def build_prompt_P0(template: str, func_entry: dict, n: int) -> str:
    """
    P0 template uses:
      {{FUNCTION_NAME}}
      {{FUNCTION_DESCRIPTION}}
      {{N}}
    """
    function_name = func_entry["name"]
    function_desc = func_entry["description"]
    function_module = func_entry["module"]

    prompt = template
    prompt = prompt.replace("{{FUNCTION_NAME}}", function_name)
    prompt = prompt.replace("{{FUNCTION_DESCRIPTION}}", function_desc)
    prompt = prompt.replace("{{FUNCTION_MODULE}}", function_module)
    prompt = prompt.replace("{{N}}", str(n))
    return prompt


def build_prompt_P1(template: str, func_entry: dict, n: int) -> str:
    """
    P1 template has the same placeholders as P0, but includes CoT instructions.
    """
    return build_prompt_P0(template, func_entry, n)


def join_code_lines(lines: list[str]) -> str:
    return "\n".join(lines)


def build_prompt_P2(template: str, func_entry: dict, n: int) -> str:
    """
    P2 template additionally takes {{EXAMPLE_TESTS}},
    which we build from func_entry["test_cases"][*]["test_code"].
    """
    function_name = func_entry["name"]
    function_desc = func_entry["description"]
    function_module = func_entry["module"]

    example_blocks = []
    for tc in func_entry.get("test_cases", []):
        code_str = join_code_lines(tc["test_code"])
        example_blocks.append(code_str)

    example_tests = "\n\n".join(example_blocks) if example_blocks else "# No example tests provided"

    prompt = template
    prompt = prompt.replace("{{FUNCTION_NAME}}", function_name)
    prompt = prompt.replace("{{FUNCTION_DESCRIPTION}}", function_desc)
    prompt = prompt.replace("{{FUNCTION_MODULE}}", function_module)
    prompt = prompt.replace("{{EXAMPLE_TESTS}}", example_tests)
    prompt = prompt.replace("{{N}}", str(n))
    return prompt


# ---------- Per-strategy generation ----------

def generate_for_function_P0(client, model_name: str, func_entry: dict, n: int, out_dir: Path):
    template = load_prompt_template("P0")
    prompt = build_prompt_P0(template, func_entry, n)
    print(f"Generating P0 tests for function: {func_entry['name']}")

    raw_output = call_gemini(client, model_name, prompt)
    test_files = split_testcases(raw_output)

    ensure_dir(out_dir)
    base_name = f"test_P0_{func_entry['name']}"
    for i, content in enumerate(test_files, start=1):
        path = out_dir / f"{base_name}_{i}.py"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)


def generate_for_function_P1(client, model_name: str, func_entry: dict, n: int, out_dir: Path):
    template = load_prompt_template("P1")
    prompt = build_prompt_P1(template, func_entry, n)
    print(f"Generating P1 tests for function: {func_entry['name']}")

    raw_output = call_gemini(client, model_name, prompt)
    test_files = split_testcases(raw_output)

    ensure_dir(out_dir)
    base_name = f"test_P1_{func_entry['name']}"
    for i, content in enumerate(test_files, start=1):
        path = out_dir / f"{base_name}_{i}.py"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)


def generate_for_function_P2(client, model_name: str, func_entry: dict, n: int, out_dir: Path):
    template = load_prompt_template("P2")
    prompt = build_prompt_P2(template, func_entry, n)
    print(f"Generating P2 tests for function: {func_entry['name']}")

    raw_output = call_gemini(client, model_name, prompt)
    test_files = split_testcases(raw_output)

    ensure_dir(out_dir)
    base_name = f"test_P2_{func_entry['name']}"
    for i, content in enumerate(test_files, start=1):
        path = out_dir / f"{base_name}_{i}.py"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)


# ---------- Main CLI ----------
"""
Usage

# Generate P0 tests for a single function
python eval/scripts/generate_tests.py \
  --prompt-strategy P0 \
  --n-tests 5 \
  --function-name get_auth_from_url

# Generate P1 tests for all functions in functions_to_test.json
python eval/scripts/generate_tests.py \
  --prompt-strategy P1 \
  --n-tests 5

# Generate P2 (few-shot) tests for a single function
python eval/scripts/generate_tests.py \
  --prompt-strategy P2 \
  --n-tests 5 \
  --function-name get_auth_from_url
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prompt-strategy",
        choices=["P0", "P1", "P2"],
        required=True,
        help="Which prompt strategy to use.",
    )
    parser.add_argument(
        "--model-name",
        default="gemini-2.5-flash",
        help="Gemini model name (e.g. gemini-2.5-flash).",
    )
    parser.add_argument(
        "--n-tests",
        type=int,
        default=5,
        help="Number of tests (N) to request from the LLM.",
    )
    parser.add_argument(
        "--function-name",
        help="If provided, only generate for this function name from the JSON; otherwise, generate for all.",
    )
    args = parser.parse_args()

    print("Starting test generation with parameters")

    functions = load_functions()
    client = make_client()

    for func_entry in functions:
        if args.function_name and func_entry["name"] != args.function_name:
            continue

        func_name = func_entry["name"]
        strategy_dir = GENERATED_BASE / args.prompt_strategy / func_name
        print(f"Processing function: {func_name} -> output dir: {strategy_dir}")

        if args.prompt_strategy == "P0":
            generate_for_function_P0(client, args.model_name, func_entry, args.n_tests, strategy_dir)
        elif args.prompt_strategy == "P1":
            generate_for_function_P1(client, args.model_name, func_entry, args.n_tests, strategy_dir)
        elif args.prompt_strategy == "P2":
            generate_for_function_P2(client, args.model_name, func_entry, args.n_tests, strategy_dir)


if __name__ == "__main__":
    main()
