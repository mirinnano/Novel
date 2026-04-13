#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob

def convert_utf8_to_sjis(input_file, delete_original=True):
    """UTF-8ファイルをShift-JISに変換して保存"""
    try:
        # UTF-8で読み込む
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 出力ファイル名を生成
        output_file = input_file.replace('.txt', '_sjis.txt')

        # Shift-JISで書き込む
        with open(output_file, 'w', encoding='shift_jis', errors='replace') as f:
            f.write(content)

        print(f"変換完了: {input_file} -> {output_file}")

        # 元のファイルを削除
        if delete_original and os.path.exists(input_file):
            os.remove(input_file)
            print(f"削除完了: {input_file}")

        return True
    except Exception as e:
        print(f"エラー: {e}")
        return False

if __name__ == "__main__":
    # すべての.txtファイルを変換（debug_、main_、0_ で始まるファイル）
    patterns = ['debug_*.txt', 'main_*.txt', '0_*.txt']

    for pattern in patterns:
        files = glob.glob(pattern)
        for file in files:
            # 既に_sjisが含まれているファイルはスキップ
            if '_sjis.txt' not in file:
                convert_utf8_to_sjis(file)
