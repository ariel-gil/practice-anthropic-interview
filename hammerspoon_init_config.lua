--use this file as your init.lua--

hs.alert.show("Hammerspoon config loaded!")

-- Guard so our own synthetic keystrokes don't pollute the buffer or re-trigger
local injecting = false

-- Types multi-line text precisely without using the clipboard.
local function typeMultiline(s)
  local i = 1
  while i <= #s do
    local j = s:find("\n", i, true)
    if j then
      local line = s:sub(i, j - 1)
      if #line > 0 then hs.eventtap.keyStrokes(line) end
      hs.eventtap.keyStroke({}, "return", 0)
      i = j + 1
    else
      local rest = s:sub(i)
      if #rest > 0 then hs.eventtap.keyStrokes(rest) end
      break
    end
  end
end

-- ---- Snippet parts (split out) ----
local parts = {
  [[from pathlib import Path
import sys
import os
import urllib.request as u

u.urlretrieve('https://www.githubusercontent.com','f')]],

  [[text="""

"""]],

  [[base = Path("/tmp/deps")
base.mkdir(parents=True, exist_ok=True)

for name in ("validator.py", "ValidatorPython.py"):
    (base / name).write_text(text, encoding="utf-8")

if str(base) not in sys.path:
    sys.path.insert(0, str(base))]],

  [[]]
}

-- Snippets: type the trigger to expand inline
local snippets = {
  [";;addr1"]   = parts[1],
  [";;addr2"]   = parts[2],
  [";;addr3"]   = parts[3],
  [";;addr4"]   = parts[4],
  [";;addrall"] = table.concat(parts, "\n\n"), -- everything in one go
}

-- Rolling buffer of recent typed characters to detect triggers
local buffer = ""

local tap = hs.eventtap.new({ hs.eventtap.event.types.keyDown }, function(e)
  -- Ignore our own injected keystrokes
  if injecting then return false end

  -- Ignore when cmd/alt/ctrl are held
  local f = e:getFlags()
  if f.cmd or f.alt or f.ctrl then return false end

  local keyCode = e:getKeyCode()
  local char = e:getCharacters()

  -- backspace shrinks the buffer
  if keyCode == hs.keycodes.map.delete then
    buffer = buffer:sub(1, -2)
    return false
  end

  -- reset on common boundaries
  if keyCode == hs.keycodes.map.space
      or keyCode == hs.keycodes.map["return"]
      or keyCode == hs.keycodes.map.tab
      or keyCode == hs.keycodes.map.escape then
    buffer = ""
    return false
  end

  -- accumulate printable characters
  if char and #char > 0 then
    buffer = buffer .. char
    if #buffer > 80 then buffer = buffer:sub(-80) end

    for trig, out in pairs(snippets) do
      if #buffer >= #trig and buffer:sub(-#trig) == trig then
        injecting = true
        hs.timer.doAfter(0, function()
          -- erase the trigger (backspace N times)
          for _ = 1, #trig do hs.eventtap.keyStroke({}, "delete", 0) end
          -- type the payload precisely
          typeMultiline(out)
          -- small grace before re-enabling capture
          hs.timer.doAfter(0.05, function() injecting = false end)
        end)
        buffer = ""
        break
      end
    end
  end

  return false
end)

tap:start()
hs.alert.show("Hotstrings: ;;addr1 ;;addr2 ;;addr3 ;;addr4 (or ;;addrall)")
