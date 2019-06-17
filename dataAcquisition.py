# LetPub提供数据查询,当数据超过50页时,只显示到50页
#   :故可能需要一次查询的范围尽可能精确,然后把多次查询结果合并处理

# 问题处理 
# # (已处理)当前页面只有一页
# # # 首页的url和第1页的不一样,第一页的和下一页的格式相同

import requests, bs4, os

# 全局变量
url = ''    # 存储url
dataAll = list()    # 存储每页的粗数据,2维list

# 函数 拼接url
def writeInfo(companyName,startTime,endTime):
    url1 = 'http://www.letpub.com.cn/?page=grant' # LetPub 国家自然基金项目查询
    url2 = '&company=' + companyName
    url3 = '&startTime=' + startTime
    url4 = '&endTime=' + endTime
    global url
    url = url1 + url2 + url3 + url4

# 函数 获取网页中表格数据
def getData():  # 获取元素数据:包含了表格的头尾,且每页分开存储,dataAll为2维list
    pageOver = False
    pageFirst = True
    while not pageOver:
        global url
        pageRe = requests.get(url)  # 请求网页
        try:    # 错误检查,请求出错,将抛出异常
            pageRe.raise_for_status()
        except Exception as exc:
            print('error problem: %s' %(exc))

        pageSoup = bs4.BeautifulSoup(pageRe.text,'lxml') # lxml?
        elems = pageSoup.select('table tr') # 获取所有<table>下<tr>元素,elems:list
        global dataAll
        dataAll.append(elems) # dateAll[0][i].getText()

        elems_a = pageSoup.select('table tr a')
        if pageFirst:   # 将拼接的url转换成系统默认生成的url,仅执行一次
            for i in elems_a:   # elems_a:list
                if i.getText() == '1':  # 首页的url和第1页的不一样,第一页的和下一页的格式相同
                    url = i.get('href')
                    pageFirst = False
                    break
        for i in elems_a:  # 获取下一页面url
            if i.getText() == '下一页': 
                if url == i.get('href'):
                    pageOver = True
                else:
                    url = i.get('href')
                break

# 函数 清洗数据:去除表格数据中的表头,表尾
def cleanData():
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





print(writeInfo('合肥学院','2018','2018'))
print(url)
getData()
print(len(dataAll))
print(dataAll)
