import appuifw,graphics,powlite_fm,e32,sys,os

#系统路径
path=os.getcwd()
MPATH=path

img=graphics.Image.open(MPATH+"pic\\tianyou.png")
appuifw.app.screen="full"
appuifw.app.body=canvas=appuifw.Canvas()
(x,y)=canvas.size
canvas.blit(img,(0,0,174,34),((x-174)/2,(y-34)/2,(x+174)/2,(y+34)/2))
e32.ao_sleep(0.001)

from hack import*
from screenshot import ScreenShot
from mf import Mf
from zip import Zip
from codeviewer import word_view
from han import Han
from search import Search

PATH="e:/data/tengge/"
title=u"Javatool"
TEXT="""名称：Java精灵v2.0.0
作者：tengge（李腾）
QQ：930372551
天游智能欢迎您！

""".decode("u8")
t=appuifw.Text(TEXT)

if not os.path.exists(PATH):
    os.makedirs(PATH)

def cn(x):return x.decode("u8")
def exit():
    if appuifw.query(cn("要退出吗？"),"query"):
        sys.exit()

manager=powlite_fm.manager()
handler=exit

def help():
    list=os.listdir(MPATH+"\\help\\")
    list2=map(lambda x:x.decode("u8"),list)
    index=appuifw.popup_menu(list2,cn("帮助文档"))
    if index!=None:
        f=open(MPATH+"\\help\\"+list[index])
        t.clear()
        d=f.read().decode("u8")
        f.close()
        t.set(d)
        t.set_pos(0)

def set():#设置
    f=open(MPATH+"settings\\settings.ini","rb")
    d=f.read()
    f.close()
    d1=int(d[0].encode("hex"),16)
    d2=int(d[1].encode("hex"),16)
    d3=int(d[2].encode("hex"),16)
    list0=(cn("压缩方式"),"combo",([cn("不压缩"),cn("压缩")],d1))
    list1=(cn("添加号码"),"combo",([cn("10086"),cn("10010"),cn("00000000")],d2))
    list2=(cn("智能过滤"),"combo",([cn("关闭"),cn("开启")],d3))
    form=appuifw.Form([list0,list1,list2],appuifw.FFormEditModeOnly|appuifw.FFormDoubleSpaced)
    form.execute()
    f=open(MPATH+"\\settings\\settings.ini","wb")
    f.write(("0"+str(form[0][2][1])+"0"+str(form[1][2][1])+"0"+str(form[2][2][1])).decode("hex"))
    f.close()
    appuifw.note(cn("设置成功！"),"conf")

def about():
    appuifw.note(cn("tengge作品！"))

class JavatoolMain(object):
    #属性
    PATH=PATH
    MPATH=MPATH
    TEXT=TEXT
    title=title
    t=t
    manager=manager
    
    def __init__(self):
        self.cn=cn
        self.handler=exit
        self.about=about
        self.menu=[\
            (cn("一键破解"),(\
                (cn("简单破解"),self.simplehack),\
                (cn("深度破解"),self.deephack))),\
            (cn("极速汉化"),self.quickhandir),\
            (cn("编辑MF文件"),self.editmf),\
            (cn("压缩解压"),(\
                (cn("压缩jar文件"),self.zipfile),\
                (cn("解压jar文件"),self.unzipfile))),\
            (cn("常用工具"),(\
                (cn("查找信息"),self.search),\
                (cn("汉字编码"),self.codeviewer),\
                (cn("屏幕截图"),self.screenshot))),\
            (cn("其他功能"),(\
                (cn("清空屏幕"),self.clearscreen),\
                (cn("清空缓存"),self.deletefile),\
                (cn("程序设置"),set),\
                (cn("使用帮助"),help),\
                (cn("软件关于"),about))),\
            (self.cn("退出程序"),self.handler)]
        
        #初始化界面
        appuifw.app.title=self.title
        appuifw.app.body=self.t
        appuifw.app.menu=self.menu
        appuifw.app.exit_key_handler=self.handler
        self.t.bind(63557,lambda:self.add("\n"))
    
    def add(self,item):
        try:
            self.t.add(cn(item)+"\n")
        except:
            self.t.add(item+"\n")
    def simplehack(self):
        SimpleHack(self)
    def deephack(self):
        DeepHack(self)
    def quickhandir(self):
        Han(self)
    def editmf(self):
        Mf(self)
    def zipfile(self):
        Zip(self).zip()
    def unzipfile(self):
        Zip(self).unzip()
    def clearscreen(self):
        self.t.clear()
    def deletefile(self):
        appuifw.note(cn("请手动清空e:\\data\\tengge文件夹"))
    def codeviewer(self):
        word_view(self.t)
    def screenshot(self):
        ScreenShot(self)
    def search(self):
        Search(self)

appuifw.app.screen="normal"
JavatoolMain()
