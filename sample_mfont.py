# コンソールに漢字を表示するサンプルプログラム
from mfont import mfont

# 定数
MY_FONT_SIZE = 16  # 使用するフォントサイズ

# フォントデータの表示
# font : フォントデータ（リスト）
# w:横ドット数
def fontdump(font, w):
    bn = (w+7)>>3
    for i in range(0, len(font), bn):
        for j in range(bn):
            for k in range(8 if (j+1)*8 <=w else w % 8):
                print("##" if font[i+j] & 0x80>>k else "  ",end="")
        print()
    print()    

s="こんにちは世界！、こんにちは埼玉！"
mf = mfont(MY_FONT_SIZE)
mf.begin()
for c in s:
    code = ord(c)
    font = mf.getFont(code)
    print(hex(code), ":", mf.getWidth(), "x", mf.getHeight())
    fontdump(font, mf.getWidth())
mf.end()
