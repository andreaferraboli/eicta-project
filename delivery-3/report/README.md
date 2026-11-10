# Report, delivery 3

**Provisional template.** The official templates (Word, LaTeX) are linked in `../ASSIGNMENT.md` and are not in this repository. Download the official LaTeX template and move these chapters into it; until then this template keeps the structure required by the PDF.

Page limit: **at most 30 pages**.

## Structure

- `main.tex`: preamble, front page (title, group number, members, academic year: all `TODO`), table of contents, chapters.
- `chapters/*.tex`: one chapter per request of the PDF. Queries are included directly from the source files (`\lstinputlisting`), so the report always shows the code that was actually run.
- `figures/`: high-resolution images. The same folder is delivered as "folder with high-resolution images".

## Figures and evidence

`\evidence{file}{caption}{label}` includes `figures/<file>` if it exists, otherwise it prints a red **TODO: missing evidence** box with the expected file name. Search the PDF for "TODO" to see what is missing. Never put a text output in place of a screenshot of the tool.

## Compile locally

```
python scripts/eicta.py report 3        # from the project root, output in build/delivery-3/report/main.pdf
```

or, from this folder: `latexmk -pdf main.tex`.

## Overleaf

The listings read files outside `report/` (`../sql/...`, `../neo4j/...`, `../mongodb/...`). Upload the whole `delivery-3` folder as a zip (New Project > Upload Project), then in Menu set *Main document* to `report/main.tex`.
