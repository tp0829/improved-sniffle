import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import jieba
import pinyin.cedict # 拼音模块:汉译英

from pandas import DataFrame
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from matplotlib.lines import Line2D

# matplotlib 无法显示中文解决如下(Ubuntu)
zhfont = mpl.font_manager.FontProperties(fname='Alibaba-PuHuiTi-Regular.otf')

import dataAcquisition # (自己写的函数)用来获取数据
                       # dataAcquisition(name='安徽大学',start='2004',end='2018')

# 函数 存储并显示词云图
def getWordCloud(fileName='安徽大学2004-2018'):
    csvFile = fileName+'.csv'
    df = pd.read_csv(csvFile)
    wordList = df['题目'].tolist()
    wordList_cut = [' '.join(jieba.cut(i)) for i in wordList]
    wordText = ' '.join(wordList_cut)
    picFile = '中国地图128W.png'
    imgMask = np.array(Image.open(picFile))

    # 设置需要屏蔽的词，如果为空，则使用内置的STOPWORDS
    stopwords = set(STOPWORDS)
    stopwords.add('及其')

    wc = WordCloud(background_color="white", max_words=1000, 
                    font_path="Alibaba-PuHuiTi-Regular.otf", 
                    mask=imgMask, stopwords=stopwords
                    ).generate(wordText)

    # 保存图片
    wcfile = '词云图_'+fileName[:-9]+'04-18.png'
    wc.to_file(wcfile)
    # 显示图片
    image=wc.to_image()
    image.show()

# 函数 统计15年每年的立项数和总金额,绘制成图表,保存并显示
def getData_count(fileName='安徽大学2004-2018'):
    csvFile = fileName+'.csv'
    df = pd.read_csv(csvFile)
    data_sum = list()   # 金额(万)
    data_count = list() # 立项数
    data_year = range(2004,2019)    # 年份
    data_name = [fileName[:-9]]*15
    for i in data_year:
        data_sum.append(int(df[df['批准年份']==i]['金额(万)'].sum()))
        data_count.append(df[df['批准年份']==i]['金额(万)'].count())
    data_f_k = ['学校','年份','总金额','立项数']
    data_f_v = [data_name,data_year,data_sum,data_count]
    data_f_d = dict(zip(data_f_k,data_f_v))
    data_f = DataFrame(data_f_d)
    data_f.index.name = '序号'
    # 存储 统计数据
    datafile = '统计表_'+fileName[:-9]+'04-18.csv'
    data_f.to_csv(datafile)

    # 绘制 图形
    x = data_f['年份']
    y1 = data_f['立项数']
    y2 = data_f['总金额']

    fig = plt.figure(figsize=(14,8), dpi=80)
    ax1 = plt.subplot(211)
    ax1.plot(x, y1, 'b-')
    ax1.grid(alpha=.4, axis="y")
    ax1.set_ylabel('立项数 /项', fontProperties=zhfont, color='tab:blue', fontsize=14)
    plt.title("国家自然基金项目:"+fileName, fontProperties=zhfont, fontsize=20, verticalalignment='bottom')

    ax2 = plt.subplot(212)
    ax2.plot(x, y2, 'r-')
    ax2.grid(alpha=.4, axis="y")
    ax2.set_xlabel('时间 /年', fontProperties=zhfont, fontsize=14)
    ax2.set_ylabel('总金额 /万元', fontProperties=zhfont, color='tab:red', fontsize=14)
    plt.subplots_adjust(wspace =0, hspace =0.2)
    # 存储
    picfile = '统计图_'+fileName[:-9]+'.png'
    plt.savefig(picfile)
    # 显示
    plt.show()

def bonus_scene(name=['安徽大学','合肥工业大学','中国科学技术大学']):
    csvFile0 = '统计表_'+name[0]+'.csv'
    data_f0 = pd.read_csv(csvFile0)
    csvFile1 = '统计表_'+name[1]+'.csv'
    data_f1 = pd.read_csv(csvFile1)
    csvFile2 = '统计表_'+name[2]+'.csv'
    data_f2 = pd.read_csv(csvFile2)

    # 绘制图形
    x = data_f0['年份']
    y0_1 = data_f0['立项数']
    y0_2 = data_f0['总金额']
    y1_1 = data_f1['立项数']
    y1_2 = data_f1['总金额']
    y2_1 = data_f2['立项数']
    y2_2 = data_f2['总金额']

    fig = plt.figure(figsize=(10,12), dpi=80)
    ax1 = plt.subplot(211)
    ax1.plot(x, y0_1, 'b-', x, y1_1, 'r-', x, y2_1, 'y-')
    ax1.grid(alpha=.4, axis="y")
    ax1.set_ylabel('立项数 /项', fontProperties=zhfont, color='tab:blue', fontsize=14)
    plt.title("国家自然基金项目:"+name[0]+','+name[1]+','+name[2], fontProperties=zhfont, fontsize=20, verticalalignment='bottom')
    
    # 图例 中文显示不了,之前解决的mat中文问题,在这里不行,采取拼音方式显示
    custom_lines = [Line2D([0], [0], color='b', lw=4),
                    Line2D([0], [0], color='r', lw=4),
                    Line2D([0], [0], color='y', lw=4)]
    name0 = pinyin.get(name[0],format="strip") 
    name1 = pinyin.get(name[1],format="strip") 
    name2 = pinyin.get(name[2],format="strip") 
    ax1.legend(custom_lines, [name0, name1, name2])

    ax2 = plt.subplot(212)
    ax2.plot(x, y0_2, 'b-', x, y1_2, 'r-', x, y2_2, 'y-')
    ax2.grid(alpha=.4, axis="y")
    ax2.set_xlabel('时间 /年', fontProperties=zhfont, fontsize=14)
    ax2.set_ylabel('总金额 /万元', fontProperties=zhfont, color='tab:red', fontsize=14)
    plt.subplots_adjust(wspace =0, hspace =0.2)
    # 存储
    picfile = '对比图_'+name[0]+','+name[1]+','+name[2]+'.png'
    plt.savefig(picfile)
    # 显示
    plt.show()

if __name__ == "__main__":
    print('----国家自然基金项目 数据获取及分析----')
    name = input('请输入学校名:')
    print('...数据正在获取')
    dataAcquisition.dataAcquisition(name)
    print('...数据正在保存到当前目录:'+name+'2004-2018.csv'+' 文件中!')
    print('数据获取成功!')
    while 1:
        ch = input("\n请输入接下来你要进行的操作:\n1.生成 词云图;\n2.生成 统计图;\n3.彩蛋;\n0.结束;\n")
        if ch == '1':
            print("词云图 生成较慢,请耐心等候...")
            getWordCloud(name+'2004-2018')
            continue
        elif ch == '2':
            getData_count(name+'2004-2018')
            continue
        elif ch == '3':
            try:
                print("接下来进入彩蛋环节,请输入三所学校的名字,确保这三所学校你已经生成过它们的 统计图 ")
                a = input("(以空格隔开):")
                a = a.split()
                bonus_scene(a)
            except :
                print("出现错误! 请检查输入的学校有无生成过统计图")
            finally:
                pass
            continue
        elif ch == '0':
            break
        else:
            print("你输入的有误,请重新运行该脚本")
            continue
