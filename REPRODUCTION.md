# Separately dated reproduction records

## 22 October 2026: same Windows machine

A new Python 3.12.14 virtual environment installed the pinned baseline dependencies. MarkItDown and PyMuPDF4LLM without an optional OCR engine each exited 0 and reproduced their historical output SHA256 exactly. Installing the separate pinned OCR requirements, then running PyMuPDF4LLM in a new process, exited 0 and reproduced its historical RapidOCR output hash exactly. This is environment isolation on one machine, not an independent clean machine.

The portable specimen generator was also replayed with ReportLab 4.4.9. Its PDF matched the original source hash; both rendered page previews were visually inspected.

Marker replay used the existing isolated Marker environment and local pinned models. It returned and saved the identical 436-byte historical output with both page checkpoints. The outer command ended with exit 1 and an empty redirected console log. No completed supervisor process.json was written. Child exit and root cause are unknown. This route is NOT counted as a clean process pass. The updated harness writes a start journal before waiting so an interrupted supervisor cannot be mistaken for a completed run. It does not fix or conceal upstream cleanup behavior.

## Independent machine

A public standard Windows GitHub Actions runner can execute the three light routes from a new VM. The workflow does not run Marker and cannot establish a four-route clean-machine pass. Read the actual Actions run before making any claim about its result. No independent-machine result is claimed in this initial record.

SHA256 checks freeze published bytes, not general extraction accuracy. One synthetic English sample does not establish performance on other documents or languages.
