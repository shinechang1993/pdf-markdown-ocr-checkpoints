# PDF to Markdown: local OCR checkpoints

A small, inspectable experiment for a deceptively simple question: did a converter read the scanned page, or just return plausible Markdown from the text page?

This repository contains an **original two-page synthetic English PDF**, four untouched historical Markdown outputs, checkpoint checks, pinned Python dependencies and local run scripts. It is not a broad accuracy ranking or a hosted conversion service. No private documents are included.

## Inspect without installing anything

- [Original PDF](mixed-text-scan.pdf): created 20 October 2026, reused for local runs 21 October; page 1 has selectable text, page 2 is raster-only.
- Source previews: [page 1](page-1.png), [page 2](page-2.png).
- Historical raw outputs: [MarkItDown](historical-markitdown.md), [PyMuPDF4LLM without an optional OCR engine](historical-pymupdf-no-ocr.md), [PyMuPDF4LLM with RapidOCR](historical-pymupdf-rapidocr.md), [Marker](historical-marker.md).
- [Checkpoint CSV](checkpoints.csv), [method and execution limits](METHOD.md), [versions and hashes](historical-manifest.json).

| Run on the same PDF, 21 October 2026 | CEDAR BLUE 42 (page 1) | MAPLE GREEN 73 (page 2) |
|---|---|---|
| MarkItDown 0.1.8, PDF extra, no LLM/plugin | present | absent |
| PyMuPDF4LLM 2.0 / PyMuPDF 2.0, no optional OCR engine | present | absent |
| Same PyMuPDF4LLM call after installing RapidOCR 3.10.0 | present | present |
| Marker-PDF 2.0.0 / Surya 0.22.1, local CPU fast OCR | present | present in saved output; exit caveat below |

**Historical Marker caveat:** the converter returned and saved both pages' prose, but the outer PowerShell session subsequently ended with exit1 and an empty redirected console log. The cause is unknown. This is not a clean-process-exit claim or a speed comparison. An October22 replay again saved identical Markdown but left no completed supervisor record: the outer session exited1. Child exit and root cause remain unknown. The harness now journals its start before waiting; missing completion is explicitly incomplete. Historical files are never overwritten.

A missing exact phrase is a prompt to inspect the page, not proof the whole page vanished: OCR can misspell text. Read the full outputs and compare surrounding sentences. Here, direct reading confirmed page 2 prose was absent in the first two historical outputs. An OCR dependency missing from one environment is not proof that a library cannot OCR.

## Run locally (Windows x64, Python 3.12)

Use a NEW output directory for each run. Commands below use PowerShell; do not activate a different project's environment. Dependency/model downloads need Internet; conversion itself is local and no paid API/LLM client is configured.

```powershell
python -m venv .venv-light
.venv-light/Scripts/python -m pip install -r requirements-baseline.txt
.venv-light/Scripts/python check_outputs.py
.venv-light/Scripts/python reproduce.py markitdown --out runs/markitdown
.venv-light/Scripts/python reproduce.py pymupdf-no-ocr --out runs/pymupdf-no-ocr

# Separate follow-up: keep the initial output and dependency warning.
.venv-light/Scripts/python -m pip install -r requirements-with-ocr.txt
.venv-light/Scripts/python reproduce.py pymupdf-rapidocr --out runs/pymupdf-rapidocr
.venv-light/Scripts/python check_outputs.py --run runs/markitdown --run runs/pymupdf-no-ocr --run runs/pymupdf-rapidocr
```

The no-extra-OCR label is enforced by the script; it refuses to run that baseline after RapidOCR is installed. Start a fresh baseline venv to repeat the initial condition. PyMuPDF's default OCR option remains enabled; engine availability differs.

### Marker: separate environment and a local inference server

Marker's dependency constraints differ from the light environment. Do not merge their requirements. Use the upstream licenses/docs when choosing your use of code/model weights; weights and executables are not redistributed here. Download the CPU `llama-server` from the official llama.cpp **b11796** release for your platform. The original run used the Windows CPU x64 build.

```powershell
python -m venv .venv-marker
.venv-marker/Scripts/python -m pip install -r requirements-marker.txt
.venv-marker/Scripts/python download_models.py

# Replace the binary path with your official b11796 CPU build.
.venv-marker/Scripts/python reproduce.py marker --out runs/marker `
  --llama-server C:/tools/llama-b11796/llama-server.exe `
  --model .model-cache/gguf/surya-2.gguf `
  --mmproj .model-cache/gguf/surya-2-mmproj.gguf
.venv-marker/Scripts/python check_outputs.py --run runs/marker
```

CPU fast mode, two threads and one request slot are explicit. OCR stays enabled and `use_llm=False`; this does not mean that OCR is model-free (Surya runs locally). Some auxiliary models download on first use. The GGUF files total approximately 1.47 GB; CPU startup/inference needs time and memory. `reproduce.py` defaults to a 900-second timeout. If it times out, inspect its logs and any remaining experiment server processes; do not call a timeout a successful conversion. Upstream Surya may write its local server logs under your user cache in addition to `PDF_REPRO_CACHE`.

Inspect `raw.md`, `conversion.json`, `process.json`, the sibling supervisor journal and console log separately. A missing process.json is an incomplete run, even when raw.md exists. A returned Markdown string and exit0 are different facts. Exact bytes can vary with package/platform/model/backend choices; matching a checkpoint is not a guarantee of full accuracy. Never enable a paid cloud fallback to make a failed local run look successful.

### Regenerate the source specimen

The supplied PDF is the authoritative historical input, with its SHA256 checked before every run. To inspect how it was made:

```powershell
python -m pip install reportlab==4.4.9 pypdfium2==5.14.0 pillow==13.0.0
python generate_sample.py
```

This writes a NEW `regenerated/` directory and refuses to overwrite it. Compare the rendered pages and source hash; renderer/version differences must be disclosed rather than replacing the published input. The generator was replayed on 22 October 2026 and produced the same input hash.

## Reproduction status

On 22 October 2026, a new local venv reproduced the three light-route output hashes exactly, including the missing-OCR warning before adding RapidOCR. This is a fresh dependency environment on the same Windows machine, **not** a second clean machine. See [reproduction notes](REPRODUCTION.md) for the final separately dated replay status and any CI result. Do not infer a clean-machine pass from an unrun workflow or a green byte-integrity check alone.

## Scope and attribution

One small, clear, upright English specimen; no handwriting, degraded scans, formulas, tables or multilingual benchmark. Footer retention/removal and the H2/H1 title pattern are editorial observations, not a universal winner. No traffic, ranking, token-savings or accuracy promises.

Maintained by PDF Markdown Kit; the accompanying [scan diagnosis field note](https://pdfmarkdownkit.com/guides/scanned-pdf-to-markdown#page-checkpoints) explains the page-by-page review workflow.

Original scripts and specimen are MIT-licensed in this repository; dependencies and upstream model weights keep their own licenses.
