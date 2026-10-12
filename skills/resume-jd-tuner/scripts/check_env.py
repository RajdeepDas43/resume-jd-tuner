#!/usr/bin/env python3
"""Report which tools this skill can use here, and how to install what is missing.

Usage:
  python3 check_env.py

Needed: Python 3.9+, reportlab (to build the PDF), pypdf (to read PDFs and links),
pdfminer.six (to measure page fill). Optional: pdftotext from poppler (a second PDF reader,
closer to what many ATS use) and a LaTeX engine (only for users who keep a .tex resume).
"""
import importlib
import shutil
import sys

PYTHON_PACKAGES = [  # (import name, pip name, why)
    ("reportlab", "reportlab", "builds the resume PDF"),
    ("pypdf", "pypdf", "reads PDFs, page counts and links"),
    ("pdfminer", "pdfminer.six", "measures the empty space at the bottom of the page"),
]
TOOLS = [  # (command, why, install hint)
    ("pdftotext", "second PDF reader (poppler)",
     "macOS: brew install poppler | Debian/Ubuntu: apt install poppler-utils | Windows: choco install poppler"),
    ("pdflatex", "compiles .tex resumes (LaTeX users only)",
     "install TeX Live or MacTeX, or compile on overleaf.com"),
    ("xelatex", "compiles .tex resumes that use fontspec", "part of TeX Live / MacTeX"),
    ("latexmk", "runs LaTeX the right number of times", "part of TeX Live / MacTeX"),
]


def main():
    import argparse
    argparse.ArgumentParser(description="Report which tools this skill can use here.").parse_args()
    ok = True
    print(f"python {sys.version.split()[0]}" + ("" if sys.version_info >= (3, 9) else "  (3.9+ needed)"))
    missing_pip = []
    for module, pip_name, why in PYTHON_PACKAGES:
        try:
            mod = importlib.import_module(module)
            version = getattr(mod, "__version__", getattr(mod, "Version", ""))
            print(f"  ok       {pip_name} {version}  - {why}")
        except ImportError:
            ok = False
            missing_pip.append(pip_name)
            print(f"  MISSING  {pip_name}  - {why}")
    for command, why, hint in TOOLS:
        path = shutil.which(command)
        print(f"  {'ok      ' if path else 'optional'} {command}  - {why}" + ("" if path else f"  [{hint}]"))
    if missing_pip:
        print("\ninstall with:  python3 -m pip install " + " ".join(missing_pip)
              + "\n(add --break-system-packages if pip refuses on a system Python, or use a venv)")
    print("\nENV: " + ("READY" if ok else "MISSING PACKAGES"))


if __name__ == "__main__":
    main()
