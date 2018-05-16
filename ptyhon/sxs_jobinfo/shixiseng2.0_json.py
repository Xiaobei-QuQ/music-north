"""
注意注意：
1、函数命名要清晰，容易弄混
2、符号要写好
3、.contents 后不能用get_text()？？？
4、使用 json 进行字符串转换存在一个潜在的问题。
由于 json 语法规定 数组或对象之中的字符串必须使用双引号，不能使用单引号 
(官网上有一段描述是 “A string is a sequence of zero or more Unicode characters, wrapped in double quotes, using backslash escapes” )
"""

import re
import csv
import requests
import jieba
import json
import numpy as np
import pandas as pd
from tqdm import tqdm
from scipy.misc import imread
from bs4 import BeautifulSoup
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt


def get_one_page(cityid, keyword, pages):
    # 获取网页html内容并返回
    paras = {
        'k': keyword,
        'p': pages
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3423.2 Safari/537.36',
        'Host': 'www.shixiseng.com',
        'Referer': 'https://www.shixiseng.com/gz',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

    url = 'https://www.shixiseng.com/interns/c-{}_?'.format(cityid)

    # 获取网页内容，返回html数据
    response = requests.get(url, headers=headers, params=paras)
    # 通过状态码判断是否获取成功
    if response.status_code == 200:
        return response.text
    return None


def get_detail_pageinfo(response):
    hrefs = re.findall('.*?<a class="name" href="(.*?)" target=.*?', response, re.S)
    return hrefs


def get_detail_page(href):
    url = 'https://www.shixiseng.com' + href

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3423.2 Safari/537.36',
        'Host': 'www.shixiseng.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

    # 获取网页内容，返回html数据
    response = requests.get(url=url, headers=headers)
    # 通过状态码判断是否获取成功
    if response.status_code == 200:
        return response.text
    return None


def parse_detail_info(response):
    response = decrypt_text(response)
    soup = BeautifulSoup(response, 'lxml')

    info1 = soup.find(class_='job-header')
    job = info1.find(class_='new_job_name').get_text()

    info1_detail = info1.find(class_='job_msg')
    salary = info1_detail.find(class_='job_money cutom_font').get_text()
    city = info1_detail.find(class_='job_position').get_text()
    education = info1_detail.find(class_='job_academic').get_text()
    workday = info1_detail.find(class_='job_week cutom_font').get_text()
    worktime = info1_detail.find(class_='job_time cutom_font').get_text()

    job_good = info1.find(class_='job_good').get_text()
    job_detail = soup.find(class_='job_detail').get_text().replace('\n','')

    info2 = soup.find(class_='job-com')
    company_href_pre = info2.a
    company_href = 'https://www.shixiseng.com' + company_href_pre['href']
    company_pic_pre = info2.find('img')
    company_pic = company_pic_pre['src']

    company_info = info2.find('div')
    company_name = company_info.get_text()
    company_scale = info2.find(class_='com-num').get_text()
    company_class = info2.find(class_='com-class').get_text()

    return {
        'job':job,
        'salary':salary,
        'city':city,
        'education':education,
        'workday':workday,
        'worktime':worktime,
        'job_good':job_good,
        'job_detail':job_detail,
        'company_pic':company_pic,
        'company_name':company_name,
        'company_scale':company_scale,
        'company_class':company_class
    }


def write_csv_headers(file, headers):
    # 写入表头
    with open(file, 'a', encoding='gb18030', newline='') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()


def write_csv_rows(file, headers, rows):
    # 写入行
    with open(file, 'a', encoding='gb18030', newline='') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writerow(rows)


def decrypt_text(text):
    # 定义文本信息处理函数，通过字典mapping中的映射关系解密
    for key, value in mapping.items():
        text = text.replace(key, value)
    return text


def write_txt_file(file, txt):
    # 写入txt文本
    with open(file, 'a', encoding='gb18030', newline='') as f:
        f.write(txt)


def read_txt_file(file):
    # 读取txt文本
    with open(file, 'r', encoding='gb18030', newline='') as f:
        return f.read()


def wordcloud(words_df, keyword):
    stopwords = pd.read_csv("stopwords.txt", index_col=False, quoting=3, sep=" ", names=['stopword'], encoding='utf-8')
    words_df = words_df[~words_df.segment.isin(stopwords.stopword)]

    words_stat = words_df.groupby(by=['segment'])['segment'].agg({"计数": np.size})
    words_stat = words_stat.reset_index().sort_values(by=["计数"], ascending=False)

    # 设置词云属性
    color_mask = imread('backgroud.png')
    wordcloud = WordCloud(font_path="simhei.ttf",   # 设置字体可以显示中文
                    background_color="white",       # 背景颜色
                    max_words=100,                  # 词云显示的最大词数
                    mask=color_mask,                # 设置背景图片
                    max_font_size=100,              # 字体最大值
                    random_state=42,
                    width=1000, height=860, margin=2,# 设置图片默认的大小,但是如果使用背景图片的话,                                                   # 那么保存的图片大小将会按照其大小保存,margin为词语边缘距离
                    )


    # 生成词云, 可以用generate输入全部文本,也可以我们计算好词频后使用generate_from_frequencies函数
    word_frequence = {x[0]:x[1]for x in words_stat.head(100).values}
    word_frequence_dict = {}
    for key in word_frequence:
        word_frequence_dict[key] = word_frequence[key]

    wordcloud.generate_from_frequencies(word_frequence_dict)
    # 从背景图片生成颜色值
    image_colors = ImageColorGenerator(color_mask)
    # 重新上色
    wordcloud.recolor(color_func=image_colors)
    # 保存图片
    picname = 'tongji_' + keyword + '.png'
    wordcloud.to_file(picname)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()


def main(city, keyword, pages):
    f_cityid = open('cityid_list.json','r', encoding ='utf8')
    data_id = f_cityid.read()
    data_id = json.loads(data_id)
    cityid = data_id[city]

    csv_filename = 'sxs' + str(cityid) +'_' +keyword +'.csv'
    txt_filename = 'sxs' + str(cityid) + '_' + keyword + '.txt'
    headers = ['job','salary','city','education','workday','worktime','job_good','job_detail',
               'company_pic','company_name','company_scale','company_class']
    write_csv_headers(csv_filename, headers)
    n = 0

    for i in tqdm(range(pages)):
        try:
            # 获取该页中的所有职位信息，写入csv文件
            i = i + 1
            response = get_one_page(cityid, keyword, i)

            hrefs = get_detail_pageinfo(response)
            for href in hrefs:
                n += 1
                response_detail = get_detail_page(href)
                items = parse_detail_info(response_detail)

                pattern = re.compile(r'[一-龥]+')        # 清除除文字外的所有字符
                data = re.findall(pattern, items['job_detail'])
                write_txt_file(txt_filename, ''.join(data))          # 不能直接写data，此时的data是列表格式
                write_csv_rows(csv_filename, headers, items)
                print('已录入 %d 条数据' % n)
        except:
            break

    content = read_txt_file(txt_filename)
    segment = jieba.lcut(content)
    words_df = pd.DataFrame({'segment': segment})
    wordcloud(words_df, keyword)


if __name__ == '__main__':
    # 手动输入解密映射，需要时自助更新
    mapping = {'&#xe3cb': '0', '&#xe955': '1', '&#xead0': '2', '&#xe9f8': '3', '&#xf25f': '4',
           '&#xe4e6': '5', '&#xf078': '6', '&#xe4d6': '7', '&#xe961': '8', '&#xef80': '9'}

    '''
    第一个参数 ：工作城市（小城市搜索不到会报错，可查看 cityid_list 文档里可搜索的城市）
    第二个参数 ：岗位关键词
    第三个参数 ：爬取的岗位网页页数，一页有10个岗位信息
    '''
    main('广州', '数据分析师', 2)
