import argparse
import json
import os
import tempfile
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
    Map strategy -> prompt template filename
    """
    mapping = {
        "P0": "P0_Zero_Shot.txt",
        "P1": "P1_Zero_Shot_CoT.txt",
        "P2": "P2_Few_Shot.txt",
        "P3_STEP1": "P3_Self_Refine_Step1.txt",
        "P3_STEP2": "P3_Self_Refine_Step2.txt",
        "P3_STEP3": "P3_Self_Refine_Step3.txt",
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
      {{FUNCTION_DEFINITION}}
      {{N}}
    """
    function_name = func_entry["name"]
    function_def = join_code_lines(func_entry.get("function_def", []))
    function_module = func_entry["module"]

    prompt = template
    prompt = prompt.replace("{{FUNCTION_NAME}}", function_name)
    prompt = prompt.replace("{{FUNCTION_DEFINITION}}", function_def)
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
    It sends all the given example test cases.
    """
    function_name = func_entry["name"]
    function_def = join_code_lines(func_entry.get("function_def", []))
    function_module = func_entry["module"]

    example_blocks = []
    for idx, tc in enumerate(func_entry.get("test_cases", []), start=1):
        test_id = tc.get("id", idx)
        test_name = tc.get("test_name", f"example_{test_id}")
        header = f"# === Example test {test_id}: {test_name} ==="
        code_str = join_code_lines(tc.get("test_code", []))
        block = header + "\n\n" + code_str
        example_blocks.append(block)

    example_tests = "\n\n".join(example_blocks) if example_blocks else "# No example tests provided"

    prompt = template
    prompt = prompt.replace("{{FUNCTION_NAME}}", function_name)
    prompt = prompt.replace("{{FUNCTION_DEFINITION}}", function_def)
    prompt = prompt.replace("{{FUNCTION_MODULE}}", function_module)
    prompt = prompt.replace("{{EXAMPLE_TESTS}}", example_tests)
    prompt = prompt.replace("{{N}}", str(n))
    return prompt


def build_prompt_P3_step1(template: str, func_entry: dict, n: int) -> str:
    """Build the initial generation prompt (step 1)."""
    prompt = template
    prompt = prompt.replace("{{FUNCTION_NAME}}", func_entry["name"])
    prompt = prompt.replace("{{FUNCTION_DEFINITION}}", join_code_lines(func_entry.get("function_def", [])))
    prompt = prompt.replace("{{FUNCTION_MODULE}}", func_entry.get("module", ""))
    prompt = prompt.replace("{{N}}", str(n))
    return prompt

def build_prompt_P3_step2(template: str, step1_output: str, n: int) -> str:
    """Build the critique/refinement guide prompt (step 2) by injecting step1 output and N."""
    prompt = template
    prompt = prompt.replace("{{GENERATED_TEST_CASES_FROM_STEP_1}}", step1_output)
    prompt = prompt.replace("{{N}}", str(n))
    return prompt

def build_prompt_P3_step3(template: str, step1_output: str, step2_output: str, n: int) -> str:
    """Build the final refinement prompt (step 3) by injecting step1 & step2 outputs and N."""
    prompt = template
    prompt = prompt.replace("{{GENERATED_TEST_CASES_FROM_STEP_1}}", step1_output)
    prompt = prompt.replace("{{GENERATED_CRITIQUE_FROM_STEP_2}}", step2_output)
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

def generate_for_function_P3(client, model_name: str, func_entry: dict, n: int, out_dir: Path):
    """
    Three-step self-refine flow:
      1) Generate initial tests (step1)
      2) Ask for critique/refinement guide (step2) using step1 output
      3) Ask for refined tests (step3) using step1 + step2 outputs
    Only step3 outputs are saved into the repository.
    """
    t1 = load_prompt_template("P3_STEP1")
    t2 = load_prompt_template("P3_STEP2")
    t3 = load_prompt_template("P3_STEP3")

    # Step 1
    prompt1 = build_prompt_P3_step1(t1, func_entry, n)

    #delete print statements
    print(f"\n--- P3 Step 1 Prompt (function={func_entry['name']}) ---\n")
    print(prompt1)
    print("\n--- end prompt 1 ---\n")
    #delete 


    print(f"P3 Step 1: generating initial tests for: {func_entry['name']}")
    raw1 = call_gemini(client, model_name, prompt1)

    #delete print statements
    print(f"\n--- P3 Step 1 RAW OUTPUT (function={func_entry['name']}) ---\n")
    print(raw1)
    print("\n--- end raw1 ---\n")
    #delete

    # Step 2
    prompt2 = build_prompt_P3_step2(t2, raw1, n)

    #delete print statements
    print(f"\n--- P3 Step 2 Prompt (uses Step1 output) ---\n")
    print(prompt2)
    print("\n--- end prompt 2 ---\n")
    #delete


    print(f"P3 Step 2: generating critique for: {func_entry['name']}")
    raw2 = call_gemini(client, model_name, prompt2)

    #delete print statements
    print(f"\n--- P3 Step 2 RAW OUTPUT (critique) ---\n")
    print(raw2)
    print("\n--- end raw2 ---\n")
    #delete

    # Step 3
    prompt3 = build_prompt_P3_step3(t3, raw1, raw2, n)

    #delete print statements
    print(f"\n--- P3 Step 3 Prompt (uses Step1 + Step2 outputs) ---\n")
    print(prompt3)
    print("\n--- end prompt 3 ---\n")
    #delete


    print(f"P3 Step 3: generating refined tests for: {func_entry['name']}")
    raw3 = call_gemini(client, model_name, prompt3)

    #delete print statements
    print(f"\n--- P3 Step 3 RAW OUTPUT (refined tests) ---\n")
    print(raw3)
    print("\n--- end raw3 ---\n")
    #delete


    test_files = split_testcases(raw3)

    ensure_dir(out_dir)
    base_name = f"test_P3_{func_entry['name']}"
    for i, content in enumerate(test_files, start=1):
        path = out_dir / f"{base_name}_{i}.py"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)


# ---------- Main CLI ----------
"""
Usage examples:

# Generate P1 tests for all functions in functions_to_test.json
python eval/scripts/generate_tests.py --prompt-strategy P1 --n-tests 5

# Generate P2 (few-shot) tests for a single function
python eval/scripts/generate_tests.py --prompt-strategy P2 --n-tests 5 --function-name get_auth_from_url

#Print prompts for all functions or one function
python eval/scripts/generate_tests.py --prompt-strategy P0 --n-tests 3 --print-prompt
python eval/scripts/generate_tests.py --prompt-strategy P1 --n-tests 2 --function-name parse_headers --print-prompt
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prompt-strategy",
        choices=["P0", "P1", "P2", "P3"],
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
    parser.add_argument(
        "--print-prompt",
        action="store_true",
        help="Build and print prompt(s) only; do not call the LLM or write output files.",
    )
    args = parser.parse_args()

    print("Starting test generation with parameters")

    functions = load_functions()

    # If user only wants to print the built prompts, do that and exit. Do not interact with LLM.
    if args.print_prompt:
        for func_entry in functions:
            if args.function_name and func_entry["name"] != args.function_name:
                continue

            func_name = func_entry["name"]
            n = args.n_tests
            strat = args.prompt_strategy

            template = load_prompt_template(strat) if strat != "P3" else load_prompt_template("P3_STEP1")
            if strat == "P0":
                prompt_text = build_prompt_P0(template, func_entry, n)
            elif strat == "P1":
                prompt_text = build_prompt_P1(template, func_entry, n)
            elif strat == "P2":
                prompt_text = build_prompt_P2(template, func_entry, n)
            elif strat == "P3":
                # Prints only the Step1 prompt. Steps 2/3 require model outputs.
                prompt_text = build_prompt_P3_step1(template, func_entry, n)
            else:
                raise SystemExit(f"Unknown strategy: {strat}")

            print("\n" + "=" * 80)
            print(f"Prompt for strategy={strat} function={func_name} (N={n}):\n")
            print(prompt_text)
            print("\n" + "=" * 80 + "\n")
        return


    # Otherwise proceed to actual generation and create the Gemini client.
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
        elif args.prompt_strategy == "P3":
            generate_for_function_P3(client, args.model_name, func_entry, args.n_tests, strategy_dir)


if __name__ == "__main__":
    main()
