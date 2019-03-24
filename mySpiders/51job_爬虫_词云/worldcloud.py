"""
    将抓取的数据生成词云
"""
import jieba
import wordcloud
import re
import numpy as np
from PIL import Image

stopwords = {  # 停用词+
    '经验', '职能', '类别', '相关', '关键字', '良好', '能力', '专业', '具有', '具备', '完成', '负责', '良好', '工作', '根据', '优先', '熟练', '使用',
    '以上', '熟悉', '要求', '拥有', '软件', '工程师', '开发', '熟悉', '以上', '以上学历', '学历', '一定', '以及', '从事', '常用', '深入', '了解', '描述'
}
# 分割词
with open('requestion.txt', 'r', encoding='gbk') as f:
    text = f.read()
    pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"')
    string_data = re.sub(pattern, '', text)  # 将符合模式的字符去除
    result = jieba.lcut(text)
    cloud_text = ",".join(result)

# 生成词云图
wc = wordcloud.WordCloud(
    stopwords=stopwords,
    scale=8,  # 越大越清晰，32已经跑不起来啦
    width=1500,
    height=1250,
    font_path="C:\\Windows\\Fonts\\STXINWEI.TTF",
    background_color="pink",
    max_words=500,
    mask=np.array(Image.open("china.png")),
    max_font_size=99,
    min_font_size=20,
    random_state=64,
).generate(cloud_text)
wc.to_file('wordcloud.jpeg')
