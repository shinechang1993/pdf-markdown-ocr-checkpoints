# Method

Input created20October2026; original local executions21October2026. This input is reused for22October replay, not a new specimen. One PDF, two pages. Page1 selectable text: CEDAR BLUE 42. Page2 raster-only image: MAPLE GREEN 73. The original generator, input hash and PNG previews allow independent inspection.

The MarkItDown baseline uses its PDF extra with plugins disabled and no LLM client. PyMuPDF4LLM's default call is executed first without an optional OCR engine, then in a separately preserved run after RapidOCR installation. The first warning concerns the environment; the library supports optional OCR. The first output is never replaced by the second.

Marker uses local CPU fast, Surya0.22.1 and llama.cpp b11796, OCR enabled, optional external LLM disabled, two threads and one slot. Historical raw output contains both page bodies, but the outer PowerShell session ended exit1 with empty redirected log, cause unknown. This caveat must accompany any use of that historical result; no process-success or speed claim. Hosted Datalab/Chandra is not a substitute.

Inspect both exact phrase presence and the full surrounding page text. Check footer policy separately: PyMuPDF4LLM's OCR follow-up retains and joins provenance/page-counter lines; historical Marker removes both footers (with the same exit caveat). Both OCR-enabled historical outputs have H2 thenH1 titles. Retaining versus removing repeated footers is a task-dependent choice, not an accuracy ranking.

Only source and raw-output bytes are frozen. Runtime timing is not controlled. No statistic here is a universal quality measure. No source documents, filenames or extracted text are sent to a paid service by these scripts. Package/model downloads are inbound network requests. New process logs and generated files belong in separate run directories.
