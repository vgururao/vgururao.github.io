#!/usr/bin/env python3
"""
build.py — rebuild index.html and cv.html from Markdown sources.

Install dependencies once:
    /opt/homebrew/bin/python3 -m pip install markdown weasyprint --break-system-packages

Usage:
    python3 build.py          # rebuild HTML pages
    python3 build.py --pdf    # rebuild HTML + regenerate CV.pdf
"""

import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit("markdown not installed.\nRun: /opt/homebrew/bin/python3 -m pip install markdown --break-system-packages")

ROOT = Path(__file__).parent
EXTENSIONS = ['extra', 'md_in_html']


def render(md_path: Path, template_path: Path, out_path: Path) -> None:
    content_html = markdown.markdown(md_path.read_text('utf-8'), extensions=EXTENSIONS)
    output = template_path.read_text('utf-8').replace('<!-- CONTENT -->', content_html)
    out_path.write_text(output, 'utf-8')
    print(f"  {md_path.relative_to(ROOT)}  →  {out_path.name}")


def build_pdf(html_path: Path, pdf_path: Path) -> None:
    try:
        import weasyprint
    except ImportError:
        sys.exit(
            "weasyprint not installed.\n"
            "Run: /opt/homebrew/bin/python3 -m pip install weasyprint --break-system-packages\n"
            "If that fails, also try: brew install pango"
        )
    weasyprint.HTML(filename=str(html_path.resolve())).write_pdf(str(pdf_path))
    print(f"  {html_path.name}  →  {pdf_path.name}")


if __name__ == '__main__':
    print("Building HTML...")
    render(ROOT / 'content/index.md', ROOT / 'templates/index.html', ROOT / 'index.html')
    render(ROOT / 'content/cv.md',    ROOT / 'templates/cv.html',    ROOT / 'cv.html')
    print("Done.")

    if '--pdf' in sys.argv:
        print("\nBuilding CV PDF...")
        build_pdf(ROOT / 'cv.html', ROOT / 'CV.pdf')
        print("Done.")
