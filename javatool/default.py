try:
    import javatool
except:
    import appuifw,sys,traceback
    appuifw.app.title="致命错误".decode("u8")
    appuifw.app.body=t=appuifw.Text("本软件需要appuifw等模块支持，请确保有这些模块，请将错误发到930372551@qq.com，谢谢您的使用！\n".decode("u8"))
    error="".join(traceback.format_exception(*sys.exc_info()))
    t.add(unicode(error))
    t.set_pos(0)
    appuifw.app.exit_key_handler=sys.exit
