import appuifw,os

class Han(object):
    file=None#当前文件路径
    path=None#当前汉化路径
    file_list=[]#文件路径列表
    is_class=1#是否是文件列表
    index=0#光标当前位置
    file_index=0#文件列表当前位置
    lang_index=0#可汉化当前位置
    size={1:0,3:5,4:5,5:9,6:9,7:3,8:3,9:5,10:5,11:5,12:5}#常量池结构长度
    isize={1:1,3:1,4:1,5:2,6:2,7:1,8:1,9:1,10:1,11:1,12:1}#占常量池长度
    changed=0#是否被改变
    less=0#是否开启过滤

    def __init__(self,super):
        self.cn=super.cn
        self.title=super.title
        self.t=super.t
        self.menu=super.menu
        self.handler=super.handler
        self.manager=super.manager
        self.path=self.manager.AskUser("e://data//tengge//","dir")
        if self.path:
            self.path=self.path.encode("u8")
            os.path.walk(self.path,self.walk,None)
            if self.file_list==[]:
                appuifw.note(self.cn("该目录下未找到class文件！"),"error")
            else:
                appuifw.app.title=self.cn("极速汉化")
                appuifw.app.menu=[(self.cn("智能过滤"),((self.cn("开启"),lambda:self.set(1)),(self.cn("关闭"),lambda:self.set(0)))),(self.cn("返回"),self.quit)]
                appuifw.app.exit_key_handler=self.quit
                self.list=map(lambda x:unicode(x.split("\\")[-1]),self.file_list)
                self.alist()

    def walk(self,n,path,list):
        if not path.endswith("\\"):
            path+="\\"
        for i in list:
            if i.endswith(".class"):
                self.file_list.append(path+i.encode("u8"))

    def alist(self):
        appuifw.app.body=self.listbox=appuifw.Listbox(self.list,self.press)
        self.listbox.set_list(self.list,self.index)
        self.listbox.bind(63495,self.backward)
        self.listbox.bind(63496,self.forward)
        self.listbox.bind(42,self.former)
        self.listbox.bind(35,self.latter)
        
    def forward(self):
        if self.is_class==1:
            self.file_index=self.listbox.current()
            self.file=self.file_list[self.file_index]
            file=open(self.file,"rb")
            self.data=file.read()
            file.close()
            self.search()
            if self.lang_list==[]:
                appuifw.note(self.cn("未找到可汉化资源！"),"error")
            else:
                self.is_class=0
                self.lang_index=0
                self.index=0
                self.changed=0
                self.list=map(lambda x:x[2],self.lang_list)
                self.alist()
                
    def search(self):
        count=int(self.data[8:10].encode("hex"),16)
        self.lang_list=[]
        start=10
        index=1
        while index<=count-1:
            tag=int(self.data[start:start+1].encode("hex"),16)
            if tag==1:
                length=int(self.data[start+1:start+3].encode("hex"),16)
                try:
                    item=self.data[start+3:start+3+length].decode("u8")
                    if self.choose(item):
                        self.lang_list.append((start,length,item))
                except:
                    pass
                start+=3+length
                index+=1
            else:
                start+=self.size[tag]
                index+=self.isize[tag]
    
    def choose(self,item):
        if self.less==0:
            return 1
        elif (item.find(u"/")==-1) and (item.find(u"(")==-1) and (item.find(u"[")==-1) and (item.find(u"StackMap")==-1) and (item.find(u"<")==-1) and (len(item)>2):
            return 1
        else:
            return 0
    
    def backward(self):
        if self.is_class==0:
            self.save()
            self.is_class=1
            self.index=self.file_index
            self.list=map(lambda x:unicode(x.split("\\")[-1]),self.file_list)
            self.alist()
            
    def press(self):
        if self.is_class!=1:
            self.han()
        else:
            appuifw.note(self.cn("按右方向键列出可汉化内容后再汉化！"))

    def han(self):
        self.index=self.lang_index=self.listbox.current()
        (start,old_length,content)=self.lang_list[self.index]
        new=appuifw.query(self.cn("请输入新内容："),"text",content)
        if new:
            new=new.encode("u8")
            new_length=hex(len(new))[2:]
            new_length=("0"*(4-len(new_length))+new_length).decode("hex")
            self.data=self.data[:start+1]+new_length+new+self.data[start+3+old_length:]
            self.changed=1
            self.search()
            self.list=map(lambda x:x[2],self.lang_list)
            self.alist()
            
    def save(self):
        if self.changed==1:
            if appuifw.query(self.cn("要保存吗？"),"query"):
                file=open(self.file,"wb")
                file.write(self.data)
                file.close()
                appuifw.note(self.cn("保存成功！"),"conf")
            
    def set(self,x):
        if x==1:
            self.less=1
            appuifw.note(self.cn("智能过滤已开启！"),"conf")
        else:
            self.less=0
            appuifw.note(self.cn("智能过滤已关闭！"),"conf")
    
    def former(self):#前一页
        self.index=self.listbox.current()
        if self.index>=8:
            self.index-=8
            self.alist()
        elif self.index<8 and self.index>1:
            self.index=0
            self.alist()
        
    def latter(self):#下一页
        self.index=self.listbox.current()
        num=len(self.list)
        if self.index+8<=num:
            self.index+=8
            self.alist()
        elif self.index+8>num and self.index!=num:
            self.index=num
            self.alist()
            
    def quit(self):
        if appuifw.query(self.cn("要返回吗？"),"query"):
            appuifw.app.title=self.title
            appuifw.app.body=self.t
            appuifw.app.menu=self.menu
            appuifw.app.exit_key_handler=self.handler
        