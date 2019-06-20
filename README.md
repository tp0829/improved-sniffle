# improved-sniffle

#### Python课程设计：XX大学近15年（2004-2018）国家自然基金项目立项数据的获取及分析

- 2.5 测试

    - 2.5.1 数据获取测试：dataAcquisition.py

        - ①代码（脚本）运行环境：

            操作系统：macOS 10.14.5

            Python版本：Python 3.7.1

            模块引用：

            ```python
            # 代码段 2
            import requests, bs4, os
            import pandas as pd
            from pandas import DataFrame
            ```
    
        - ②代码（脚本）说明：
    
            运行该代码（脚本），将以提示的方式，引导用户在命令行里分别输入：学校名称、要查询数据的起始年份和终止年份。
    
            ```python
            # 代码段 3
            if __name__ == "__main__":
                print('----国家自然基金项目 数据获取----')
                name = input('请输入要获取数据的的学校名:')
                start = input('请输入起始年份:')
                end = input('请输入终止年份:')
                print('...数据正在获取')
                dataAcquisition(name,start,end)
                print('...数据正在保存到当前目录:'+name+start+'-'+end+'.csv'+' 文件中!')
                print('数据获取成功!')            
            ```
    
        - ③测试实例：
    
            输入：
    
            ![img](http://ww4.sinaimg.cn/large/006tNc79ly1g487jio37rj31co07gacg.jpg)

            输出：

            ![img](http://ww1.sinaimg.cn/large/006tNc79ly1g4889n3428j31180dc7av.jpg)

        

    - 2.5.1 数据分析测试：dataVisualization.py

        - ①代码（脚本）运行环境：

            操作系统：macOS 10.14.5

            Python版本：Python 3.7.1

            模块引用：
        
            ```python
            # 代码段 4
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
            ```

		- ②代码（脚本）说明：

            运行该代码（脚本），将以提示的方式，引导用户在命令行里分别输入学校名称然后进行该学校04-18年数据的获取，获取数据结束后，以一个选择方式让用户选择：生成词云图或生成统计表，再或者用户选择选项3，则提示用户输入3所学校的名称，进行统计数据的对比（3所学校必须都进行过生成统计表操作。）

			```python
			# 代码段 5
            if __name__ == "__main__":
                print('----国家自然基金项目 数据获取及分析----')
                name = input('请输入学校名:')
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
			```
			
		- ③测试实例：
			
			输入：
			
			![img](http://ww4.sinaimg.cn/large/006tNc79ly1g4889lnav9j313m068myr.jpg)
			
			输出：
			
			![img](http://ww2.sinaimg.cn/large/006tNc79ly1g4889o2cacj313o0baq8r.jpg)
			
			输入：
			
			![img](http://ww3.sinaimg.cn/large/006tNc79ly1g4889ozccwj313w09e75s.jpg)
			
			输出：
			
			![img](http://ww1.sinaimg.cn/large/006tNc79ly1g4889l4f3ij30u00u04em.jpg)
			
			输入：
			
			![img](http://ww2.sinaimg.cn/large/006tNc79ly1g4889m4bjqj313o05k74k.jpg)
			
			输出：
			
			![img](http://ww2.sinaimg.cn/large/006tNc79ly1g4889oinjnj31320h876p.jpg)
			
			![img](http://ww3.sinaimg.cn/large/006tNc79ly1g4889pgug9j30v40hs0um.jpg)
			
			输入：
			
			![img](http://ww1.sinaimg.cn/large/006tNc79ly1g4889nkw12j313w06uwfj.jpg)
			
			输出：
			
			![img](http://ww1.sinaimg.cn/large/006tNc79ly1g4889mlholj30m80qoq53.jpg)