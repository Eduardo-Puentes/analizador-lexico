import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEXER = ROOT / "clang-lexer.py"
INPUTS = ROOT / "tests" / "inputs"


def run_case(source_path: Path) -> tuple[str, str]:
    result = subprocess.run(
        [sys.executable, str(LEXER), str(source_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip(), result.stderr.strip()


def main() -> int:
    failures = []

    for source_path in sorted(INPUTS.glob("*.c")):
        stdout_actual, stderr_actual = run_case(source_path)
        is_valid_case = source_path.name.startswith("valid-")
        has_stdout = bool(stdout_actual)
        has_stderr = bool(stderr_actual)
        case_passed = has_stdout and ((is_valid_case and not has_stderr) or (not is_valid_case and has_stderr))

        if not case_passed:
            failures.append(source_path.name)
            print(f"[FAIL] {source_path.name}")
            if not has_stdout:
                print("  lexer did not produce any tokens")
            elif is_valid_case and has_stderr:
                print("  valid case produced lexical errors")
            elif not is_valid_case and not has_stderr:
                print("  invalid case did not produce lexical errors")
        else:
            print(f"[PASS] {source_path.name}")

    if failures:
        print("\nFailed cases:")
        for name in failures:
            print(f"- {name}")
        return 1

    print("\nAll lexer cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
