#!/usr/bin/env python3
"""
JSONファイルから矩形情報を読み込み、画像に矩形を描画して保存するプログラム
使用方法:
    python draw_rectangles.py input_image.jpg rectangles.json output_image.png
"""

import sys
import os
import json
import argparse
from PIL import Image, ImageDraw, ImageFont

def draw_rectangles(input_path, json_path, output_path, font_size=20, color="red", with_label=False):
    """
    JSONファイルから矩形情報を読み込み、画像に矩形を描画して保存する

    Args:
        input_path (str): 入力画像のパス
        json_path (str): 矩形情報を含むJSONファイルのパス
        output_path (str): 出力画像のパス
        font_size (int): フォントサイズ（デフォルト: 20）
        color (str): 矩形とラベルの色（デフォルト: "red"）
        with_label (bool): ラベルを描画するかどうか（デフォルト: False）
    """
    try:
        # 画像を開く
        with Image.open(input_path) as img:
            # 編集用に画像をコピー
            img = img.copy()

            # 描画オブジェクトを作成
            draw = ImageDraw.Draw(img)

            # JSONファイルを読み込む
            with open(json_path, 'r', encoding='utf-8') as f:
                rectangles = json.load(f)

            # フォントの設定（可能であればシステムフォントを使用）
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
            except IOError:
                # フォントが見つからない場合はデフォルトフォントを使用
                print("警告: DejaVuSansフォントが見つかりません。デフォルトフォントを使用します。", file=sys.stderr)
                font = ImageFont.load_default()

            # 各矩形を描画
            for rect in rectangles:
                # 矩形情報を取得
                top = rect.get('top', 0)
                left = rect.get('left', 0)
                width = rect.get('width', 0)
                height = rect.get('height', 0)
                label = rect.get('label', '')

                # 矩形の座標を計算
                box = [left, top, left + width, top + height]

                # 矩形を描画（枠線のみ）
                draw.rectangle(box, outline=color, width=1)

                # ラベルのテキストを描画（矩形の上部に）
                if with_label and label:
                    # ラベルの背景用の矩形を描画
                    text_width, text_height = draw.textbbox((0, 0), label, font=font)[2:]
                    draw.rectangle([left, top - text_height - 4, left + text_width + 4, top],
                                  fill=color)
                    # ラベルテキストを描画
                    draw.text((left + 2, top - text_height - 2), label, fill="white", font=font)

            # 画像を保存
            img.save(output_path, 'PNG')
            print(f"矩形を描画し、{output_path}に保存しました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    # コマンドライン引数の設定
    parser = argparse.ArgumentParser(
        description='JSONファイルから矩形情報を読み込み、画像に矩形を描画して保存するプログラム'
    )
    parser.add_argument('input_image', help='入力画像のパス')
    parser.add_argument('json_file', help='矩形情報を含むJSONファイルのパス')
    parser.add_argument('output_image', help='出力画像のパス')
    parser.add_argument('--font-size', type=int, default=20, help='フォントサイズ（デフォルト: 20）')
    parser.add_argument('--color', default='red', help='矩形とラベルの色（デフォルト: red）')
    parser.add_argument('--with-label', action='store_true', help='ラベルを描画する')

    args = parser.parse_args()

    # 入力ファイルの存在確認
    if not os.path.exists(args.input_image):
        print(f"入力画像ファイル '{args.input_image}' が見つかりません。", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.json_file):
        print(f"JSONファイル '{args.json_file}' が見つかりません。", file=sys.stderr)
        sys.exit(1)

    # 矩形の描画と保存
    draw_rectangles(args.input_image, args.json_file, args.output_image, 
                   args.font_size, args.color, args.with_label)

if __name__ == "__main__":
    main()
