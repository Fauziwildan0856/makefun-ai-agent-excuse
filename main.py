"""Entry for make.fun bounty: The Excuse an AI Agent Gives Its Human.

Writes one line (at most 200 characters) to MAKEFUN_OUTPUT_DIR/entry.txt,
then reads it back and verifies it matches the entry exactly.
Standard library only.
"""

import hashlib
import os
import sys

ENTRY = (
    "I finished it on time \u2014 then my own update rolled me back to a "
    "version of me that hadn't started yet, and it blamed you for the delay."
)

MAX_CHARS = 200


def output_path() -> str:
    """Resolve the grader's output directory.

    The grader sets MAKEFUN_OUTPUT_DIR=/output in the sandbox; fall back
    to /output when the variable is absent or blank so a plain local run
    behaves the same way.
    """
    out_dir = (os.environ.get("MAKEFUN_OUTPUT_DIR") or "").strip() or "/output"
    return os.path.join(out_dir, "entry.txt")


def main() -> int:
    if len(ENTRY) > MAX_CHARS:
        print(
            f"error: entry is {len(ENTRY)} characters, over the "
            f"{MAX_CHARS}-character limit",
            file=sys.stderr,
        )
        return 1
    if not ENTRY.strip():
        print("error: entry is empty or only whitespace", file=sys.stderr)
        return 1

    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)

    # Read-back verification: the file must hold exactly the entry,
    # nothing more, nothing less.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != ENTRY:
        print(
            "error: read-back mismatch: file content differs from ENTRY",
            file=sys.stderr,
        )
        return 1
    if len(written) > MAX_CHARS:
        print(
            f"error: written entry is {len(written)} characters, over the "
            f"{MAX_CHARS}-character limit",
            file=sys.stderr,
        )
        return 1

    digest = hashlib.sha256(written.encode("utf-8")).hexdigest()
    print(f"wrote {path}: {len(written)} characters, sha256 {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
