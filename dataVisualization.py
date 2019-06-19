import numpy as np
import pandas as pd
from pandas import DataFrame

import jieba
from wordcloud import WordCloud, STOPWORDS
from PIL import Image

def getWordCloud(fileName='安徽大学2014-2018'):
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

    wc = WordCloud(background_color="white", max_words=2000, 
                    font_path="Alibaba-PuHuiTi-Regular.otf", 
                    mask=imgMask, stopwords=stopwords
                    ).generate(wordText)
    
    # 保存图片
    wcfile = fileName+'.png'
    wc.to_file(wcfile)

    # 显示图片
    # image=wc.to_image()
    # image.show()

if __name__ == "__main__":
    getWordCloud()


