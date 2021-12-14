import pandas as pd
import jieba
import matplotlib.pyplot as plt
# from wordcloud import STOPWORDS
# 加载自定义词典
newdict_path = "a.txt"
jieba.load_userdict(newdict_path)
def judge_null(column):
    if pd.isna(column):
        return '\n'
    if len(column)<0:
        return '\n'
    return column

# 加载停用词词典
stop_list = []
# stopwords=STOPWORDS
stopdict_path = 'StopWords.txt'
with open(stopdict_path, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        stop_list.append(line[:-1])
data = pd.read_csv('知乎三孩.csv')
data['回答'] = data['回答'].apply(lambda x : judge_null(x).replace('\n', ''))
# data['回答'] = data['回答'].apply(lambda x : judge_null(x).replace('\n', ''))
data['分词'] = data['回答'].apply(lambda x : [i for i in jieba.cut(judge_null(x)) if i not in stop_list])
data['创建时间'] = data['创建时间'].apply(lambda x : x[:10])
all_words = data['分词'].to_list()

word_dict = {}
for words in all_words:
    for word in words:
        if word in word_dict:
            word_dict[word] += 1
        else:
            word_dict[word] = 1



from wordcloud import WordCloud
from matplotlib import colors

color_list = ['#130c0e','#464547']#建立颜色数组
colormap = colors.ListedColormap(color_list)#调用

def getIndexEndDic(data):
    ciyun_dic={}
    for v in data:
        ciyun_dic[str(v[0])]=v[1]
    return ciyun_dic

def removeEmpty(data):
    data2 = {}
    for o in data:
        if not o==' ':
            data2[o] = data[o]
    return data2
# 生成词云
def create_word_cloud(word_dict):
    # 支持中文, SimHei.ttf可从以下地址下载：https://github.com/cystanford/word_cloud
    wc = WordCloud(
        font_path="SimHei.ttf",
        background_color='white',
        max_words=50,
        scale=28,
        colormap=colormap
    )
    f_txt = open('词频.txt', 'w+', encoding='utf_8')

    word_dict=removeEmpty(word_dict)
    wdic=sorted(word_dict.items(), key=lambda item: item[1],reverse=True)
    start_index=0
    end_index=50
    wdic=wdic[start_index:end_index]
    ciyun_dic=getIndexEndDic(wdic)

    for v in wdic:
        if v[0]==' ':
            print('移除空数据')
        else:
            f_txt.write(str(v[0]) + ':' + str(v[1]) + '\n')

    word_cloud = wc.generate_from_frequencies(ciyun_dic)
    # 写词云图片
    word_cloud.to_file("sanhai.jpg")
    # 显示词云文件
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.show()
    f_txt.close()

# 根据词频生成词云
create_word_cloud(word_dict)
