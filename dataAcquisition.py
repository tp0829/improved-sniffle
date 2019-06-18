# LetPub提供数据查询,当数据超过50页时,只显示到50页
#   :故可能需要一次查询的范围尽可能精确,然后把多次查询结果合并处理

# 问题处理 
# # (已处理)当前页面只有一页
# # # 首页的url和第1页的不一样,第一页的和下一页的格式相同

import requests, bs4, os
import pandas as pd
from pandas import DataFrame


# 全局变量
companyName = ''    # 学校
startTime = ''      # 起始时间
endTime = ''        # 终止时间
url = ''            # 存储url
dataAll = list()    # 存储每页的粗数据,2维list
data_two_f = dict() # 存储数据为pandas.DataFrame对象

# 函数 拼接url
def writeInfo():
    global companyName
    global startTime
    global endTime
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
        elems_td = pageSoup.select('table tr td') # 获取所有<table><tr><td>元素,elems:list
        global dataAll
        dataAll.append(elems_td) # dateAll[0][i].getText()

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

# 函数 清洗数据:去除表格数据中的表头,表尾,保存为pandas.DataFrame对象,且保存到本地csv文件中
def cleanData():
    # 获取"清洗1.0"数据:去除表格的头尾,且把每页的数据保存在一起
    data_one = list()
    for i in dataAll:
        data_oneone = list()
        for ii in i:
            data_oneone.append(ii.getText())
        data_oneone = data_oneone[36:-1]  # 去掉表头等不必要信息
        data_one.extend(data_oneone)

    # 获取"清洗2.0"数据:pandas.DataFrame存储数据
    data_one_0 = data_one[::15] # 负责人
    data_one_1 = data_one[1::15] # 单位
    data_one_2 = data_one[2::15] # 金额(万)
    data_one_3 = data_one[3::15] # 项目编号
    data_one_4 = data_one[4::15] # 项目类型
    data_one_5 = data_one[5::15] # 所属学部
    data_one_6 = data_one[6::15] # 批准年份
    data_one_8 = data_one[8::15] # 题目
    data_one_10 = data_one[10::15] # 学科分类
    data_one_12 = data_one[12::15] # 学科代码
    data_one_14 = data_one[14::15] # 执行时间
    data_two_d_k = ['负责人','单位','金额(万)','项目编号','项目类型','所属学部','批准年份','题目','学科分类','学科代码','执行时间']
    data_two_d_v = [data_one_0,data_one_1,data_one_2,data_one_3,data_one_4,data_one_5,data_one_6,data_one_8,data_one_10,data_one_12,data_one_14]
    data_two_d = dict(zip(data_two_d_k,data_two_d_v))
    global data_two_f
    data_two_f = DataFrame(data_two_d)
    data_two_f.index.name = '序号'

    '''
    0   负责人      '张琛',
    1   单位        '合肥学院',
    2   金额(万)    '23.00',
    3   项目编号    '61806068',
    4   项目类型    '青年科学基金项目',
    5   所属学部    '信息科学部',
    6   批准年份    '2018',
    7                   '题目',
    8   题目            '面向PM2.5空气污染的多重分形与协同群体智能算法研究',
    9                   '学科分类',
    10  学科分类        '一级：人工智能，二级：知识表示与处理，三级：知识发现与数据挖掘',
    11                  '学科代码',
    12  学科代码        '一级：F06，二级：F0605，三级：F060504',
    13                  '执行时间',
    14  执行时间        '2019-01 至 2021-12',
    '''

    # 存储"清洗2.0"数据:DataFrame存储到本地CSV文件
    global companyName
    global startTime
    global endTime    
    pagePath = companyName+startTime+'-'+endTime+'.csv'
    data_two_f.to_csv(pagePath)
    # 读取
    # d = pandas.read_csv('xx.csv')


if __name__ == "__main__":
    print('----国家自然基金项目 数据获取----')
    companyName = input('请输入要获取数据的的学校名:')
    startTime = input('请输入起始年份:')
    endTime = input('请输入终止年份:')
    print('...正在获取')
    writeInfo()
    getData()
    cleanData()
    print('获取成功!')
