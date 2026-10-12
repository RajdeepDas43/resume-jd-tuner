#!/usr/bin/env python3
"""Report which tools this skill can use here, and how to install what is missing.

Usage:
  python3 check_env.py

Needed: Python 3.9+, reportlab 4.0.4+ (to build the PDF), pypdf 5.1+ (to read PDFs and links;
older versions glue words together in extracted text, which makes the PDF checks report false
failures), pdfminer.six (to measure page fill). Optional: pdftotext from poppler (a second PDF
reader, closer to what many ATS use) and a LaTeX engine (only for users who keep a .tex resume).

Exits 0 when the required packages are installed and recent enough, 1 otherwise.
"""
import importlib
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from resume_text import utf8_stdio  # noqa: E402

PYTHON_PACKAGES = [  # (import name, pip name, minimum version, why)
    ("reportlab", "reportlab", "4.0.4", "builds the resume PDF"),
    ("pypdf", "pypdf", "5.1", "reads PDFs, page counts and links"),
    ("pdfminer", "pdfminer.six", "20221105", "measures the empty space at the bottom of the page"),
]
TOOLS = [  # (command, why, install hint)
    ("pdftotext", "second PDF reader (poppler)",
     "macOS: brew install poppler | Debian/Ubuntu: apt install poppler-utils | Windows: choco install poppler"),
    ("pdflatex", "compiles .tex resumes (LaTeX users only)",
     "install TeX Live or MacTeX, or compile on overleaf.com"),
    ("xelatex", "compiles .tex resumes that use fontspec", "part of TeX Live / MacTeX"),
    ("latexmk", "runs LaTeX the right number of times", "part of TeX Live / MacTeX"),
]


def version_tuple(version):
    """'5.1.0' -> (5, 1, 0); '20221105' -> (20221105,); '6.0.0rc1' -> (6, 0, 0). Empty if unknown."""
    parts = []
    for piece in str(version).split("."):
        m = re.match(r"\d+", piece)
        if not m:
            break
        parts.append(int(m.group()))
        if m.end() < len(piece):  # "0rc1": keep the number, stop at the suffix
            break
    return tuple(parts)


def is_older(installed, minimum):
    """True when the installed version is known and below the minimum."""
    have, need = version_tuple(installed), version_tuple(minimum)
    if not have:
        return False
    width = max(len(have), len(need))
    return have + (0,) * (width - len(have)) < need + (0,) * (width - len(need))


def installed_version(module, pip_name):
    """The installed version, or "" when it can't be told."""
    try:
        from importlib.metadata import PackageNotFoundError, version
    except ImportError:  # Python before 3.8
        version = None
    if version:
        # Python 3.9 doesn't normalise names, and newer packages record "pdfminer_six", not "pdfminer.six".
        for name in dict.fromkeys((pip_name, pip_name.replace(".", "_"), pip_name.replace(".", "-"))):
            try:
                return version(name)
            except PackageNotFoundError:
                continue
            except Exception:
                break
    found = str(getattr(module, "__version__", getattr(module, "Version", "")))
    return "" if found in ("0.0", "0.0.0") else found  # placeholders some packages ship


def main():
    import argparse
    argparse.ArgumentParser(description="Report which tools this skill can use here.").parse_args()
    ok = sys.version_info >= (3, 9)
    print(f"python {sys.version.split()[0]}" + ("" if ok else "  (3.9+ needed)"))
    to_install = []
    for module, pip_name, minimum, why in PYTHON_PACKAGES:
        try:
            mod = importlib.import_module(module)
        except ImportError:
            ok = False
            to_install.append(f'"{pip_name}>={minimum}"')
            print(f"  MISSING  {pip_name}  - {why}")
            continue
        version = installed_version(mod, pip_name)
        if is_older(version, minimum):
            ok = False
            to_install.append(f'"{pip_name}>={minimum}"')
            print(f"  OUTDATED {pip_name} {version} (needs {minimum}+)  - {why}")
        else:
            print(f"  ok       {pip_name} {version or '(version unknown)'}  - {why}")
    for command, why, hint in TOOLS:
        path = shutil.which(command)
        print(f"  {'ok      ' if path else 'optional'} {command}  - {why}" + ("" if path else f"  [{hint}]"))
    if to_install:
        print("\ninstall with:  python3 -m pip install -U " + " ".join(to_install)
              + "\n(add --break-system-packages if pip refuses on a system Python, or use a venv)")
    print("\nENV: " + ("READY" if ok else "MISSING OR OUTDATED PACKAGES"))
    return 0 if ok else 1


if __name__ == "__main__":
    utf8_stdio()
    sys.exit(main())
