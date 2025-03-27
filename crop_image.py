#!/usr/bin/env python3
"""
画像ファイルから指定された矩形領域を切り取り、指定サイズのRGBA形式のPNGとして保存するプログラム
使用方法:
    python crop_image.py input_image.jpg output_image.png left top width height [output_width output_height]
"""

import sys
import os
from PIL import Image

def crop_and_resize_image(input_path, output_path, left, top, width, height, output_width=None, output_height=None):
    """
    画像ファイルから指定された領域を切り取り、指定サイズのRGBA形式のPNGとして保存する

    Args:
        input_path (str): 入力画像のパス
        output_path (str): 出力画像のパス
        left (int): 切り取り開始位置の左からのピクセル数
        top (int): 切り取り開始位置の上からのピクセル数
        width (int): 切り取り領域の幅
        height (int): 切り取り領域の高さ
        output_width (int, optional): 出力画像の幅。Noneの場合はwidthと同じ
        output_height (int, optional): 出力画像の高さ。Noneの場合はheightと同じ
    """
    try:
        # 画像を開く
        with Image.open(input_path) as img:
            # 指定された矩形領域を切り取る
            crop_box = (left, top, left + width, top + height)
            cropped_img = img.crop(crop_box)

            # RGB or RGBA形式に変換
            if cropped_img.mode not in ('RGBA'):
                cropped_img = cropped_img.convert('RGBA')

            # 出力サイズを決定
            final_width = max(width, output_width) if output_width is not None else width
            final_height = max(height, output_height) if output_height is not None else height

            # サイズ変更が必要な場合は新しい透明な画像を作成して中央に配置
            if final_width > width or final_height > height:
                # 新しい透明な画像を作成
                new_img = Image.new('RGBA', (final_width, final_height), (0, 0, 0, 0))

                # 中央に配置するための座標を計算
                paste_x = (final_width - width) // 2
                paste_y = (final_height - height) // 2

                # 切り取った画像を中央に配置
                new_img.paste(cropped_img, (paste_x, paste_y))

                # 最終的な画像を保存
                new_img.save(output_path, 'PNG')
            else:
                # 切り取った画像をそのまま保存
                cropped_img.save(output_path, 'PNG')

            print(f"画像を切り取り、{output_path}に保存しました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    # コマンドライン引数のチェック
    if len(sys.argv) not in [7, 9]:
        print("使用方法: python crop_image.py 入力画像 出力画像 左位置 上位置 幅 高さ [出力幅 出力高さ]", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    try:
        left = int(sys.argv[3])
        top = int(sys.argv[4])
        width = int(sys.argv[5])
        height = int(sys.argv[6])

        # オプションの出力サイズパラメータ
        output_width = int(sys.argv[7]) if len(sys.argv) >= 8 else None
        output_height = int(sys.argv[8]) if len(sys.argv) >= 9 else None

    except ValueError:
        print("位置と大きさのパラメータは整数で指定してください。", file=sys.stderr)
        sys.exit(1)

    # 入力ファイルの存在確認
    if not os.path.exists(input_path):
        print(f"入力ファイル '{input_path}' が見つかりません。", file=sys.stderr)
        sys.exit(1)

    # 画像の切り取りとリサイズ、保存
    crop_and_resize_image(input_path, output_path, left, top, width, height, output_width, output_height)

if __name__ == "__main__":
    main()
