# 数据最多提供50页,故可能需要再次处理
import requests, bs4, os

url1 = 'http://www.letpub.com.cn/?page=grant' #LetPub 国家自然基金项目查询
url2 = '&company='
url3 = '中国科学技术大学'
url4 = '&startTime=2016&endTime=2016'
url = url1 + url2 + url3 + url4

# 获取元素数据:包含了表格的头尾,且每页分开存储
pageOver = False
dateAll = list()
pageNum = 0
while not pageOver:
    pageNum = pageNum + 1
    # (未处理)当前页面只有一页
    res = requests.get(url)
    # 检查错误,下载文件出错,将抛出异常
    try:
        res.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' %(exc))

    # 写二进制模式打开该文件,并写入文件
    pagePath = url3+url4+str(pageNum)+'.txt'
    pageFile = open(pagePath, 'wb')
    for chunk in res.iter_content(100000):
        pageFile.write(chunk)
    pageFile.close()

    # bs4 获取主要信息
    pageFile = open(pagePath) 
    pageSoup = bs4.BeautifulSoup(pageFile.read(),'lxml') # lxml??
    elems = pageSoup.select('table tr') # 在<table>元素下的<tr>元素
    dateAll.append(elems) # dateAll[0][i].getText()
    pageFile.close()

    # 获取下一页面路径
    elems_a_nextPage = pageSoup.select('table tr a')
    for i in range(len(elems_a_nextPage)): 
        if elems_a_nextPage[i].getText() == '下一页': 
            # print(elems_a_nextPage[i].get('href'))
            if url == elems_a_nextPage[i].get('href'):
                pageOver = True
            else:
                url = elems_a_nextPage[i].get('href')
            break

# 获取"清洗1.0"数据:去除表格的头尾,且把每页的数据保存在一起
date_1 = list()
for i in range(len(dateAll)):
    date_11 = [] # 临时变量
    for ii in range(len(dateAll[i])):
        date_11.append(dateAll[i][ii].getText())
    date_11 = date_11[11:]
    date_11 = date_11[:-1]
    date_1.extend(date_11)

# "清洗1.0"数据保存到文件中
pagePath = url3+'.txt'
pageFile = open(pagePath, 'a')

dateNum = 0
for i in date_1:
    dateNum = dateNum + 1
    pageFile.write(i+'\n')
    if dateNum % 5 == 0:
        pageFile.write('\n')
pageFile.close()


