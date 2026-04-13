#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NScripter形式自動変換ツール
Markdown形式のシナリオファイルをNScripter形式に変換します
"""

import sys
import re

def convert_markdown_to_nscript(input_file, output_file):
    """
    MarkdownファイルをNScripter形式に変換します
    """

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    output_lines = []
    nvl_mode = False
    current_scene = None

    for i, line in enumerate(lines, 1):
        line = line.strip()

        # 空行とコメントをスキップ
        if not line or line.startswith('*') or line.startswith('#') or line.startswith(';'):
            output_lines.append(line)
            continue

        # シーン切り替え検出
        if line.startswith('---') or line.startswith('**'):
            # シーン切り替え
            output_lines.append(line)
            # シーン切り替えの後は自動的にADVモードへ
            nvl_mode = False
            current_scene = line
            continue

        # モード検出
        if line == 'nvl':
            output_lines.append('nvl')
            nvl_mode = True
            current_scene = None
        elif line == 'adv':
            output_lines.append('adv')
            nvl_mode = False

        # 背景切り替え検出
        bg_match = re.match(r'^bg\s+"([^"]+)"', line)

        if bg_match:
            output_lines.append(f'scenechange "bg/{bg_match.group(1)}", 2')
            nvl_mode = False
            continue

        # コマンド検出（wait, fadeout, quake）
        if line.startswith('wait ') or line.startswith('fadeout ') or line.startswith('quake ') or line.startswith('goto '):
            output_lines.append(line)
            continue

        # ターン検出
        if 'END' in line:
            output_lines.append('goto *end_day2')
            output_lines.append('scenechange "bg/bg_title.bmp", 2')
            output_lines.append('end')
            continue

        # ダイアログ検出：「名前」と「セリフ」
        dialogue_match = re.match(r'^(.+?)「(.+?)」', line)
        if dialogue_match:
            speaker = dialogue_match.group(1).strip()
            dialogue = dialogue_match.group(2).strip()
            # 「セリフ」形式に戻す
            dialogue_with_quotes = f'「{dialogue}」'

            # 元のセリフをそのまま維持
            if speaker == '俺':
                output_lines.append(f'talk "俺","{dialogue_with_quotes}"')
            elif speaker == 'ミオ':
                output_lines.append(f'talk "ミオ","{dialogue_with_quotes}"')
            else:
                output_lines.append(f'talk "{speaker}","{dialogue_with_quotes}"')
            continue

        # 叙述・描写行の処理（日本語を含む行）
        if re.match(r'^[一-龠あ-んア-ン]+$', line):
            # 叙述（漢字・ひらがな・カタカナ）
            output_lines.append(line)
            continue

        # 行末の記号処理
        if line.endswith('。'):
            output_lines.append(line)
        elif line.endswith('...'):
            output_lines.append(line)
        else:
            if nvl_mode:
                output_lines.append(line)
            else:
                output_lines.append(line)

    # 終了コードを追加
    output_lines.append('goto *end_day2')
    output_lines.append('scenechange "bg/bg_title.bmp", 2')
    output_lines.append('end')

    # 出力ファイルに書き込み
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    print(f'変換完了: {input_file} -> {output_file}')
    print(f'変換行数: {len(output_lines)}')

def main():
    if len(sys.argv) < 2:
        print('使用方法: python convert_md_to_nscript.py <入力ファイル> <出力ファイル>')
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else '03.txt'
        convert_markdown_to_nscript(input_file, output_file)

if __name__ == '__main__':
    main()
