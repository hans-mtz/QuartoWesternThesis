# Western University Thesis Template for Quarto

A [Quarto](https://quarto.org) book template that renders a PDF thesis in the format
required by the School of Graduate and Postdoctoral Studies (SGPS) at the University of
Western Ontario. It follows the Senate
[Procedure for Thesis Formats and Content](https://www.uwo.ca/univsec/pdf/academic_policies/grad_postdoc/thesis_procedures_format.pdf)
(effective June 5, 2026) and the layout of the SGPS Word template.

You write each chapter in Markdown (`.qmd`). The template handles the title page, front
matter order, page numbering, margins, lists and spacing.

## Requirements

- [Quarto](https://quarto.org/docs/get-started/) 1.4 or later
- A LaTeX distribution with LuaLaTeX, for example [TeX Live](https://tug.org/texlive/) or
  TinyTeX (`quarto install tinytex`)

## Get started

Create a new thesis folder from the template:

```sh
quarto use template hans-mtz/QuartoWesternThesis
```

Then render it:

```sh
quarto render
```

The PDF is written to `_thesis/thesis.pdf`.

To use the format in an existing Quarto book, add only the extension:

```sh
quarto add hans-mtz/QuartoWesternThesis
```

and set `format: westernthesis-pdf` in `_quarto.yml`.

## Fill in your thesis

1. Edit the title page information in `_quarto.yml`:

   ```yaml
   book:
     title: "Your Thesis Title"
     author:
       - name:
           given: Jane
           family: Doe        # underlined on the title page
     date: 2026-09-01         # shown as "September 2026"

   supervisor: "Dr. A. Supervisor"   # or a list for several supervisors
   program: "Statistics and Actuarial Science"
   degree: "Doctor of Philosophy"
   degree-level: doctoral             # doctoral | masters
   keywords: [time series, long memory]
   ```

2. Write the front matter in `index.qmd` (Abstract) and `frontmatter/`.
3. Write your chapters in `chapters/` and list them in `_quarto.yml` under `book.chapters`.
4. Put references in `references.bib`, appendices in `appendices/`, and your CV in
   `backmatter/cv.qmd`.

Remove the files you don't need from `_quarto.yml`, for example the Co-Authorship
Statement or the List of Abbreviations.

## What the template does for you

| Requirement | How it is handled |
|---|---|
| Title page | Laid out as in the SGPS Word template. It counts as page i, with no number shown. |
| Front matter order | Abstract and Keywords, Summary for Lay Audience, Co-Authorship Statement, Acknowledgements, GenAI statement, Table of Contents, then the List of Tables, Figures, Plates, Appendices and Abbreviations. |
| Preliminary pages in the TOC | Every front-matter page and list gets a Table of Contents entry. |
| Page numbers | Roman numerals centred at the bottom in the front matter. Arabic numerals in the upper right from page 1 of Chapter 1, including chapter opening pages. |
| Margins | 1.5 in left and 1 in top, right and bottom on every page. |
| Text | 12 pt Times (TeX Gyre Termes), 1.5 line spacing, Arial-style headings (TeX Gyre Heros). Footnotes are 10 pt. The bibliography is single-spaced. |
| Word limits | Warns during rendering if the Abstract is over 150 (master's) or 350 (doctoral) words, or the Lay Summary is over 350. |
| Lists | The List of Plates and List of Appendices appear only if the thesis has plates or appendices. |
| Curriculum Vitae | Last page, not lettered as an appendix. |

## Writing features

**Figures, tables, equations and theorems** use standard Quarto cross-references
(`@fig-`, `@tbl-`, `@eq-`, `@thm-`, `@sec-`). See `chapters/02-long-memory.qmd`.

**Plates** (photographs and similar) have their own numbering and list:

```markdown
::: {#plt-site}
![](images/site.jpg)

Aerial photograph of the study site.
:::
```

**Published chapters.** SGPS requires a footnote on chapters that are published,
accepted or submitted. Add an attribute with the citation to the chapter heading:

```markdown
# Long Memory in River Flows {#sec-flows published="@doe2025"}
```

This prints "A version of this chapter has been published: Doe (2025)." Use
`accepted=` or `submitted=` for the other statuses.

**References at the end of each chapter** (common in integrated-article theses):

```yaml
format:
  westernthesis-pdf:
    chapter-bibliographies: true
```

Each chapter that cites gets its own reference list. You can then remove
`backmatter/references.qmd` from the chapters list.

## Options

Set these under `format: westernthesis-pdf:` in `_quarto.yml`.

| Option | Default | Description |
|---|---|---|
| `title-page` | `true` | Print the SGPS title page. |
| `running-headers` | `true` | Chapter number and title at the top left of body pages. |
| `line-spacing` | `onehalf` | `onehalf` or `double` (SGPS allows 1.5 to 2). |
| `chapter-bibliographies` | `false` | A reference list at the end of each chapter. |
| `chapter-bibliography-title` | `References` | Heading of those lists. |

Use a different citation style by adding `csl: your-style.csl` to `_quarto.yml`
([Zotero style repository](https://www.zotero.org/styles)).

## Check the layout

`_scripts/check-layout.py` checks every page of the PDF against the SGPS margin and
page-number rules. It needs `pdftotext` from Poppler.

```sh
python3 _scripts/check-layout.py _thesis/thesis.pdf
```

Wide figures and tables are the usual cause of margin problems.

## Notes

- **Title page.** The Senate procedure says Scholarship@Western generates a title page
  on upload. The SGPS website and Word template ask you to include one. This template
  includes it by default. Set `title-page: false` if SGPS tells you to leave it out.
- **Always check the current SGPS requirements** and your program's rules before you
  submit. This template is not an official SGPS product.

## Credits

The example content is adapted from the Western LaTeX thesis template by Justin Veenstra
(2010). The extension structure follows
[quarto-cnam-thesis](https://github.com/zinc75/quarto-cnam-thesis).
