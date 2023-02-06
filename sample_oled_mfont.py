# Raspberry Pi Pico MicroPython OLEDディスプレイ フォント表示テストプログラム v2.0
# 利用OLEDディスプレイ: ssd13006 128x64ドット(I2C接続タイプ)

from machine import Pin, I2C
from micropython import const
import time
from device.ssd1306 import SSD1306_I2C
from mfont import mfont

# 定数(デフォルトは、Seeed XIAO RP2040用)
I2C_ID       = const(1)       # I2C ID
I2C_FREQ     = const(400_000) # I2C バス速度
OLED_WIDTH   = const(128)     # OLEDの横ドット数
OLED_HEIGHT  = const(64)      # OLEDの縦ドット数
OLED_ADDR    = const(0x3c)    # OLEDのI2Cアドレス
OLED_SCL     = const(7)       # OLEDのSCLピン
OLED_SDA     = const(6)       # OLEDのSDAピン

# フォントの表示
def drawFont(self, font, x, y, w, h, flg=False):
    bn = (w+7)>>3
    py = y
    for i in range(0, len(font), bn):
        px = x
        for j in range(bn):
            for k in range(8 if (j+1)*8 <=w else w % 8):
                self.pixel(px+k,py, 1 if font[i+j] & 0x80>>k else 0) 
            px+=8
        py+=1
    if flg:
        self.show()

# 改行
def newLine(self):
    self.x=0
    if self.y+self.mf.fs*2 > OLED_HEIGHT:
        self.scroll(0, -self.mf.fs)
        self.fill_rect(0, self.y, OLED_WIDTH, OLED_HEIGHT-self.y, 0)
        self.show()
    else:
        self.y=self.y+self.mf.fs
    
# テキストの表示
def drawText(self, text, x, y, fs, wt=0):
    self.x = x
    self.y = y
    
    # フォントの設定
    self.mf = mfont(fs)
    self.mf.begin()

    # テキスト表示
    for c in text:
        if c == '\n': # 改行コードの処理
            self.newLine()
            continue
        code = ord(c) 
        font = self.mf.getFont(code)
        if self.x+self.mf.getWidth()>=OLED_WIDTH:
            self.newLine()
        self.drawFont(font, self.x, self.y, self.mf.getWidth(), self.mf.getHeight(), True)
        if wt:
            time.sleep_ms(wt)
        self.x+=self.mf.getWidth()
    self.mf.end()

# SSD1306_I2Cに漢字表示インスタンス・メソッドの追加
SSD1306_I2C.drawText = drawText
SSD1306_I2C.drawFont = drawFont
SSD1306_I2C.newLine  = newLine

# OLEDディスプレイのインスタンスの生成
i2c = I2C(I2C_ID, scl=Pin(OLED_SCL), sda=Pin(OLED_SDA), freq=I2C_FREQ)
oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c, addr=OLED_ADDR)
oled.contrast(255)
oled.invert(False)

# 表示用テキスト
txt = "吾輩は猫である。名前はまだ無い。"\
    "どこで生れたかとんと見当がつかぬ。"\
    "何でも薄暗いじめじめした所でﾆｬｰﾆｬｰ泣いていた事だけは記憶している。"

# テキストの表示
while True:
    for fsize in (20,16,14,12,10,8):
        oled.fill(0)
        oled.text(str(fsize)+"px font",0,0,1)
        oled.show()
        time.sleep(2)
        oled.fill(0)
        oled.drawText(txt, 0, 0, fsize, 50)
        time.sleep(2)
