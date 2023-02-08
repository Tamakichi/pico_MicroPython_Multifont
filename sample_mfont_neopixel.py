# Neopixel 16x16ドットマトリックス マルチフォントライブラリ テスト表示デモ
from micropython import const
from machine import Pin
from time import sleep_ms
from mfont import mfont
from device.neomatrix import NeoMatrix

# 定数(デフォルトは、Seeed XIAO RP2040用)
MY_FONT_SIZE = const(12)       # 使用するフォントサイズ(8,10,12,14,16,20,24)
DIN_PIN      = const(26)       # Neopixcel データピン
MATRIX_W     = const(16)       # Neopixcel 横ドット数
MATRIX_H     = const(16)       # Neopixcel 縦ドット数
FD_COLOR     = const((0,0,20)) # 前景色
BK_COLOR     = const((0,0,0))  # 背景色

# 指定位置のドットの取得
def dotAt(font, lb, x, y):
    return font[lb*y+x//8] & (0x80>>(x%8)) > 0

# 1文字左スクロール挿入
def scrollIn(np, fnt, fc, bc, tm, ypos=0, fw=16, fh=16):
    lb = (fw+7)>>3 # 1行あたりのフォントバイト数
    for x in range(0, fw):
        np.scroll()
        # フォントパターン1列分のセット
        for y in range(0, fh):
            np.pixcel(MATRIX_W-1, ypos+y, fc if dotAt(fnt, lb, x, y) else bc)
        np.update()
        sleep_ms(tm)

# フォントの配置
def putAt(np, font, w, h, x, y,fc, bc, flg=True):
    bn = (w+7)>>3 # 1行あたりのフォントバイト数
    for py in range(h):
        if py+y >= matrix_h:
            break
        for px in range(w):
            if px+x >= matrix_w:
                break
            if dotAt(font, bn, px, py):
               np.pixcel(px, py, fc)
            else:
               if bc != None: # Noneの場合、透明色扱い
                  np.pixcel(px, py, bc)
    if flg:
        np.update()

str="こんにちは世界！、こんにちは埼玉！"  
mf = mfont()
mf.setFontSize(MY_FONT_SIZE)
np = NeoMatrix(DIN_PIN, MATRIX_W, MATRIX_H)
np.cls(True)
mf.begin()

while True:
    for c in str:
        font = mf.getFont(ord(c))
        scrollIn(np, font, FD_COLOR, BK_COLOR, 10, (MATRIX_H-mf.getHeight())//2 ,mf.getWidth(), mf.getHeight())
    sleep_ms(1000)
    np.cls(True)

