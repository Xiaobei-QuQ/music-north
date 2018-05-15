from bs4 import BeautifulSoup
import requests
import re
import json


def get_response(url, params, headers):
    response = requests.post(url=url, headers=headers, data=params).text
    return response

def get_info(hotsongs):
    for i in range(20):
        dic = {}
        songsinfo = hotsongs['playlist']['tracks'][i]
        dic['name'] = songsinfo['name']
        id = songsinfo['id']
        dic['id'] = id
        singer = ''
        for n in songsinfo['ar']:
            singer = singer + n['name'] +' '
        dic['singer'] = singer
        dic['album'] = songsinfo['al']['name']
        dic['album_pic'] = songsinfo['al']['picUrl']
        dic['href'] = 'http://music.163.com/m/song?id={}'.format(id)

        response = get_lyris(id)
        dic['lyris'] = response['lrc']['lyric']

        yield dic

def get_lyris(id):
    url = 'http://music.163.com/api/song/lyric?id={}&lv=1&kv=1&tv=-1'.format(id)
    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'music.163.com',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3423.2 Mobile Safari/537.36'
    }
    response = requests.get(url=url,headers=headers).text
    response = json.loads(response)
    return response

def save_jsonf(data):
    lst = []
    for n in data:
        lst.append(n)
    music_data = json.dumps(lst)
    with open ('data_hotsongs.json','a') as f:
        f.write(music_data)
        f.close()

def main():
    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Origin': 'http://music.163.com',
        'Referer': 'http://music.163.com/m/',
        'Host': 'music.163.com',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3423.2 Mobile Safari/537.36'
    }
    params = {
        'params': 'HgFzrXBaEyCNyZRDfykp35TUGDNNWV+a3yaD5VZG8wLmPDmh2f6VPDRLD+2+yQFO',
        'encSecKey': '3b629684ede056772fe5201f45677bb3e7c3c7980eb04b4b55326fee382c89f3e0646607677fda4bdd79a8b4b23283ac79f63db779f49b81788b3580818f491722cce6078c8d696071607916883edde78c32c5aab3f847ed02f0721236af98db0a8296d75c2421cc8b4d59038c86c817de1a6b42e45189a851185256001e0b44'
    }
    requests_url = 'http://music.163.com/weapi/v3/playlist/detail'

    response = get_response(requests_url, params, headers)
    hotsongs = json.loads(response)
    data = get_info(hotsongs)
    save_jsonf(data)

if __name__ == '__main__':
    main()