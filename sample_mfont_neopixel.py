"""
Neopixel 16x16ドットマトリックス マルチフォントライブラリ テスト表示デモ

"""
from machine import Pin
from neopixel import NeoPixel
import time
from random import randint
from neomatrix import NeoMatrix
from mfont import mfont

pin = 26
matrix_w = 16
matrix_h = 16
bright = 50

# ビットパターン表示
# d: 8ビットパターンデータ
def bitdisp(d):
    for i in range(8):
        if d & 0x80>>i:
            print("##",end="")
        else:
            print("  ",end="")

# フォントデータの表示
# font : フォントデータ（リスト）
# bn:横バイト数
def fontdump(font,bn):
    for i in range(0,len(font),bn):
        for j in range(bn):
            bitdisp(font[i+j])
        print()
    print()
    
# 指定位置のドットの取得
def dotAt(font, lb, x, y):
    return font[lb*y+x//8] & (0x80>>(x%8)) > 0

# 1文字左スクロール挿入
def scrollIn(np, fnt, color, tm, ypos=0, fw=16, fh=16):
    lb = (fw+7)>>3 # 1行あたりのフォントバイト数
    for x in range(0,fw):
        np.scroll()
        # フォントパターン1列分のセット
        for y in range(0,fh):
            if dotAt(fnt,lb,x,y):
                 np.pixcel(matrix_w-1,ypos+y, color)
            else:
                 np.pixcel(matrix_w-1,ypos+y, (0,0,0))            
        np.update()
        time.sleep_ms(tm)

# フォントの配置
def putAt(np,font,w,h,x,y,fc,bc,flg=True):
    bn = (w+7)>>3 # 1行あたりのフォントバイト数
    for py in range(h):
        if py+y >= matrix_h:
            break
        for px in range(w):
            if px+x >= matrix_w:
                break
            d = dotAt(font, bn, px, py)
            if d:
               np.pixcel(px,py,fc)
            else:
               if bc != None: # Noneの場合、透明色扱い
                  np.pixcel(px,py,bc)
    if flg:
        np.update()

str="こんにちは世界！、こんにちは埼玉！"  
mf = mfont()
mf.setFontSize(8)
np = NeoMatrix(pin,matrix_w,matrix_h)
np.cls(True)

mf.begin()
fc=(0,0,20)
bc=(0,0,0)

#for sz in (8,10,12,14,16,):
for sz in (14,):
#while True:
    mf.setFontSize(sz)
    for c in str:
        #sz = (8,10,12,14,16)[randint(0,4)]
        #mf.setFontSize(sz)
        code = ord(c)
        font = mf.getFont(code)
        scrollIn(np,font,fc,10,(16-mf.getHeight())//2 ,mf.getWidth(),mf.getHeight())
        #putAt(np, font, mf.getWidth(), mf.getHeight(),0,0,fc,bc)
        #time.sleep_ms(300)
        #np.cls()
    time.sleep_ms(1000)
    np.cls(True)

