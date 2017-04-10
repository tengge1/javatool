'''
作者：tengge
QQ:930372551


'''
import appuifw
import base64

code=["unicode","utf8","utf7","utf16","gbk","big5","ascii","utf8_base64","gbk_base64","aliases","cp1251","cp866","iso8859_5","koi8_r","utf_16_be","utf_16_le","uu_codec","latin_1","koi8_u"]


def cn(x):return x.decode("u8")

def translator(x,code):
    if code=="unicode":
        x=eval(repr(x).replace("\\u","\\\\u"))
    elif code=="ascii":
        y=str(eval(repr(x).replace("\\u","")))
        i=0
        z=""
        while i<len(y):
            z+="\\x"+y[i+2:i+4]
            z+="\\x"+y[i:i+2]
            i+=4
        x=z
    elif code=="utf8_base64":
        x=eval(repr(self.encodestring(x.encode("utf8"))).replace("\\n","\\\\n"))
    elif code=="gbk_base64":
        x=eval(repr(self.encodestring(x.encode("gbk"))).replace("\\n","\\\\n"))
    else:
        x=eval(repr(x.encode(code)).replace("\\x","\\\\x"))
    return x
        
def word_view(t):
    x=appuifw.query(cn("请输入汉字："),"text")
    if x:
        t.clear()
        t.add(cn("下面是“")+x+cn("”的各种编码：\n"))
        for i in code:
            try:
                t.add(cn("\n")+unicode(i)+cn("码：")+unicode(translator(x,i)))
            except:
                pass
        try:
            t.add(cn("\nutf8_hex码：")+unicode(x.encode("utf8").encode("hex")))
        except:
            pass
        try:
            t.add(cn("\ngbk_hex码：")+unicode(x.encode("gbk").encode("hex")))
        except:
            pass
        t.set_pos(0)   

