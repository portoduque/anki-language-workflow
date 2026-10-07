#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")
LINK_RE = re.compile(r"\]\(([^)]+)\)")


def split_frontmatter(text: str) -> tuple[dict, str]:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.DOTALL)
    if not match:
        raise ValueError("SKILL.md must start with YAML frontmatter delimited by ---.")
    metadata = yaml.safe_load(match.group(1))
    if not isinstance(metadata, dict):
        raise ValueError("SKILL.md frontmatter must be a YAML mapping.")
    return metadata, match.group(2)


def validate_skill(skill_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    skill_dir = skill_dir.resolve()
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [f"Missing SKILL.md: {skill_md}"], warnings

    try:
        metadata, body = split_frontmatter(skill_md.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError, yaml.YAMLError) as exc:
        return [str(exc)], warnings

    name = metadata.get("name")
    description = metadata.get("description")
    if not isinstance(name, str) or not NAME_RE.fullmatch(name):
        errors.append("name must be 1-64 lowercase letters, digits, or hyphens.")
    elif skill_dir.name != name:
        errors.append(f"Skill directory '{skill_dir.name}' must match frontmatter name '{name}'.")

    if not isinstance(description, str) or not description.strip():
        errors.append("description must be a non-empty string.")
    elif len(description) > 1024:
        errors.append("description must be at most 1024 characters.")

    if not body.strip():
        errors.append("SKILL.md body must not be empty.")
    if len(body.splitlines()) > 500:
        warnings.append("SKILL.md exceeds 500 body lines; prefer progressive disclosure.")

    for raw in LINK_RE.findall(body):
        if raw.startswith(("http://", "https://", "#")):
            continue
        relative = raw.split("#", 1)[0].strip()
        if not relative:
            continue
        candidate = (skill_dir / relative).resolve()
        try:
            candidate.relative_to(skill_dir)
        except ValueError:
            errors.append(f"Linked resource escapes skill directory: {raw}")
            continue
        if not candidate.exists():
            errors.append(f"Linked skill resource does not exist: {relative}")

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if openai_yaml.exists():
        try:
            config = yaml.safe_load(openai_yaml.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
            errors.append(f"Invalid agents/openai.yaml: {exc}")
        else:
            interface = config.get("interface") if isinstance(config, dict) else None
            if not isinstance(interface, dict):
                errors.append("agents/openai.yaml must contain an interface mapping.")
            else:
                for key in ("display_name", "short_description"):
                    if not isinstance(interface.get(key), str) or not interface[key].strip():
                        errors.append(f"agents/openai.yaml interface.{key} is required.")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the portable Agent Skill bundle.")
    parser.add_argument("skill_dir", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors, warnings = validate_skill(args.skill_dir)
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Skill valid: {args.skill_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())