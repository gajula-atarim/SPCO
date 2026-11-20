"""Inline the WHC report stylesheet and logo into a report source file.

Usage: python3 reports/whc-brand/build.py <source.src.html> <output.html>

The source file uses two placeholders:
  <!--WHC:CSS-->   replaced with <style>…whc-report.css…</style>
  WHC_LOGO_SRC     replaced with the logo as a data: URI (use it in <img src="WHC_LOGO_SRC">)
The output is a single self-contained HTML file, ready to publish as an artifact.
"""
import base64
import pathlib
import sys

here = pathlib.Path(__file__).resolve().parent
src, out = map(pathlib.Path, sys.argv[1:3])

css = (here / "whc-report.css").read_text(encoding="utf-8")
logo = base64.b64encode((here / "whc-logo.png").read_bytes()).decode()

html = src.read_text(encoding="utf-8")
html = html.replace("<!--WHC:CSS-->", "<style>\n" + css + "</style>")
html = html.replace("WHC_LOGO_SRC", "data:image/png;base64," + logo)
out.write_text(html, encoding="utf-8")
print(f"wrote {out} ({out.stat().st_size:,} bytes)")
