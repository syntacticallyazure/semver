#!/usr/bin/env python3
import argparse
import re
import subprocess

SEMVER_RE = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)$")


def get_semver_tags():
    try:
        result = subprocess.run(
            ["git", "tag"], capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError:
        raise RuntimeError("Not a git repository.")

    versions = []

    for tag in result.stdout.splitlines():
        if match := SEMVER_RE.match(tag):
            versions.append((tuple(map(int, match.groups())), tag))

    return sorted(versions, key=lambda x: x[0], reverse=True)


def main():
    parser = argparse.ArgumentParser(description="Get semantic version tags from Git.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--latest",
        action="store_true",
        help="Print the latest semantic version (default).",
    )
    group.add_argument(
        "--all",
        action="store_true",
        help="Print all semantic versions in descending order.",
    )
    args = parser.parse_args()

    versions = get_semver_tags()

    if not versions:
        parser.error("No semantic version tags found.")

    if args.all:
        print("\n".join(tag for _, tag in versions))
    else:
        print(versions[0][1])


if __name__ == "__main__":
    main()
