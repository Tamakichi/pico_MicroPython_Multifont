# This is Japanese font library for MicroPython
# 2022/12/01 v1.00 by Tamakichi-San

import os
from tma_jp_utl import isHkana, hkana2kana, han2zen, binfind

# フォント管理クラス
class mfont:
    MFONT8  = 0    # 8ドット美咲フォント
    MFONT10 = 1    # 10ドット nagaフォント
    MFONT12 = 2    # 12ドット東雲フォント
    MFONT14 = 3    # 14ドット東雲フォント
    MFONT16 = 4    # 16ドット東雲フォント
    MFONT20 = 5    # 20ドットJiskanフォント
    MFONT24 = 6    # 24ドットXフォントト

    flgBegin = False
    path = ""

    # フォント種別テーブル

    finfo = (
        # name,     num  bytes  w   h
        ("u_4x8a",   191,  8,  4,  8) , # 0:u_4x8a.hex
        ("u_5x10a",  256, 10,  5, 10) , # 1:u_5x10a.hex
        ("u_6x12a",  256, 12,  6, 12) , # 2:u_6x12a.hex
        ("u_7x14a",  221, 14,  7, 14) , # 3:u_7x14a.hex
        ("u_8x16a",  221, 16,  8, 16) , # 4:u_8x16a.hex
        ("u_10x20a", 190, 40, 10, 20) , # 5:u_10x20a.hex
        ("u_12x24a", 221, 48, 12, 24) , # 6:u_12x24a.hex

        ("u_8x8",    6879,  8,  8,  8) , # 7:u_8x8.hex
        ("u_10x10",  6877, 20, 10, 10) , # 8:u_10x10.hex
        ("u_12x12",  6879, 24, 12, 12) , # 9:u_12x12.hex
        ("u_14x14",  6879, 28, 14, 14) , # 10:u_14x14.hex
        ("u_16x16",  6879, 32, 16, 16) , # 11:u_16x16.hex
        ("u_20x20",  6879, 60, 20, 20) , # 12:u_20x20.hex
        ("u_24x24",  6877, 72, 24, 24) , # 13:u_24x24.hex

    )

    def __init__(self,sz=16,path=""):
        self.setFontSize(sz)
        self.path=path

    def selectFont(self, no):
        self.font_no         = no + 7
        self.h_font_no       = no
        self.index_len       = self.finfo[self.font_no][1]
        self.filename        = self.finfo[self.font_no][0] + ".fnt"
        self.data_top_pos    = self.index_len*2
        self.font_bytes      = self.finfo[self.font_no][2]
        self.font_line_bytes = (self.finfo[self.font_no][3] + 7)>>3
        self.offset          = self.finfo[self.h_font_no][1]*(2+self.finfo[self.h_font_no][2]) # 全角文字データ先頭オフセット
        
        self.h_index_len       = self.finfo[self.h_font_no][1]
        self.h_data_top_pos    = self.h_index_len*2
        self.h_font_bytes      = self.finfo[self.h_font_no][2]
        self.h_font_line_bytes = (self.finfo[self.h_font_no][3] + 7)>>3
        self.h_offset          = 0
        self.flgZenkaku        = True
        
        # フォントファイルの開き直し
        if self.flgBegin:
            self.end()
            self.begin()
                
    # 利用サイズの設定
    def setFontSize(self, sz):
      if sz < 10:
        self.selectFont(self.MFONT8)
      elif sz < 12:
        self.selectFont(self.MFONT10) 
      elif sz < 14:
        self.selectFont(self.MFONT12)
      elif sz < 16:
        self.selectFont(self.MFONT14)
      elif sz < 20:
        self.selectFont(self.MFONT16)
      elif sz < 24:
        self.selectFont(self.MFONT20)
      else:
        self.selectFont(self.MFONT24)

    # 直前に取得したフォントの1行あたりのフォントデータバイト数の取得
    def getRowLength(self):
        return self.font_line_bytes if self.flgZenkaku else self.h_font_line_bytes
    
    # 直前に取得したフォントのフォントの横ドット数の取得
    def getWidth(self):
        return self.finfo[self.font_no][3] if self.flgZenkaku else self.finfo[self.h_font_no][3]

    # 直前に取得したフォントのフォントの縦ドット数の取得
    def getHeight(self):
        return self.finfo[self.font_no][4] if self.flgZenkaku else self.finfo[self.h_font_no][4]

    # 直前に取得したフォントのデータバイト数の取得
    def len(self):
        return self.font_bytes if self.flgZenkaku else self.h_font_bytes
    
    # フォントデータ参照開始
    def begin(self):
        if self.flgBegin == False:
            self.f_r = open(self.path+self.filename, "rb")
            self.flgBegin = True

    # フォントデータ参照終了
    def end(self):
        if self.flgBegin:
            self.f_r.close()
            self.flgBegin = False

    # インデックスファイルの検索
    def find(self, code, index_size, offset):
        if not self.flgBegin:
           return -1 
        
        def get_at(pos):
            self.f_r.seek(pos*2+offset)
            d = int.from_bytes(self.f_r.read(2),"big")
            return d
        return binfind(code, index_size, get_at)

    # 指定した位置の取得
    def get_fontdata(self, pos, font_bytes, offset):
        if not self.flgBegin:
           return []
        self.f_r.seek(pos+offset)
        font_data = [int(d) for d in self.f_r.read(font_bytes)]
        return font_data

    # フォントデータの取得
    def getFont(self, code):
        # 文字コードの変更(＼￠￡￢)
        c = { 0xFF3C:0x5C, 0xFFE0:0xA2, 0xFFE1:0xA3, 0xFFE2:0xAC }.get(code)
        if c != None:
            code = c
        if code < 0x100:
            self.flgZenkaku = True if code in (0x5C,0xA2,0xA3,0xA7,0xA8,0xAC,0xB0,0xB1,0xB4,0xB6,0xD7,0xF7) else False
        else:
            self.flgZenkaku = True
            if isHkana(code):
                code = hkana2kana(code)
        if self.flgZenkaku:
            index = self.find(code, self.index_len, self.offset)
            pos = index*self.font_bytes + self.data_top_pos
            font = self.get_fontdata(pos, self.font_bytes, self.offset)                
        else:
            index = self.find(code, self.h_index_len, self.h_offset)
            pos = index*self.h_font_bytes + self.h_data_top_pos
            font = self.get_fontdata(pos, self.h_font_bytes, self.h_offset)                            
        return font
