import os

md_path = r"C:\Users\quicp\OneDrive\Desktop\Novel\src\08_day8.md"
out_path = r"C:\Users\quicp\OneDrive\Desktop\engine\src\AriaEngine\assets\scripts\scenario_09.aria"

with open(md_path, "r", encoding="utf-8") as f:
    lines = f.read().splitlines()

out_lines = []
out_lines.append("; converted from Novel source: 08_day8.md")
out_lines.append("*scenario_09")
out_lines.append("cls()")
out_lines.append("set_vflag in_scene, 1")
out_lines.append("set_sflag scenario_09_started, 1")
out_lines.append("set_pflag chapter_09, 1")
out_lines.append('chapter_card_fx("DAY 8", "帰路")')
out_lines.append('scenechange("japanese_room_morning", 2, "fade")')
out_lines.append("nvl")
out_lines.append("")

for line in lines:
    stripped = line.strip()
    if not stripped:
        out_lines.append("")
    else:
        # Check if it's a scene change or something in the markdown
        if stripped == "遠くで、汽笛が鳴る。":
            out_lines.append(stripped + "\\")
        elif stripped == "俺達は軽くなってきたカバンを背負い、本州行きの船へと乗り込む。":
            out_lines.append('scenechange("ferry_deck", 2, "fade")')
            out_lines.append(stripped + "\\")
        elif stripped == "船が島から離れるほど、霧は強まっていく。":
            out_lines.append('fx_fog()')
            out_lines.append(stripped + "\\")
        elif stripped == "俺は慎重に一歩一歩を歩む。":
            out_lines.append(stripped + "\\")
        elif stripped == "何度か躓きそうになりつつ、客室のドアを掴む。":
            out_lines.append(stripped + "\\")
            out_lines.append('scenechange("ferry_inside", 2, "fade")')
            out_lines.append('fx_reset()')
        elif stripped == "俺達はまた、本州へと戻ってきた。":
            out_lines.append('scenechange("train_station", 2, "fade")')
            out_lines.append(stripped + "\\")
        else:
            if stripped.startswith("俺「") or stripped.startswith("ミオ「") or stripped.startswith("老婆「"):
                # Make sure it ends with \ 
                out_lines.append(stripped + "\\")
            elif stripped == "...":
                out_lines.append("...\\")
            else:
                out_lines.append(stripped + "\\")

out_lines.append("")
out_lines.append("set_pflag chapter_09, 1")
out_lines.append("clear_vflag in_scene")
out_lines.append("fx_reset()")
out_lines.append("cls()")
out_lines.append("goto *chapter_select")
out_lines.append("")

with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines))

print("Done converting!")
