from tkinter import *
import time, threading, urllib, urllib.request as urllib2, gzip
import tkinter.messagebox as messagebox
from urllib.parse import unquote, quote, quote_plus, quote_from_bytes, unquote_to_bytes
import requests, datetime, time, os, sys
from bs4 import BeautifulSoup
from GUIFunction import Search as GUI_Search ,DownloadNovel as GUI_DownloadNovel
from tkinter import ttk

VersionInformation = 'V2.0.1_18_04_11'
__author__ = "Heanny Liu"
__title__ = "小说下载器"
rootTk = Tk()
rootTk.title("{} BY  {}".format(__title__, __author__))
rootTk.geometry("351x130")
rootTk.resizable(width=False, height=False)
rootTk.iconbitmap('favicon.ico')  # 添加icon
# nowPath = os.getcwd()
# rootTk.iconbitmap('{}\\favicon.ico'.format(nowPath))
from PIL import Image, ImageTk
var = StringVar()
var1 = StringVar()
var2 = StringVar()
_Text = Text

def SearchListWin():
    var2.set(var1.get())
    if var1.get() == '':
        messagebox.showerror('错误', "输入为空")
        return
    else:
        ReText = GUI_Search(var1.get())
        if ReText == 'none':
            messagebox.showinfo('提示', "搜索结果为空")
        else:
            # WinDL.destroy()
            WinDLList = Toplevel()
            WinDLList.title('小说下载')
            WinDLList.geometry("1021x500")
            # WinDLList.resizable(width=False, height=False)
            WinDLList.iconbitmap('favicon.ico')  # 添加icon
            Label(WinDLList, text='搜索内容为：{} 总共：{}本小说'.format(var1.get(), len(ReText))).pack()

            SelectFrame = Frame(WinDLList)
            SelectFrame.pack()
            Label(SelectFrame, text='选择序号：').pack(side=LEFT)

            #下拉列表
            DlValue = StringVar()
            numberChosen = ttk.Combobox(SelectFrame, width=12, textvariable=DlValue)
            numberChosen['values'] = list(range(len(ReText)))  # 设置下拉列表的值
            numberChosen.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
            numberChosen.pack(side=LEFT)

            Button(SelectFrame, text='提交',command=lambda :DownloadNovel_ID(ReText[int(DlValue.get())])).pack(side=LEFT)

            ##滚动条文本框
            ScroForT = Scrollbar(rootTk)  # 创建滚动条
            TextView = _Text(WinDLList, height=4, width=145)  # 创建文本框
            ScroForT.pack(side=RIGHT, fill=Y)
            TextView.pack(side=LEFT, fill=Y)
            ScroForT.config(command=TextView.yview)
            TextView.config(yscrollcommand=ScroForT.set)
            for Text in ReText:
                TextView.insert(E, '{}  {}  {}   {}  {}  {}  {}\n'.format(ReText.index(Text), Text[0], Text[2], Text[3], Text[5], Text[6], Text[7]))
                # Radiobutton(SearchFrame, text=Text[0],variable=var, value=Text[1],command=lambda :DownloadNovel_ID(Text)).pack()
            WinDLList.mainloop()
            # ##滚动条文本框
            # ScroForT = Scrollbar(WinDLList)  # 创建滚动条
            #
            # ScroForT.pack(side=RIGHT, fill=Y)
            # SearchFrame.pack(side=LEFT, fill=Y)
            # ScroForT.config(command=SearchFrame)


def DownloadNovel_ID(Text):
    DLre = messagebox.askquestion(title='下载', message='是否下载{}'.format(Text[0]))
    if DLre == 'yes':
        if GUI_DownloadNovel(Text[1],Text[0]) is True:
            messagebox.showinfo(title='提示' ,message='下载完成')
        else:
            messagebox.showerror('下载失败')
    else:
        pass
    # WinDLNovelNameLabel.pack()
    # WinDL.destroy()




def about():
    messagebox.showinfo('关于', "{}\n版本信息：{}\n作者：{}".format(__title__, VersionInformation, __author__))


menubar = Menu(rootTk)

# 创建下拉菜单File，然后将其加入到顶级的菜单栏中
FileMenu = Menu(menubar, tearoff=0)
FileMenu.add_command(label="搜索", command=lambda: rootTk.withdraw())
FileMenu.add_separator()  # 菜单横线
FileMenu.add_command(label="退出", command=rootTk.quit)
menubar.add_cascade(label="文件", menu=FileMenu)

# 创建下拉菜单Help
HelpMenu = Menu(menubar, tearoff=0)
HelpMenu.add_command(label="关于", command=about)
menubar.add_cascade(label="关于", menu=HelpMenu)
# 显示菜单
rootTk.config(menu=menubar)

# indexLbl = Label(rootTk,text='欢迎使用').pack(pady=20)

NovelFrame = Frame(rootTk)
NovelFrame.pack(pady=25)

NovelNameLabel = Label(NovelFrame, text='搜索内容：')
NovelNameLabel.pack(side=LEFT)
entryDL = Entry(NovelFrame, show='', textvariable=var1)
entryDL.pack(side=LEFT)
DownLoadBtn = Button(NovelFrame, text='搜索', command=SearchListWin)
DownLoadBtn.pack(side=LEFT, padx=10)

# entryDL = Entry(rootTk,show='')
# entryDL.pack()
# entrySe = Entry(rootTk,show='')
# entrySe.pack()


'''
##滚动条文本框
ScroForT = Scrollbar(rootTk)  # 创建滚动条
TextView = Text(rootTk, height=4, width=100)  # 创建文本框
ScroForT.pack(side=RIGHT, fill=Y)
TextView.pack(side=LEFT, fill=Y)
ScroForT.config(command=TextView.yview)
TextView.config(yscrollcommand=ScroForT.set)
'''
'''
#单选按钮radiobutton
v=rootTk.IntVar()
v.set(1)
#f1.bind('<KeyPress-1>',word_know)
f1 = rootTk.Radiobutton('xin',text = 'Know', font =24, variable=v,value=1, command = 'word_know')
f1.grid(row=6,column=2)
f1.configure(state='disabled')
#f2.bind('<KeyPress-2>',word_unknow)
f2 = rootTk.Radiobutton('xin',text = 'Unknow',font =24,variable=v,value=2, command = 'word_unknow')
f2.grid(row=6,column=3)
f2.configure(state='disabled')
'''

mainloop()
