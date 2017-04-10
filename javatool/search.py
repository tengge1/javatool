import appuifw,os

class Search(object):
    def __init__(self,super):
        self.cn=super.cn
        self.manager=super.manager
        self.add=super.add
        self.result=[]
        
        self.index=appuifw.popup_menu([self.cn("Utf8编码"),self.cn("十六进制")])
        if self.index!=None:
            self.path=self.manager.AskUser("e:\\data\\tengge\\","dir")
            if self.path:
                self.path=self.path.encode("u8")
                self.word=appuifw.query(self.cn("输入查找内容："),"text")
                if self.word:
                    os.path.walk(self.path,self.walk,None)
                    self.show()
            
    def walk(self,x,path,list):
        if not path.endswith("\\"):
            path+="\\"
        for i in list:
            p=path+i
            if os.path.isfile(p) and p.endswith(".class"):
                self.add("正在查找"+i)
                pos=-1
                f=open(p,"rb")
                if self.index==0:
                    pos=f.read().find(self.word.encode("u8"))
                else:
                    pos=f.read().encode("hex").find(self.word.encode("u8"))
                f.close()
                if pos!=-1:
                    self.result.append((p,pos))
                    
    def show(self):
        if self.result==[]:
            self.add("未找到相关信息")
        else:
            self.add(self.word.encode("u8")+"查找结果：")
            for i in self.result:
                self.add(i[0].replace(self.path,"")+"  位置："+str(i[1]))
