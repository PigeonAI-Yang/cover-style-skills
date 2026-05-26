#!/usr/bin/env python3
"""Fail final image prompts that leak creator names or skip identity protection."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


STYLE_SHORTCUT_PATTERNS = [
    re.compile(r"\binspired\s+by\b", re.IGNORECASE),
    re.compile(r"\b[a-z0-9 _-]+-inspired\b", re.IGNORECASE),
    re.compile(r"\bin\s+the\s+style\s+of\b", re.IGNORECASE),
    re.compile(r"\bstyle\s+of\b", re.IGNORECASE),
    re.compile(r"某某风格"),
    re.compile(r"风格迁移"),
]

IDENTITY_REQUIRED_PATTERNS = [
    re.compile(r"preserve (the )?(user'?s |provided |reference )?identity", re.IGNORECASE),
    re.compile(r"preserve identity traits", re.IGNORECASE),
    re.compile(r"preserve .*identity .*reference", re.IGNORECASE),
    re.compile(r"preserve .*PigeonYang .*identity", re.IGNORECASE),
    re.compile(r"preserve .*anime identity", re.IGNORECASE),
    re.compile(r"must resemble the user'?s (supplied |provided |reference )?(portrait|reference|image)", re.IGNORECASE),
    re.compile(r"保持用户.*身份"),
    re.compile(r"保留用户.*身份"),
    re.compile(r"保持.*人设"),
    re.compile(r"保留.*人设"),
    re.compile(r"保持.*身份参考"),
    re.compile(r"保留.*身份参考"),
]

PUBLIC_CREATOR_NEGATIVE_PATTERNS = [
    re.compile(r"must not resemble any public creator", re.IGNORECASE),
    re.compile(r"must not resemble a public creator", re.IGNORECASE),
    re.compile(r"must not resemble public creators", re.IGNORECASE),
    re.compile(r"不要像任何公众创作者"),
    re.compile(r"不得像任何公众创作者"),
]


def normalized_contains(text: str, needle: str) -> bool:
    return needle.casefold() in text.casefold()


def fail(message: str) -> None:
    raise SystemExit(f"prompt firewall failed: {message}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a final GPT Image prompt before image generation."
    )
    parser.add_argument("prompt_file", type=Path)
    parser.add_argument(
        "--forbid",
        action="append",
        default=[],
        help="creator name, alias, or phrase forbidden in the final generation prompt",
    )
    parser.add_argument(
        "--require-identity-reference",
        action="store_true",
        help="require explicit user identity preservation language",
    )
    args = parser.parse_args()

    if not args.prompt_file.exists():
        fail(f"prompt file does not exist: {args.prompt_file}")

    text = args.prompt_file.read_text(encoding="utf-8")
    if not text.strip():
        fail("prompt file is empty")

    forbidden_hits = [term for term in args.forbid if term and normalized_contains(text, term)]
    if forbidden_hits:
        fail("forbidden creator/style term(s) found: " + ", ".join(sorted(set(forbidden_hits))))

    style_hits = [pattern.pattern for pattern in STYLE_SHORTCUT_PATTERNS if pattern.search(text)]
    if style_hits:
        fail("style shortcut wording found; rewrite as concrete design rules")

    if args.require_identity_reference:
        if not any(pattern.search(text) for pattern in IDENTITY_REQUIRED_PATTERNS):
            fail("portrait reference was supplied, but prompt does not explicitly preserve user identity")
        if not any(pattern.search(text) for pattern in PUBLIC_CREATOR_NEGATIVE_PATTERNS):
            fail("portrait reference was supplied, but prompt does not block public-creator resemblance without naming a creator")

    print("prompt firewall OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
