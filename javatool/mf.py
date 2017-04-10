import appuifw

class Mf(object):
    def __init__(self,super):
        self.cn=super.cn
        self.t=super.t
        self.MPATH=super.MPATH
        self.clear=super.clearscreen
        self.manager=super.manager
        self.menu=super.menu
        self.title=super.title
        self.handler=super.handler
        self.t.bind(63557,lambda:self.t.add(u"\n"))
        
        self.path=self.choose()
        if self.path:
            self.path=self.path.encode("u8")
            appuifw.app.menu=[\
                (self.cn("插入"),(\
                    (self.cn("小屏改中屏"),self.insert1),\
                    (self.cn("中屏改小屏"),self.insert2),\
                    (self.cn("RMS BT制作"),self.insert3))),\
                (self.cn("保存"),self.save),\
                (self.cn("返回"),self.quit)]
            appuifw.app.exit_key_handler=self.quit
            appuifw.app.title=self.cn("编辑MF文件")
            f=open(self.path)
            self.t.set(f.read().decode("u8"))
            f.close()

    def choose(self):
        return self.manager.AskUser("e:\\data\\tengge\\","file",[".mf"])
    
    def insert1(self):
        self.t.add(self.cn("Nokia-MIDlet-Original-Display-Size: 176,208\nNokia-MIDlet-Target-Display-Size: 240,320"))
        
    def insert2(self):
        self.t.add(self.cn("Nokia-MIDlet-Original-Display-Size: 240,320\nNokia-MIDlet-Target-Display-Size: 176,208"))
        
    def insert3(self):
        self.t.add(self.cn("MIDlet-2: BT修改,, RMSBackup\nRMSBackup-path: /e:/others/"))
        f=open(self.MPATH+"\\class\\RMSBackup.class")
        d=f.read()
        f.close()
        f=open(self.path[:-20]+"RMSBackup.class","wb")
        f.write(d)
        f.close()

    def save(self):
        try:
            f=open(self.path,"w")
            f.write(self.t.get().encode("u8").replace('\xe2\x80\xa9',"\r\n"))
            f.close()
            appuifw.note(self.cn("保存成功！"),"conf")
        except:
            appuifw.note(self.cn("无法保存文件！"),"error")
    def quit(self):
        if appuifw.query(self.cn("要返回吗？"),"query"):
            self._quit()
    def _quit(self):
        appuifw.app.title=self.title
        appuifw.app.menu=self.menu
        appuifw.app.exit_key_handler=self.handler
        self.t.clear()
