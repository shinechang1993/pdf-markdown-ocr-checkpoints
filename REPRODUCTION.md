# Separately dated reproduction records

## 22 October 2026: same Windows machine

A new Python 3.12.14 virtual environment installed the pinned baseline dependencies. MarkItDown and PyMuPDF4LLM without an optional OCR engine each exited 0 and reproduced their historical output SHA256 exactly. Installing the separate pinned OCR requirements, then running PyMuPDF4LLM in a new process, exited 0 and reproduced its historical RapidOCR output hash exactly. This is environment isolation on one machine, not an independent clean machine.

The portable specimen generator was also replayed with ReportLab 4.4.9. Its PDF matched the original source hash; both rendered page previews were visually inspected.

Marker replay used the existing isolated Marker environment and local pinned models. It returned and saved the identical 436-byte historical output with both page checkpoints. The outer command ended with exit 1 and an empty redirected console log. No completed supervisor process.json was written. Child exit and root cause are unknown. This route is NOT counted as a clean process pass. The updated harness writes a start journal before waiting so an interrupted supervisor cannot be mistaken for a completed run. It does not fix or conceal upstream cleanup behavior.

## Independent machine

The [actual public Actions run 39769924829](https://github.com/shinechang1993/pdf-markdown-ocr-checkpoints/actions/runs/39769924829), commit5a86c24e73c8896b4f0b3cc2844a0269c943dcd3, ran on a fresh standard windows-2025 VM with official Windows Python3.12.10, distinct from the local bundled3.12.14 runtime. Job119794599015 completed successfully on22October2026 (11:21:14–11:22:01 UTC). The downloaded job log contains all three actual converter executions, their raw Markdown, per-process exit0 records, SHA256 values and final dependency freeze. All three output hashes matched the historical files. This is a three-light-route independent-machine pass, not a four-route pass; Marker was not run on that VM.

The first two workflow attempts failed at Python setup because the requested3.12.14 Windows build was unavailable on windows-2025; converter steps were skipped. These were environment failures, not conversion results. The workflow now explicitly selects the available official3.12.10 Windows build.

An initial local clone exposed Git's Windows automatic newline conversion on this ASCII-compatible PDF and raw Markdown. Added .gitattributes to mark the source PDF and historical raw files as byte-preserved. A subsequent unauthenticated clone passed every published source/output hash check. No historical file was rewritten.

SHA256 checks freeze published bytes, not general extraction accuracy. One synthetic English sample does not establish performance on other documents or languages.
