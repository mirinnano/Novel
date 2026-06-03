import re
import difflib

md_path = r"C:\Users\quicp\OneDrive\Desktop\Novel\src\07_day7.md"
aria_path = r"C:\Users\quicp\OneDrive\Desktop\engine\src\AriaEngine\assets\scripts\scenario_08.aria"

with open(md_path, "r", encoding="utf-8") as f:
    md_lines = f.read().splitlines()

with open(aria_path, "r", encoding="utf-8") as f:
    aria_lines = f.read().splitlines()

# Strip engine tags and trailing slashes from aria
aria_text = []
for line in aria_lines:
    if line.startswith(";") or line.startswith("*"): continue
    if line.strip() in ("cls()", "nvl", "adv", "fx_reset()", "mood_danger()", "mood_calm()", "fx_sunlight()", "fx_fog()", "fx_focus()"): continue
    if "scenechange(" in line or "chapter_card_fx(" in line or "set_vflag" in line or "set_sflag" in line or "set_pflag" in line or "clear_vflag" in line or "goto " in line or "fx_scene_cut" in line: continue
    
    clean_line = line.rstrip("\\")
    if clean_line.strip():
        aria_text.append(clean_line.strip())

md_text = [l.strip() for l in md_lines if l.strip()]

# Compare
matcher = difflib.SequenceMatcher(None, aria_text, md_text)
diffs = []
for tag, i1, i2, j1, j2 in matcher.get_opcodes():
    if tag != "equal":
        diffs.append(f"--- ARIA ({i1}:{i2}) ---\n" + "\n".join(aria_text[i1:i2]) + f"\n+++ MD ({j1}:{j2}) +++\n" + "\n".join(md_text[j1:j2]) + "\n======================")

with open(r"C:\Users\quicp\OneDrive\Desktop\Novel\scratch_diff.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(diffs))

print(f"Found {len(diffs)} differences in Day 7.")
