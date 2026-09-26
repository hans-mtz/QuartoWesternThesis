# CLAUDE.md

## Project

A Quarto **custom format extension** (`quarto use template`) that renders a PDF thesis
meeting the requirements of the School of Graduate and Postdoctoral Studies (SGPS),
University of Western Ontario. PDF output only (no HTML format).

Quarto docs: https://quarto.org/docs/extensions/formats.html
Local toolchain: Quarto 1.9.x, TeX Live (xelatex/lualatex/tlmgr), pdftotext.

## Reference material (read-only — never edit)

- `WesternThesisLatex/` — 2010 LaTeX template (J. Veenstra). Useful for LaTeX idioms
  (list of appendices via `tocloft`, theorem envs, CV table) but **outdated**: it has a
  Certificate of Examination, twoside layout and a title page, all of which the current
  policy no longer wants. Do not copy its layout rules.
- `quarto-cnam-thesis-main/` — a mature Quarto thesis extension (Cnam, France) used as the
  architectural example: book project + `_extensions/<name>/` with `_extension.yml`,
  `_schema.yml`, Lua filter, template partials, `.quartoignore`.

- `etd_template2026.docx` — SGPS Word template (2026). Source of truth for the **visual
  style and the title page**. `thesis_procedures_format.pdf` — local copy of the policy.

## Authoritative requirements (source of truth)

Senate "Procedure for Thesis Formats and Content", effective 2026-06-05:
https://www.uwo.ca/univsec/pdf/academic_policies/grad_postdoc/thesis_procedures_format.pdf
Also: https://grad.uwo.ca/academics/thesis/formatting.html

Key rules the format must enforce:
- **Title page** as in the SGPS Word template (the grad website asks students to include
  it; the policy text says Scholarship@Western adds one). It is page i, number not shown.
  No Certificate of Examination. No signatures, emails, phone numbers or addresses anywhere.
- Front matter order (Word template): Title page → Abstract + Keywords → Summary for Lay
  Audience (≤350 words) → Co-Authorship Statement (if applicable) → Acknowledgements
  (optional) → Statement on the use/non-use of GenAI (required, §4.7) → Table of Contents →
  List of Tables → List of Figures → List of Appendices → List of Abbreviations, Symbols,
  Nomenclature → Preface (optional). Epigraph / Dedication are optional (policy §1.4).
- All preliminary pages appear in the Table of Contents.
- Abstract limit: 150 words (master's) / 350 words (doctoral).
- Body: Introduction … Conclusion → Bibliography → Appendices → Curriculum Vitae (last).
- Published/submitted chapters carry the footnote "A version of this chapter has been
  published/accepted for publication/submitted for publication (citation)."
- Font ≥ 12 pt for text (≥ 9 pt allowed for footnotes, figures, formulas, appendices).
- Line spacing 1.5–2 for all text including front matter; references, bibliography and
  block quotes may be single-spaced.
- Margins: left ≥ 1.5 in; top, bottom, right ≥ 1 in, on every page (so one-sided layout,
  no mirrored margins). Figures and tables must fit inside them too.
- Word template style: Times New Roman 12pt body, 1.5 spacing, no first-line indent, 12pt
  before each paragraph; headings Arial bold (16/16/14pt; front-matter titles centred);
  captions bold "Table 1: …"; bibliography single-spaced; footnotes 10pt. The template
  uses TeX Gyre Termes / Heros as the Times / Arial equivalents.
- Page numbers: front matter = lowercase roman, centred at the bottom, ≥ 0.5 in from the
  edge. Body = arabic starting at 1 on the first page of Chapter 1 / Introduction, in the
  **upper right corner**, ≥ 0.5 in from each edge (including chapter opening pages).

## Design decisions (agreed with the user)

- Quarto **book** project, one file per chapter. Extension name `westernthesis`, format
  `westernthesis-pdf`. Repo: `QuartoWesternThesis` under the user's GitHub account.
- Title page: on by default (`title-page: true`), laid out like the SGPS Word template.
- Citations: citeproc + CSL by default.
- Running headers (chapter/section title + page number top right): **on** by default, option
  to turn off.
- Per-chapter bibliographies (integrated-article theses): opt-in, in v1.
- GenAI statement goes after Acknowledgements (SGPS Word template order).
- Per-chapter bibliographies are implemented in `westernthesis.lua` (`chapter-bibliographies`),
  not with pandoc-ext/section-bibliographies, which breaks Quarto cross-references in books.
- The filter runs at the default (pre-quarto) stage: after Quarto's filters, chapter
  headings are wrapped in Quarto nodes. Anything that needs post-shortcode state goes
  through metadata read by the template (e.g. `has-appendices`).
- List of Plates is kept (Word template has it; the policy doesn't) via a custom `plt`
  crossref float (aux ext `lopl`, since `lop` is Quarto's listings). Quarto turns
  crossref divs into `FloatRefTarget` custom nodes before user filters: match them with
  a `FloatRefTarget` filter function; `doc:walk` does not visit them.
- Test the template as a student gets it: commit, `git clone` to the scratchpad, then
  `quarto use template <clone> --no-prompt` in an empty dir (a local-path install also
  copies git-ignored files).

## Conventions

- Prefer **template partials** and `include-in-header` over replacing Pandoc's whole
  `template.tex`, so the extension keeps working as Quarto updates.
- Structural logic (front/main matter switch, lists placement, appendix list, chapter
  publication footnotes) lives in the Lua filter, not in user content.
- Every user-facing option is declared in `_schema.yml` with a description.
- Keep the example content generic (no real people's names).

## Commands

```sh
quarto render                       # render the example thesis (book project) to PDF
quarto use template ./ --no-prompt  # test installing the template into a scratch dir
```

After a layout change, run `python3 _scripts/check-layout.py` (margins and page-number
positions on every page; exits non-zero on a violation), and `pdftotext -layout` for the
front-matter order. Setspace gotcha: `\singlespacing` resets the font size — use
`\setstretch{1}` before `\fontsize` in heading formats.
