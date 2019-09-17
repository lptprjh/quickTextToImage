#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
from escpos.printer import Usb
import os,sys,usb,subprocess

class softunicode():
    def __init__(self, width):
        self.width = width

        #if font != '': self.font = ImageFont.load(font)
        #else: self.font = ImageFont.load('Arial')
        self.font = None
    
    def changeFont(self,font:str):
        if font[-3:].lower() in ('ttf', 'otf'):
            self.changeFontTTF(font)
        else:
            self.font = ImageFont.load(font)
        return self.font

    def changeFontTTF(self,font:str, size=10, index=0, encoding='', layout_engine=None):
        self.font = ImageFont.truetype(font,size=size, index=index,encoding=encoding,layout_engine=layout_engine)
        return self.font

    def text(self, text, fill=None, font=None, anchor=None, spacing=3, align="left", direction=None, features=None, language=None) -> None:
        canvas = Image.new('RGBA', (self.width,65536))
        draw = ImageDraw.Draw(canvas)
        
        if fill==None: fill = (0,0,0,255)
        if font==None: font = self.font
        wrappedText = self.__textwrap(draw,text,font,spacing)
        draw.text((0,0), wrappedText, \
            fill=fill, font=font, anchor=anchor, spacing=spacing, \
            align=align, direction=direction, features=features, language=language)
        
        wrappedTextSize = canvas.getbbox()
        if wrappedTextSize == None:
            return canvas.crop((0,0,self.width,draw.textsize('Abg', font=font, spacing=spacing)[1]))
        else:
            return canvas.crop((0,0,self.width,wrappedTextSize[3]))

    def __textwrap(self,draw,text,font,spacing=4) -> str:
        out = []
        line = []

        for c in text:
            if   c == '\r': continue
            elif c == '\n':
                line.append('\n')
                out.append(''.join(line))
                line.clear()
                continue
            else:
                line.append(c)
                if self.width < draw.textsize(''.join(line), font=font, spacing=spacing)[0]:
                    line[-1] = '\n'
                    out.append(''.join(line))
                    line.clear()
                    line.append(c)
        
        if len(line) != 0:
            line.append('\n')
            out.append(''.join(line))
        return ''.join(out)

def main():
    try: p = Usb(0x0416,0x5011)
    except usb.core.USBError as e:
        if e.errno == 13:
            print("Printing permission is required. (are you root?)")
            subprocess.call(['sudo', '/usr/bin/python3', *sys.argv])
            quit(1)
        else:
            print("Unknown Error about has catched during handling with USB Device. Program will closed.\n==========================")
            raise e
    
    tt = softunicode(350)
    tt.changeFontTTF('neodgm.ttf',size=32)

    try:
       while True:
           p.image(tt.text(input()), impl=u'bitImageColumn')
    finally:
        p.text("\n\n\n")
        p.close()

if __name__ == "__main__":
    main()
