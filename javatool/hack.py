import appuifw
import zipfile

class Hack(object):
    hacked=0
    def __init__(self,super):
        self.cn=super.cn
        self.t=super.t
        self.add=super.add
        f=open(super.MPATH+"settings\\settings.ini","rb")
        d=int(f.read()[1].encode("hex"),16)
        f.close()
        if d==0:
            self.phone="10086"
            self.phonelength="\x0b"
        elif d==1:
            self.phone="10010"
            self.phonelength="\x0b"
        else:
            self.phone="00000000"
            self.phonelength="\x0e"

        path=super.manager.AskUser("","file",[".jar"])
        if path:
            path=path.encode("u8")
            self.add("开始破解…")
            self.handlefile(path)
            if self.hacked==1:
                #游戏被简单破解
                self.add("破解成功，请谨慎使用。如果手机提示发短信时，以“10086”开头，证明成功破解！")
                if appuifw.query(self.cn("破解完成，要安装吗？"),"query"):
                    appuifw.Content_handler().open((path[:-4]+"_hack.jar").decode("u8"))
            elif self.hacked==2:
                #游戏被深度破解
                self.add("破解成功，请谨慎使用。按确定手机未提示发短信而游戏提示发送成功，证明破解成功；按确定游戏提示发送失败证明游戏采用反破解技术，该方法无法破解！")
                if appuifw.query(self.cn("破解完成，要安装吗？"),"query"):
                    appuifw.Content_handler().open((path[:-4]+"_hack.jar").decode("u8"))
            else:
                self.add("可能不是短信收费游戏或者游戏已经被破解过，无法破解！")
                appuifw.note(self.cn("无法破解！"))
    def handlefile(self,path):
        ofile=zipfile.ZipFile(path)
        nfile=zipfile.ZipFile(path[:-4]+"_hack.jar","w",8)
        list=ofile.namelist()
        try:
            list.remove("")
        except:
            pass
        for i in list:
            self.add("正在处理"+i)
            if not i.endswith(".class"):
                nfile.writestr(ofile.getinfo(i),ofile.read(i))
            else:
                self.function(ofile,nfile,i)
        ofile.close()
        nfile.close()
    def function(self,ofile,nfile,i):
        pass

class SimpleHack(Hack):
    def function(self,ofile,nfile,i):
        data=ofile.read(i)
        pos=data.find("sms://")
        if pos==-1:
            nfile.writestr(ofile.getinfo(i),ofile.read(i))
        else:
            data=data[:pos-1]+self.phonelength+"sms://"+self.phone+data[pos+6:]
            nfile.writestr(ofile.getinfo(i),data)
            self.hacked=1

def name(index,pool):#名称
    for i in pool:
        if i[0]==index:
            break
    if i[1]=="Utf8" or i[1]=="Integer" or i[1]=="Float" or i[1]=="Long" or i[1]=="Double":
        return i[2].decode("u8")
    elif i[1]=="Class" or i[1]=="String" or i[1]=="NameAndType":
        return name(int(i[2]),pool)
    elif i[1]=="Fieldref" or i[1]=="Methodref" or i[1]=="InterfaceMethodref":
        return name(int(i[3]),pool)
def Int(x):
    return int(x.encode("hex"),16)

def constant(d):
    count=Int(d[8:10])
    pool=[]
    index=1
    pos=10
    INDEX={1:1,3:1,4:1,5:2,6:2,7:1,8:1,9:1,10:1,11:1,12:1}
    POS={1:0,3:5,4:5,5:9,6:9,7:3,8:3,9:5,10:5,11:5,12:5}
    TAG={1:"Utf8",3:"Integer",4:"Float",5:"Long",6:"Double",7:"Class",8:"String",9:"Fieldref",10:"Methodref",11:"InterfaceMethodref",12:"NameAndType"}
    while index<=count-1:
        tag=Int(d[pos:pos+1])
        if tag==1:
            length=Int(d[pos+1:pos+3])
            bytes=d[pos+3:pos+3+length]
            pool.append((index,TAG[1],bytes))
            pos+=3+length
        elif tag==3 or tag==5:
            bytes=d[pos+1:pos+5]
            if tag==3:
                bytes=str(Int(bytes[0:2])*100+Int(bytes[2:]))
            pool.append((index,TAG[tag],bytes))
        elif tag==4 or tag==6:
            bytes=d[pos+1:pos+9]
            pool.append((index,TAG[tag],bytes))
        elif tag==7 or tag==8:
            name=Int(d[pos+1:pos+3])
            pool.append((index,TAG[tag],name))
        elif tag==9 or tag==10 or tag==11 or tag==12:
            a=Int(d[pos+1:pos+3])
            b=Int(d[pos+3:pos+5])
            pool.append((index,TAG[tag],a,b))
        index+=INDEX[tag]
        pos+=POS[tag]
    return (pos,pool)

class DeepHack(Hack):
    def function(self,ofile,nfile,i):
        data=ofile.read(i)
        pos=data.find("send")
        if pos==-1:
            nfile.writestr(ofile.getinfo(i),data)
        else:
            (pos,pool)=constant(data)
            pos+=4
            while pos<=len(data)-5:
                pos=data.find("\xb9",pos)
                if pos==-1:
                    break
                else:
                    index=Int(data[pos+1:pos+3])
                    n=name(index,pool)
                    if n=="send" and Int(data[pos+4])==0:
                        data=data[:pos]+"\x57\x57\x00\x00"+data[pos+4:]
                        pos+=3
                        self.hacked=2
                    else:
                        pos+=1
            nfile.writestr(ofile.getinfo(i),data)
                