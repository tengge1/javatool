import appuifw,os,zipfile

class Zip:
    def __init__(self,super):
        self.cn=super.cn
        self.add=super.add
        self.manager=super.manager
        self.clear=super.clearscreen
        self.compress=zipfile.ZIP_DEFLATED
        
    def unzip(self):
        path=self.manager.AskUser("","file",[".jar"])
        if path:
            path=path.encode("u8")
            self.add("开始解压…")
            path=path.replace("\\","/")
            name=path.split("/")[-1]
            if not os.path.exists("e:/data/tengge/"+name+"/"):
                os.makedirs("e:/data/tengge/"+name+"/")
            type=zipfile.ZipInfo().compress_type
            f=zipfile.ZipFile(path,"r",type)
            for i in f.namelist():
                p="e:/data/tengge/"+name+"/"+i
                if i.endswith("/"):
                    if not os.path.exists(path):
                        os.makedirs(path)
                else:
                    if i.find("/")!=-1:
                        temp="/".join(p.split("/")[:-1])
                        if not os.path.exists(temp):
                            os.makedirs(temp)
                    self.add("正在解压"+i)
                    file=open(p,"wb")
                    file.write(f.read(i))
                    file.close()
            f.close()
            self.add("解压完成…")
            appuifw.note(self.cn("解压完成！"),"conf")
            
    def zip(self):
        path=self.manager.AskUser("e:/data/tengge/","dir")
        if path:
            path=path.encode("u8")
            path=path.replace("\\","/")
            if not path.endswith("/"):
                path+="/"
            self.add("开始压缩…")
            self._zip(path)
            self.add("压缩完成！")
            if appuifw.query(self.cn("压缩完成，要安装吗？"),"query"):
                appuifw.Content_handler().open(("e:/data/"+path.split("/")[-2]).replace("/","\\").decode("u8"))

            appuifw.note(self.cn("压缩完成！"),"conf")
    
    def _zip(self,path):
        self.name=path.split("/")[-2]
        self.f=zipfile.ZipFile("e:/data/"+path.split("/")[-2],"w",self.compress)
        os.path.walk(path,self.walk,None)
        self.f.close()

    def walk(self,n,p,l):
        if not(p.endswith("/")):
            p+="/"
        l=map(lambda x:(p+x),l)
        for i in l:
            if os.path.isfile(i):
                self.add("正在添加"+i.replace("e:/data/tengge/"+self.name+"/",""))
                self.f.write(i,str(i.replace("e:/data/tengge/"+self.name+"/","")),self.compress)
                