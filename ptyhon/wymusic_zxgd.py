from bs4 import BeautifulSoup
import requests
import re
import json

def get_response(url,params,headers):
    response = requests.post(url=url, headers=headers, data=params).text
    return response

def get_info(zx_music):
    for i in range(10):
        dic = {}
        id_ = zx_music[i]['id']
        dic['id_'] = id_
        zx_music_info = zx_music[i]['song']
        dic['name']= zx_music_info['name']
        dic['signer']= zx_music_info['artists'][0]['name']
        dic['album']= zx_music_info['album']['name']
        dic['href'] = 'http://music.163.com/m/song?id={}'.format(id_)
        href = dic['href']

        soup = get_albumpic(href)
        pic = soup.find(class_='u-img')
        dic['album_pic'] = pic['src']

        response = get_lyris(id_)
        dic['lyris'] = response['lrc']['lyric']

        yield dic

def get_albumpic(href):
    url = href
    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': '_ntes_nnid=a19975546950292418732f517c987ebb,1525955180755; _ntes_nuid=a19975546950292418732f517c987ebb; __f_=1525955759964; __e_=1525955826425; _iuqxldmzr_=32; WM_TID=DsfwNEpfeqgBZQK9SCRG47HtHbpkza1m; __utmz=94650624.1525965955.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=94650624.1410656019.1525965718.1525965955.1526034887.3; __utmc=94650624; JSESSIONID-WYYY=1vTzS%2B2e6Vko5IZuZYQ4m8gWQNEpJRGw9AY%2BcxWO7VfvAIRbt9OaYkvT3%2B7H9lDYDg6Utr8eoqc04KeQakhmUQqassojvVThWYZoAqlHFUZbKw3omIUvqwKM3nhXjcUb1eR%2BwHVdHuST1mClBqoCynW5hsV5rlz7AeKl6Z1fKJBv4ukk%3A1526040168634; __utmb=94650624.23.10.1526034887',
        'Host': 'music.163.com',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3423.2 Mobile Safari/537.36'
    }
    response = requests.get(url=url,headers=headers).text
    soup = BeautifulSoup(response,'lxml')
    return soup

def get_lyris(id_):
    url = 'http://music.163.com/api/song/lyric?id={}&lv=1&kv=1&tv=-1'.format(id_)
    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'music.163.com',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3423.2 Mobile Safari/537.36'
    }
    response = requests.get(url=url,headers=headers).text
    response = json.loads(response)
    return response

def load_jsonf(response):
    soup = BeautifulSoup(response,'lxml')
    content = soup.p.text
    con = json.loads(content)
    return con['result']

def read_jsonf(data):
    lst = []
    for n in data:
        lst.append(n)
    music_data = json.dumps(lst)
    with open ('data.json','a') as f:
        f.write(music_data)
        f.close()

def main():
    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': '_ntes_nnid=a19975546950292418732f517c987ebb,1525955180755; _ntes_nuid=a19975546950292418732f517c987ebb; __f_=1525955759964; __e_=1525955826425; _iuqxldmzr_=32; WM_TID=DsfwNEpfeqgBZQK9SCRG47HtHbpkza1m; __utmz=94650624.1525965955.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=94650624.1410656019.1525965718.1525965955.1526034887.3; __utmc=94650624; JSESSIONID-WYYY=1vTzS%2B2e6Vko5IZuZYQ4m8gWQNEpJRGw9AY%2BcxWO7VfvAIRbt9OaYkvT3%2B7H9lDYDg6Utr8eoqc04KeQakhmUQqassojvVThWYZoAqlHFUZbKw3omIUvqwKM3nhXjcUb1eR%2BwHVdHuST1mClBqoCynW5hsV5rlz7AeKl6Z1fKJBv4ukk%3A1526040168634; __utmb=94650624.23.10.1526034887',
        'Host': 'music.163.com',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3423.2 Mobile Safari/537.36'
    }
    params = {
        'params': '/0XrBlSajPi+USV8m9PiS3pwWJCIn3PQpbjCdlngC5E=',
        'encSecKey': '673814b420a1f21fecd37514795cb67a89ca175335184f6e1b9a4023d7ed84aca74ec3d78c24196ebdb31855a436fa1d4a031686abf963c1639339019e715a9efe6b4b6429a416e218cf5af2270d6b7a773e3a9edaae8f20add7c029878edda74c89298aef84d609bc2d9ca059de4845f3cdd8db96e434e42c1b68081885770e'
    }
    sy_url = 'http://music.163.com/weapi/personalized/newsong'
    
    response = get_response(sy_url,params,headers)
    zx_music = load_jsonf(response)
    data = get_info(zx_music)
    read_jsonf(data)

if __name__ == '__main__':
    main()

