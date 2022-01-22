from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error
import xlwt
from os import path
from wordcloud import WordCloud
import xlrd
import jieba
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
# from matplotlib.font_manager import FontProperties
# font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=14)
def main():
    baseurl ="https://www.bilibili.com/v/popular/rank/all"
    datalist=getdata(baseurl)
    # askurl(baseurl)
    path = "bilibili.xls"
    savedata(datalist,path)
    wordcloud()

findtitle = re.compile('<div class="info"><a class="title".*>(.*?)</a>')
findup = re.compile(r'<img alt="up".*>\s+(.*?)\s+</span>')
findplay = re.compile(r'<img alt="play".*>\s+(.*?)\s+</span>')
findlike = re.compile(r'<img alt="like".*>\s+(.*?)\s+</span>')
findlink = re.compile(r'<a href="(.*?)".*>')

def getdata(baseurl):
    print('getdata')
    datalist=[]
    html = askurl(baseurl)
    soup = BeautifulSoup(html,"html.parser")
    # print(soup)
    for item in soup.find_all("div",class_="content"):
        data = []
        item = str(item)
        title = re.findall(findtitle,item)[0]
        print(title)
        data.append(title)
        up = re.findall(findup,item)[0]
        data.append(up)
        play = re.findall(findplay,item)[0]
        print(play)
        data.append(play)
        like = re.findall(findlike,item)[0]
        data.append(like)
        link = "https:"+re.findall(findlink,item)[0]
        data.append(link)
            # print("Film Title: "+title+"Score: "+score+"Short Infomation: "+info)
        datalist.append(data)
    return datalist

def askurl(url):
    head={
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37"
    }
    request = urllib.request.Request(url,headers=head)
    print('askurl')
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode()
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html

def savedata(datalist,path):
    print('savedata')
    film = xlwt.Workbook(encoding='utf-8',style_compression=0)
    sheet = film.add_sheet('bilibil排行榜',cell_overwrite_ok=True)
    col = ("视频标题","UP主","播放量","弹幕数量","视频链接")
    for i in range(0,5):
        sheet.write(0,i,col[i])
    for i in range(0,100):
        data=datalist[i]
        for j in range(0,5):
            if(j!=4):
                sheet.write(i+1,j,data[j])
            else:
                sheet.write(i+1,j,xlwt.Formula('HYPERLINK("%s")' % data[j]))
    film.save(path)
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords

def seg_sentence(sentence):
   sentence_seged = jieba.cut(sentence.strip())
   stopwords = stopwordslist('stop.txt')
   outstr = ''
   for word in sentence_seged:
       if word not in stopwords:
           if word != '\t':
               outstr += word
               outstr += " "
   return outstr
def wordcloud():
    book = xlrd.open_workbook('bilibili.xls')
    sheet_name = book.sheet_names()
    sheet = book.sheet_by_name(sheet_name[0])
    col_data = ""
    for i in sheet.col_values(0):
        col_data = col_data + i
    f = open("wordcloud.txt", 'w', encoding='utf-8')
    f.write(col_data)
    f.close()
    inputs = open('wordcloud.txt', 'r', encoding='utf-8')
    outputs = open('wordcloud-cn.txt', 'w', encoding='utf-8')
    for line in inputs:
        line_seg = seg_sentence(line)
        outputs.write(line_seg + '\n')
    outputs.close()
    inputs.close()
    mask = np.array(Image.open("派大星.jpg"))  # 模板图片
    d = path.dirname(__file__)
    # Read the whole text.
    inputs = open('wordcloud.txt', 'r', encoding='utf-8')
    text = inputs.read()
    text = open(path.join(d, 'wordcloud-cn.txt'), encoding="UTF-8").read()
    wordcloud = WordCloud(mask=mask, font_path='STFANGSO.TTF', margin=1, random_state=1, max_words=300, width=1000,
                          height=700, background_color='white').generate(text)
    wordcloud.to_file('词云.jpg')
    inputs.close()
def pic():
    salary = [2500, 3300, 2700, 5600, 6700, 5400, 3100, 3500, 7600, 7800,
              8700, 9800, 10400]

    group = [500000,1000000,1500000,2000000,2500000,3000000,3500000,4000000]

    plt.hist(salary, group, histtype='bar', rwidth=0.8)

    plt.legend()

    plt.xlabel('salary-group')
    plt.ylabel('salary')
if __name__ == '__main__':
    main()