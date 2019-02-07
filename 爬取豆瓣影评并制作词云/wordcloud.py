import jieba
import wordcloud
import re
import numpy as np
from PIL import Image

with open('蔡娘娘不欺负女孩子短评.txt', 'r', encoding='utf-8') as f:
    text = f.read()
    pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"')  # 定义正则表达式匹配模式
    string_data = re.sub(pattern, '', text)  # 将符合模式的字符去除
    result = jieba.lcut(text)
    cloud_text = ",".join(result)

wc = wordcloud.WordCloud(
    scale=16,  # 越大越清晰，32已经跑不起来啦
    width=1024,
    height=768,  # width,height设置生成的词云图片的大小
    font_path="C:\\Windows\\Fonts\\STXINWEI.TTF",  # 设置字体为本地的字体，有中文必须要加
    background_color="pink",  # 设置背景的颜色，需与背景图片的颜色保持一致，否则词云的形状会有问题
    max_words=1000,  # 设置最大的字数
    mask=np.array(Image.open("pic.jpg")),  # 通过mask 参数 来设置背景图片，即词云的形状
    max_font_size=100,  # 设置字体的最大值
    random_state=48  # 设置有多少种随机生成状态，即有多少种配色方案
).generate(cloud_text)
wc.to_file('蔡娘娘.jpeg')
