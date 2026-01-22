import argparse
import json
import os
import tempfile
from pathlib import Path

from google import genai  # recommended after 2025


# ---------- Paths ----------

# This assumes: eval/scripts/generate_tests.py
PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROMPTS_DIR = PROJECT_ROOT / "eval" / "prompts" / "API"
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
    ===TESTCASE_FILE_START=== / ===TESTCASE_FILE_END=== delimiters.

    Any reasoning or extra text outside these blocks (e.g. P1 CoT reasoning) is ignored.
    """
    START = "===TESTCASE_FILE_START==="
    END = "===TESTCASE_FILE_END==="

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
    
    # --- Reveal Model Parameter Defaults ---
    print(f"Fetching metadata for: {model_name}...")
    model_info = client.models.get(model=model_name)

    default_top_p = getattr(model_info, 'top_p', 'Not specified')
    default_top_k = getattr(model_info, 'top_k', None)
    top_k_display = default_top_k if default_top_k is not None else "None (Not applied)"
    default_temp = getattr(model_info, 'temperature', 1.0)

    print(f"  -> Default Temperature: {default_temp}")
    print(f"  -> Default TopP: {default_top_p}")
    print(f"  -> Default TopK: {top_k_display}")

    #-------------------------------------------------------------------
    print(f"Calling model: {model_name}")

    token_info = client.models.count_tokens(
        model=model_name,
        contents=prompt,
    )
    print(f"  -> estimated input tokens: {token_info.total_tokens}")

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
    )
    print("  -> model call complete")
    # google-genai exposes a .text convenience property

    if response.usage_metadata:
        print(f"  -> output tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print("  -> token usage metadata not available")

    # Check for empty or None response
    if not response.text:
        # Check if there's a safety/block reason
        if hasattr(response, 'prompt_feedback'):
            print(f"  -> Response blocked or empty. Feedback: {response.prompt_feedback}")
        if hasattr(response, 'candidates') and response.candidates:
            print(f"  -> Candidate finish reason: {response.candidates[0].finish_reason}")
        raise ValueError("Model returned empty response. Check safety filters or prompt content.")
    
    return response.text


# ---------- Prompt building helpers ----------

def build_prompt_P0(template: str, func_entry: dict) -> str:
    """
    P0 template uses:
      {{FUNCTION_NAME}}
      {{FUNCTION_DEFINITION}}
      {{N}}
      {{IMPORTS}}
      {{DEPENDENCIES}}
    """

    prompt = template
    prompt = prompt.replace("{{FUNCTION_NAME}}", func_entry["name"])
    prompt = prompt.replace("{{FUNCTION_DEFINITION}}", join_code_lines(func_entry.get("function_def", [])))
    prompt = prompt.replace("{{FUNCTION_MODULE}}", func_entry["module"])
    prompt = prompt.replace("{{DEPENDENCIES}}", get_dependencies(func_entry))
    prompt = prompt.replace("{{IMPORTS}}", join_code_lines(func_entry.get("imports", [])))
    prompt = prompt.replace("{{SETUP_NOTES}}", func_entry.get("setup_notes", ""))
    return prompt


def build_prompt_P1(template: str, func_entry: dict) -> str:
    """
    P1 template has the same placeholders as P0, but includes CoT instructions.
    """
    return build_prompt_P0(template, func_entry)

def join_code_lines(lines: list[str]) -> str:
    return "\n".join(lines)


def get_dependencies(func_entry: dict) -> str:
    """
    Concatenate dependency_function_def entries into a single space-separated string.
    """
    deps = func_entry.get("dependencies", []) or []

    for dep in deps:
        dep_def = dep.get("dependency_function_def")

        # Short-circuit if dependency explicitly says there are none
        if isinstance(dep_def, str) and dep_def.strip() == "No dependencies for this function were needed":
            return "No dependencies for this function were needed"

    blocks = []

    for dep in deps:
        dep_def = dep.get("dependency_function_def", [])
        code_str = "\n\n" + join_code_lines(dep_def) 
        blocks.append(code_str)

    dependencies_str = "\n\n".join(blocks) if blocks else "# No dependencies"
    return dependencies_str

def build_prompt_P2(template: str, func_entry: dict) -> str:
    """
    P2 template additionally takes {{EXAMPLE_TESTS}},
    which we build from func_entry["test_cases"][*]["test_code"].
    It sends all the given example test cases.
    """

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
    
    prompt = prompt.replace("{{EXAMPLE_TESTS}}", example_tests)
    prompt = prompt.replace("{{FUNCTION_NAME}}", func_entry["name"])
    prompt = prompt.replace("{{FUNCTION_DEFINITION}}", join_code_lines(func_entry.get("function_def", [])))
    prompt = prompt.replace("{{FUNCTION_MODULE}}", func_entry["module"])
    prompt = prompt.replace("{{DEPENDENCIES}}", get_dependencies(func_entry))
    prompt = prompt.replace("{{IMPORTS}}", join_code_lines(func_entry.get("imports", [])))
    prompt = prompt.replace("{{SETUP_NOTES}}", func_entry.get("setup_notes", ""))
    return prompt


def build_prompt_P3_step1(template: str, func_entry: dict) -> str:
    """Build the initial generation prompt (step 1)."""
    prompt = template
    prompt = prompt.replace("{{FUNCTION_NAME}}", func_entry["name"])
    prompt = prompt.replace("{{FUNCTION_DEFINITION}}", join_code_lines(func_entry.get("function_def", [])))
    prompt = prompt.replace("{{FUNCTION_MODULE}}", func_entry.get("module", ""))
    prompt = prompt.replace("{{DEPENDENCIES}}", get_dependencies(func_entry))
    prompt = prompt.replace("{{IMPORTS}}", join_code_lines(func_entry.get("imports", [])))
    prompt = prompt.replace("{{SETUP_NOTES}}", func_entry.get("setup_notes", ""))
    return prompt

def build_prompt_P3_step2(template: str, step1_output: str) -> str:
    """Build the critique/refinement guide prompt (step 2) by injecting step1 output and N."""
    prompt = template
    prompt = prompt.replace("{{GENERATED_TEST_CASES_FROM_STEP_1}}", step1_output)
    return prompt

def build_prompt_P3_step3(template: str, step1_output: str, step2_output: str) -> str:
    """Build the final refinement prompt (step 3) by injecting step1 & step2 outputs and N."""
    prompt = template
    prompt = prompt.replace("{{GENERATED_TEST_CASES_FROM_STEP_1}}", step1_output)
    prompt = prompt.replace("{{GENERATED_CRITIQUE_FROM_STEP_2}}", step2_output)
    return prompt

# ---------- Per-strategy generation ----------
# If test case with the same name exists, it will be overwritten. So actually each LLM run overwrites old tests

def generate_for_function_P0(client, model_name: str, func_entry: dict, out_dir: Path):
    template = load_prompt_template("P0")
    prompt = build_prompt_P0(template, func_entry)
    print(f"Generating P0 tests for function: {func_entry['name']}")

    raw_output = call_gemini(client, model_name, prompt)
    test_files = split_testcases(raw_output)

    ensure_dir(out_dir)
    base_name = f"test_P0_{func_entry['name']}"
    for i, content in enumerate(test_files, start=1):
        path = out_dir / f"{base_name}_{i}.py"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)


def generate_for_function_P1(client, model_name: str, func_entry: dict, out_dir: Path):
    template = load_prompt_template("P1")
    prompt = build_prompt_P1(template, func_entry)
    print(f"Generating P1 tests for function: {func_entry['name']}")

    raw_output = call_gemini(client, model_name, prompt)
    test_files = split_testcases(raw_output)

    ensure_dir(out_dir)
    base_name = f"test_P1_{func_entry['name']}"
    for i, content in enumerate(test_files, start=1):
        path = out_dir / f"{base_name}_{i}.py"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)


def generate_for_function_P2(client, model_name: str, func_entry: dict, out_dir: Path):
    template = load_prompt_template("P2")
    prompt = build_prompt_P2(template, func_entry)
    print(f"Generating P2 tests for function: {func_entry['name']}")

    raw_output = call_gemini(client, model_name, prompt)
    test_files = split_testcases(raw_output)

    ensure_dir(out_dir)
    base_name = f"test_P2_{func_entry['name']}"
    for i, content in enumerate(test_files, start=1):
        path = out_dir / f"{base_name}_{i}.py"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

def generate_for_function_P3(client, model_name: str, func_entry: dict, out_dir: Path):
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
    prompt1 = build_prompt_P3_step1(t1, func_entry)

    #TODO: delete print statements
    print(f"\n--- P3 Step 1 Prompt (function={func_entry['name']}) ---\n")
    print(prompt1)
    print("\n--- end prompt 1 ---\n")
    #delete 


    print(f"P3 Step 1: generating initial tests for: {func_entry['name']}")
    raw1 = call_gemini(client, model_name, prompt1)

    #TODO: delete print statements
    print(f"\n--- P3 Step 1 RAW OUTPUT (function={func_entry['name']}) ---\n")
    print(raw1)
    print("\n--- end raw1 ---\n")
    #delete

    # Step 2
    prompt2 = build_prompt_P3_step2(t2, raw1)

    #TODO: delete print statements
    print(f"\n--- P3 Step 2 Prompt (uses Step1 output) ---\n")
    print(prompt2)
    print("\n--- end prompt 2 ---\n")
    #delete


    print(f"P3 Step 2: generating critique for: {func_entry['name']}")
    raw2 = call_gemini(client, model_name, prompt2)

    #TODO: delete print statements
    print(f"\n--- P3 Step 2 RAW OUTPUT (critique) ---\n")
    print(raw2)
    print("\n--- end raw2 ---\n")
    #delete

    # Step 3
    prompt3 = build_prompt_P3_step3(t3, raw1, raw2)

    #TODO: delete print statements
    print(f"\n--- P3 Step 3 Prompt (uses Step1 + Step2 outputs) ---\n")
    print(prompt3)
    print("\n--- end prompt 3 ---\n")
    #delete


    print(f"P3 Step 3: generating refined tests for: {func_entry['name']}")
    raw3 = call_gemini(client, model_name, prompt3)

    #TODO:delete print statements
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

#gemini-3-pro   Request per minute:25    Tokens per minute:1M  Requests per day:250 

# Generate P1 tests for all functions in functions_to_test.json
python eval/scripts/generate.py --prompt-strategy P1 

# Generate P2 (few-shot) tests for a single function
python eval/scripts/generate.py --prompt-strategy P2 --function-name get_auth_from_url

#Print prompts for all functions or one function
python eval/scripts/generate.py --prompt-strategy P0  --print-prompt
python eval/scripts/generate.py --prompt-strategy P1  --function-name parse_headers --print-prompt
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
            strat = args.prompt_strategy

            template = load_prompt_template(strat) if strat != "P3" else load_prompt_template("P3_STEP1")
            if strat == "P0":
                prompt_text = build_prompt_P0(template, func_entry)
            elif strat == "P1":
                prompt_text = build_prompt_P1(template, func_entry)
            elif strat == "P2":
                prompt_text = build_prompt_P2(template, func_entry)
            elif strat == "P3":
                # Prints only the Step1 prompt. Steps 2/3 require model outputs.
                prompt_text = build_prompt_P3_step1(template, func_entry)
            else:
                raise SystemExit(f"Unknown strategy: {strat}")

            print("\n" + "=" * 80)
            print(f"Prompt for strategy={strat} function={func_name}:\n")
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
            generate_for_function_P0(client, args.model_name, func_entry, strategy_dir)
        elif args.prompt_strategy == "P1":
            generate_for_function_P1(client, args.model_name, func_entry, strategy_dir)
        elif args.prompt_strategy == "P2":
            generate_for_function_P2(client, args.model_name, func_entry, strategy_dir)
        elif args.prompt_strategy == "P3":
            generate_for_function_P3(client, args.model_name, func_entry, strategy_dir)


if __name__ == "__main__":
    main()
