import sys, urllib, urllib.request as urllib2, gzip,time
from urllib.parse import quote_from_bytes
from bs4 import BeautifulSoup

SearchUrl = 'http://www.biquge.com.tw/modules/article/soshu.php?searchkey=+'
dUrl = 'http://www.biquge.com.tw'


def Search(keyWord):
    SearchList = []
    key = quote_from_bytes(keyWord.encode('gbk'))
    url = '{}{}'.format(SearchUrl, key)
    data = None
    cookie_lib = None
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Accept': 'text/html, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
        'DNT': '1',
        # 'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,ja;q=0.6',
        'Cookie': '%s' % cookie_lib
    }
    reqUrl = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(reqUrl)
    html = response.read()
    try:
        htmlData = gzip.decompress(html)
    except:
        try:
            htmlData = html.decode('gbk')
        except:
            htmlData = html.decode("utf-8")
    trData = BeautifulSoup(htmlData, 'html.parser').findAll('tr', attrs={'id': 'nr'})
    for tr in trData:
        oddData = tr.findAll('td', attrs={'class': 'odd'})
        NovelName = oddData[0].find('a').text
        NovelUrl = oddData[0].find('a')['href']
        NovelAuthor = oddData[1].text
        NovelDate = oddData[2].text
        evenData = tr.findAll('td', attrs={'class': 'even'})
        NovelEnd = evenData[0].find('a').text
        NovelEndUrl = evenData[0].find('a')['href']
        NovelSize = evenData[1].text
        NovelState = evenData[2].text
        SearchList.append(['《{}》'.format(NovelName), NovelUrl, '作者：{}'.format(NovelAuthor), '最新章节：{}'.format(NovelEnd),
                           'http://www.biquge.com.tw{}'.format(NovelEndUrl), '字数：{}'.format(NovelSize),
                           '最后更新时间：{}'.format(NovelDate),
                           '状态：{}'.format(NovelState)])
    # for SearList in SearchList:
    #     print(SearchList.index(SearList), ':', SearList[0], SearList[2], SearList[3], SearList[5], SearList[6])
    if len(SearchList) == 0:
        return 'none'
    else:
        return SearchList





def NovelIDData(url, BookName):
    cookie_lib = None
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Accept': 'text/html, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
        'DNT': '1',
        # 'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,ja;q=0.6',
        'Cookie': '%s' % cookie_lib
    }
    UrlData = None
    reqURL = urllib2.Request(url, UrlData, headers)
    html = urllib2.urlopen(reqURL).read()
    try:
        htmlData = gzip.decompress(html)
    except:
        try:
            htmlData = html.decode('gbk')
        except:
            htmlData = html.decode("utf-8")
    # html = response.read().decode('gb2312')
    return htmlData


def AnalyticDataBS4(html):
    aList = []
    htmlData = BeautifulSoup(html, 'html.parser')
    divData = htmlData.find('div', attrs={'id': "list"})
    ddData = divData.findAll('dd')
    for dd in ddData:
        aData = dd.find('a')
        aList.append([aData.text, aData['href']])
    return aList


def DetailedOfChapter(chapterID, chapterName):
    url = '{}{}'.format(dUrl, chapterID)
    cookie_lib = None
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Accept': 'text/html, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
        'DNT': '1',
        # 'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,ja;q=0.6',
        'Cookie': '%s' % cookie_lib
    }
    UrlData = None
    reqUrl = urllib2.Request(url, UrlData, headers)
    response = urllib2.urlopen(reqUrl)
    html = response.read()
    try:
        htmlData = gzip.decompress(html)
    except:
        try:
            htmlData = html.decode('gbk')
        except:
            htmlData = html.decode("utf-8")
    return htmlData


def ChapterText(htmlData):
    ''' 获取章节内容 '''
    html = BeautifulSoup(htmlData, 'html.parser')
    ChapterData = html.find('div', attrs={'class': "bookname"}).find('h1').text
    DivData = html.find('div', attrs={'id': "content"})
    return '\n{}\n{}'.format(ChapterData, DivData.text)


def SaveNovelText(data, BookID):
    f = open('{}.txt'.format(BookID), 'w+', encoding='utf8')
    try:
        f.write(data)
    except:
        return False
    finally:
        f.close()
        return True



def DownloadNovel(url, BookName):
    text = ''
    try:
        IDHtml = NovelIDData(url, BookName)
        aList = AnalyticDataBS4(IDHtml)
        for aData in aList:
            deData = DetailedOfChapter(aData[1], aData[0])
            text += str(ChapterText(deData))
            # time.sleep(1)
        SaveNovelText(text, BookName)
        return True
    except:
        return False

'''
def show1():
    top1=Toplevel()
    image = Image.open('logo.png')
    img = ImageTk.PhotoImage(image)
    canvas1 = Canvas(top1, width = image.width ,height = image.height, bg = 'white')
    canvas1.create_image(0,0,image = img,anchor="nw")
    canvas1.create_image(image.width,0,image = img,anchor="nw")
    canvas1.pack()
    top1.mainloop()
    '''
'''
def DownloadWin():
    WinDL = Toplevel()
    WinDL.title('小说下载')
    WinDL.geometry("521x300")
    WinDL.iconbitmap('favicon.ico')  # 添加icon

    NovelNameLabel = Label(WinDL, text='名字：')
    NovelNameLabel.pack()
    entryDL = Entry(WinDL, show='')
    entryDL.pack()
    NovelIDLabel = Label(WinDL, text='ID：')
    NovelIDLabel.pack()
    entrySe = Entry(WinDL, show='')
    entrySe.pack()
    DownLoadBtn = Button(WinDL, text='下载')
    DownLoadBtn.pack()

    WinDL.mainloop()


def SearchWin(rootTk):
    # rootTk.withdraw() #隐藏主窗口
    # rootTk.hide()
    WinSe = Toplevel()
    WinSe.title('小说搜索')
    WinSe.geometry("521x300")
    WinSe.iconbitmap('favicon.ico')  # 添加icon

    NovelNameLabel = Label(WinSe,text='搜索内容：')
    NovelNameLabel.pack()
    entryDL = Entry(WinSe,show='',textvariable=var1)
    entryDL.pack()
    DownLoadBtn = Button(WinSe,text='搜索',command=lambda :SearchListWin())
    # DownLoadBtn = Button(WinSe,text='搜索',command=WinSe.destroy,dict={'a':1})
    DownLoadBtn.pack()

    WinSe.mainloop()
'''


'''
            canvas = Canvas(WinDLList, width=510, height=280, scrollregion=(0, 0, 280, 600))  # 创建canvas
            canvas.place(x=0, y=20)  # 放置canvas的位置
            SearchFrame = Frame(canvas)  # 把frame放在canvas里
            SearchFrame.place(width=500, height=280)  # frame的长宽，和canvas差不多的
            vbar = Scrollbar(canvas, orient=VERTICAL)  # 竖直滚动条
            vbar.place(x=500,width=20, height=280)
            vbar.configure(command=canvas.yview)
            # canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.config( yscrollcommand=vbar.set)  # 设置
            canvas.create_window((90, 240), window=SearchFrame)  # create_window

'''


