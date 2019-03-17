# -*- coding: utf-8 -*-
from ctypes import WinDLL, c_char_p, c_int, c_wchar_p
from ctypes.wintypes import BOOL
from flask import Flask, request
from gevent.pywsgi import WSGIServer
import re

app = Flask(__name__)

class TransEngine:
    def initialize(self, engine):
        self.start = engine.J2K_InitializeEx
        self.start.argtypes = [c_char_p, c_char_p]
        self.start.restype = BOOL

        self.trans = engine.J2K_TranslateMMNTW
        self.trans.argtypes = [c_int, c_wchar_p]
        self.trans.restype = c_wchar_p

        self.start_obj = self.start(b"CSUSER123455", b"C:\Program Files (x86)\ChangShinSoft\ezTrans XP\Dat")
    def translate_j2k(self, src_text):
        trans_obj = self.trans(0, src_text)
        return trans_obj
        
eng = TransEngine()

def decode_text(txt):
    chars = "↔◁◀▷▶♤♠♡♥♧♣⊙◈▣◐◑▒▤▥▨▧▦▩♨☏☎☜☞↕↗↙↖↘♩♬㉿㈜㏇™㏂㏘＂＇∼ˇ˘˝¡˚˙˛¿ː∏￦℉€㎕㎖㎗ℓ㎘㎣㎤㎥㎦㎙㎚㎛㎟㎠㎢㏊㎍㏏㎈㎉㏈㎧㎨㎰㎱㎲㎳㎴㎵㎶㎷㎸㎀㎁㎂㎃㎄㎺㎻㎼㎽㎾㎿㎐㎑㎒㎓㎔Ω㏀㏁㎊㎋㎌㏖㏅㎭㎮㎯㏛㎩㎪㎫㎬㏝㏐㏓㏃㏉㏜㏆┒┑┚┙┖┕┎┍┞┟┡┢┦┧┪┭┮┵┶┹┺┽┾╀╁╃╄╅╆╇╈╉╊┱┲ⅰⅱⅲⅳⅴⅵⅶⅷⅸⅹ½⅓⅔¼¾⅛⅜⅝⅞ⁿ₁₂₃₄ŊđĦĲĿŁŒŦħıĳĸŀłœŧŋŉ㉠㉡㉢㉣㉤㉥㉦㉧㉨㉩㉪㉫㉬㉭㉮㉯㉰㉱㉲㉳㉴㉵㉶㉷㉸㉹㉺㉻㈀㈁㈂㈃㈄㈅㈆㈇㈈㈉㈊㈋㈌㈍㈎㈏㈐㈑㈒㈓㈔㈕㈖㈗㈘㈙㈚㈛ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⒜⒝⒞⒟⒠⒡⒢⒣⒤⒥⒦⒧⒨⒩⒪⒫⒬⒭⒮⒯⒰⒱⒲⒳⒴⒵⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽⑾⑿⒀⒁⒂"
    for c in chars:
        if c in txt:
            txt = txt.replace(c,"\\u" + str(hex(ord(c)))[2:])
    return txt

def encode_text(txt):
    return re.sub(r'(?i)(?<!\\)(?:\\\\)*\\u([0-9a-f]{4})', lambda m: chr(int(m.group(1), 16)), txt)

def main():
    engine_object = WinDLL('C:\Program Files (x86)\ChangShinSoft\ezTrans XP\J2KEngineH.dll')
    eng.initialize(engine_object)
    
    http_server = WSGIServer(('127.0.0.1', 5000), app)
    http_server.serve_forever()
    
    #app.run()

@app.route("/")
def home():
    return "ezTranslator J2K Web Wrapper"

@app.route("/translate")
def webtranslate():
    src_text = request.args.get('text')
    return encode_text(eng.translate_j2k(decode_text(src_text)))

if __name__ == '__main__':
    main()