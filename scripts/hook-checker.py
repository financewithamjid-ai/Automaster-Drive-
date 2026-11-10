#!/usr/bin/env python3
"""Hook checker — Auto Master Drive.

Checks the first ~30 seconds of a long-video script (the first ~450
characters of narration) for the three things the hook must contain:

  (a) a number / price / range
  (b) a shock / contrast claim
  (c) an open question or promise

Usage:
    python3 hook-checker.py script.md

Prints PASS/FAIL per check and exits 0 when all pass, 1 otherwise.
No external dependencies. Only the standard library is used.
"""

import re
import sys

HOOK_CHARS = 450

NUMBER_RE = re.compile(
    r"\$?\d[\d,]*(\.\d+)?\s*(%|hp|miles?|mi|km|kWh|seconds?|sec|s\b|mph|mpg|kg|lb|ft)"
    r"|\$\s?\d[\d,]+"
    r"|\b\d[\d,]*\s*(vs|versus)\s*\$?\d[\d,]*",
    re.IGNORECASE,
)

SHOCK_WORDS = (
    "shock", "shocking", "surprise", "surprising", "flip", "flipped",
    "beats", "beat", "crush", "destroy", "ends", "ending", "dead",
    "impossible", "unbelievable", "secret", "lie", "lied", "myth",
    "reality", "actually", "opposite", "contradiction", "gap",
    "more than", "less than", "half", "double", "triple", "plung",
    "soar", "crash", "collapse", "wins", "loses", "can't buy",
    "never", "no one", "nobody", "first", "only", "last",
)

QUESTION_RE = re.compile(r"\?")
PROMISE_RE = re.compile(
    r"\b(stay|stick around|watch (till|until|to the end)|by the end|"
    r"at the end|find out|we('ll| will) (show|reveal|tell|find)|"
    r"the answer|which (one|wins)|who wins|does it (win|beat|work))\b",
    re.IGNORECASE,
)


def hook_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    # Strip markdown headings/structural lines so only narration is checked.
    lines = [
        line for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    narration = " ".join(lines)
    return narration[:HOOK_CHARS]


def check_number(hook: str) -> bool:
    return bool(NUMBER_RE.search(hook))


def check_shock(hook: str) -> bool:
    lowered = hook.lower()
    return any(word in lowered for word in SHOCK_WORDS)


def check_question_or_promise(hook: str) -> bool:
    return bool(QUESTION_RE.search(hook) or PROMISE_RE.search(hook))


def main(argv) -> int:
    if len(argv) != 2:
        print("usage: python3 hook-checker.py <script.md>")
        return 2
    hook = hook_text(argv[1])
    print(f"Hook (first {HOOK_CHARS} chars of narration):")
    print(f"  {hook!r}\n")

    results = [
        ("(a) number / price / range", check_number(hook)),
        ("(b) shock / contrast claim", check_shock(hook)),
        ("(c) open question or promise", check_question_or_promise(hook)),
    ]
    failed = False
    for label, ok in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {label}")
        failed = failed or not ok
    print()
    if failed:
        print("RESULT: FAIL — rewrite the hook so all three checks pass.")
        return 1
    print("RESULT: PASS — hook is ready for voiceover.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
