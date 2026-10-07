---
name: reference-brand-pdf-script
description: "How to actually run scripts/md_to_brand_pdf.py — the system Python's weasyprint is broken; use the ~/.venvs/e4e-pdf venv"
metadata:
  node_type: memory
  type: reference
  originSessionId: 8db06326-4b4d-4049-9b7a-48ebcf0eced6
  modified: 2026-08-27T22:08:34.576Z
---

`scripts/md_to_brand_pdf.py` renders any project Markdown doc into the house-style E4E PDF (A4, ivory paper, tree letterhead, Cormorant Garamond headings, Lexend body, Deep Bronze gold rules — per `.claude/brand-voice-guidelines.md` §16). This is the standard format for Sabi research/proposal docs (matches existing PDFs like `SABI_HARD_QUESTIONS.pdf`, `RESEARCH_BRIEF_SENDABLE.pdf`).

**It does not run on the system `python3`** — as of Aug 2026, Homebrew's Python had `weasyprint==68.1` (needs `tinycss2>=1.5.0`) but only `tinycss2==1.4.0` installed, throwing `ModuleNotFoundError: No module named 'tinycss2.color5'`. Homebrew's Python is also PEP-668 externally-managed, so `pip install --upgrade` (even with `--user`) is blocked without `--break-system-packages`.

**Fix applied:** created an isolated venv instead of touching the system Python:
```bash
python3 -m venv ~/.venvs/e4e-pdf
~/.venvs/e4e-pdf/bin/pip install "weasyprint==68.1" "tinycss2>=1.5.0" markdown
```

**Usage going forward:**
```bash
~/.venvs/e4e-pdf/bin/python3 scripts/md_to_brand_pdf.py <input.md> [output.pdf] [--tag "Sabi programme"]
```
Do not `pip install` weasyprint/tinycss2 into the system/Homebrew Python again — use this venv.
