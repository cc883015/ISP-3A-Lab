"""Python package root. Run this file to print the layout."""

from pathlib import Path

if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    print("python packages:", ", ".join(sorted(p.name for p in here.iterdir() if p.is_dir())))
