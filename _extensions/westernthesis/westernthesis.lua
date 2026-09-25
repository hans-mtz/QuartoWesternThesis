-- westernthesis.lua — structural logic for the Western thesis format.
--
-- Front matter / main matter switch (SGPS §6.6): every level-1 heading before the
-- first numbered chapter is a preliminary page (roman numbering). `\westernmainmatter`
-- is inserted right before the first numbered chapter so it starts at page 1.

local mainmatter_started = false

local function is_numbered_chapter(el)
  return el.level == 1 and not el.classes:includes("unnumbered")
end

function Header(el)
  if not quarto.doc.is_format("latex") then
    return nil
  end
  -- A book chapter file without a heading (e.g. frontmatter/lists.qmd) gets an
  -- empty `\chapter{}` from Quarto; drop it so it is neither a page nor a chapter.
  if el.level == 1 and #el.content == 0 then
    return {}
  end
  if not mainmatter_started and is_numbered_chapter(el) then
    mainmatter_started = true
    return { pandoc.RawBlock("latex", "\\westernmainmatter"), el }
  end
  return nil
end
