# The LaTeX path

Use it when the user's résumé is a `.tex` file (attached, or in their résumé folder), or when they ask for LaTeX. Their template is their design: change the words, not the look.

## Steps

1. Copy their file to `<application folder>/First_Last_Role.tex`, with any files it needs beside it (images, `.cls` or `.sty` files).
2. Edit content only: summary, bullets, skills. Keep the preamble, macros, font, font size, margins, paper size and section order: the template is the user's design.
3. Copy profile links (`\href{...}{LinkedIn}` and the like) exactly from their file. Never guess or "fix" a handle.
4. Add the ATS-safety lines below if they are missing.
5. Compile twice, with the engine the template expects (look for `fontspec`: that means XeLaTeX or LuaLaTeX; otherwise pdfLaTeX):

   ```bash
   pdflatex -interaction=nonstopmode -halt-on-error First_Last_Role.tex
   pdflatex -interaction=nonstopmode -halt-on-error First_Last_Role.tex
   ```

   `latexmk -pdf` (or `-xelatex`, `-lualatex`) does the same in one call. Read the log on failure; a missing package usually means installing it (`tlmgr install <pkg>`) or compiling on Overleaf.
6. Run SKILL.md step 7 on the PDF with `--source First_Last_Role.tex`, and deliver both the `.tex` and the `.pdf`.

No TeX engine and none can be installed: say so, deliver the `.tex` with "upload this to overleaf.com and press Recompile", and run step 7 once the user shares the PDF. Or render with the default renderer if the user prefers.

## ATS-safety lines

Put these just before `\begin{document}`. They do not change how the page looks, and they compile under pdfLaTeX, XeLaTeX and LuaLaTeX (each line only acts where it applies):

```latex
% ATS-safe text layer: real Unicode for every glyph, real spaces between words,
% and outline (not bitmap) bullets. Does not change how the page looks.
\ifdefined\pdfgentounicode
  \input{glyphtounicode}\pdfgentounicode=1
  \ifdefined\UseLegacyTextSymbols \UseLegacyTextSymbols \fi
\fi
\ifdefined\pdfinterwordspaceon
  \pdfinterwordspaceon
\fi
```

Why they matter. pdfLaTeX does not write space characters into the PDF; a reader guesses word breaks from the gaps between letters. Where a bold run meets regular text, the gap often comes out too small and the extracted text glues the words: "Forward Deployment Engineer working" becomes "Engineerworking", and that keyword disappears from the ATS's view while the printed page looks perfect. `\pdfinterwordspaceon` writes real spaces and stops it. `glyphtounicode` maps ligatures and special glyphs to the right characters, so "efficient" doesn't come out as "e�cient". Since 2020, LaTeX draws `itemize` bullets from the TS1 text-symbol font; on installations without its outline version (BasicTeX, many Docker images) that font is a bitmap, and the bullet extracts as a control character or vanishes. `\UseLegacyTextSymbols` takes the bullet from the standard symbol font instead.

## Other LaTeX traps the checks catch

| pdf_checks says | Cause | Fix |
|---|---|---|
| Garbled characters, Type 3 (bitmap) fonts | `\usepackage[T1]{fontenc}` with no Type 1 font installed, so TeX falls back to bitmap fonts | Add `\usepackage{lmodern}` (or keep the template's font package and install it, e.g. `tlmgr install cm-super`) |
| Bullets come out as a control character or `(cid:N)` | Bitmap TS1 bullets (see above), or a symbol font without a Unicode map | The safety lines above on pdfLaTeX; on XeLaTeX or LuaLaTeX add `\UseLegacyTextSymbols` before `\begin{document}` |
| Glued words on XeLaTeX or LuaLaTeX | No interword-space switch in those engines | End the bold run at punctuation, or bold the whole phrase, so no bold-to-regular boundary falls between two words |
| Words missing (hyphenated at a line end) | TeX hyphenated a keyword across lines ("Kuber-" / "netes") | Add `\hyphenpenalty=10000 \exhyphenpenalty=10000` to the preamble, then re-check the page: line breaks may shift |
| Ligature characters (ﬁ, ﬀ) on XeLaTeX or LuaLaTeX | OpenType ligatures written as single glyphs | Add `\defaultfontfeatures{Ligatures=NoCommon}` before `\setmainfont`, or `Ligatures=NoCommon` in its options |
| Contact details or headers missing from the text | Header built from images or `tikz` text | Use real text for name, contact line and section titles |

## Filling or trimming the page in LaTeX

Content first (SKILL.md step 7): an extra relevant bullet or summary sentence before any spacing change, then the targeted questions to the user. When no more true content can come, small changes to the template's own spacing are acceptable (the section spacing, `itemsep` and `topsep` in the bullet list), up to about twice their original values, never its font size, and never margins below 0.5 inch. Say in the report what was changed, since the user asked to keep their template. To trim, cut the least relevant content before touching spacing.
