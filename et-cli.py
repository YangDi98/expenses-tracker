#!/usr/bin/env python3
import sys
import subprocess


def run_lint():
    subprocess.run(["poetry", "run", "black", "."], check=True)
    subprocess.run(["poetry", "run", "flake8", "."], check=True)


def main():
    if len(sys.argv) != 2 or sys.argv[1] != "lint":
        print("Usage: ./et-cli.py lint")
        sys.exit(1)
    run_lint()


if __name__ == "__main__":
    main()
