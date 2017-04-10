'''
作者：tengge
QQ:930372551

'''


import appuifw
import keycapture
import graphics
import os

class ScreenShot(object):
    def __init__(self,super):
        self.cn=super.cn
        self.menu=super.menu
        self.clear=super.clearscreen
        self.add=super.add
        
        self.capture=keycapture.KeyCapturer(self.press)
        self.capture.keys=[63586]
        
        appuifw.app.menu=[(self.cn("停止截图"),self.stop)]
        self.clear()
        self.add("将本软件转入后台，按拨号键截图，在本软件菜单中停止截图。")
        
        self.start()
    def press(self,key):
        if key==63586:
            img=graphics.screenshot()
            num=1
            path=""
            while True:
                path="e:\\Images\\Screenshot"+str(num)+".jpg"
                if not os.path.exists(path):
                    break
                num+=1
            img.save(path)
            appuifw.note(("另存为"+path).decode("u8"),"conf",1)
    def start(self):
        self.capture.start()
    def stop(self):
        self.capture.stop()
        appuifw.app.menu=self.menu
        self.clear()
