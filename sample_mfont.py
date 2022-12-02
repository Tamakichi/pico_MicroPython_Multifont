import os
from tma_jp_utl import isHkana, hkana2kana, han2zen, binfind
from random import randint
from mfont import mfont

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

s="こんにちは世界！、こんにちは埼玉！"
mf = mfont(16)
mf.begin()
for c in s:
    code = ord(c)
    font = mf.getFont(code)
    lb = mf.getRowLength()
    print(hex(code),":",mf.getWidth(),"x",mf.getHeight())
    fontdump(font, lb)
mf.end()
