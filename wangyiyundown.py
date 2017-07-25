#coding=utf-8
from Crypto.Cipher import AES
import base64
import requests
import json
import urllib,urllib2
import re



headers={
    'Cookie':'appver=2.0.2;',
    'Referer':'http://music.163.com/'
    }

def AES_encrypt(text,key,iv):
    encry=AES.new(key,AES.MODE_CBC,iv)
    pad=16-len(text)%16 #填充为16倍数
    text=text+pad*chr(pad)
    encrypt_text=encry.encrypt(text)
    encrypt_text=base64.b64encode(encrypt_text)
    return encrypt_text

def get_param():
    iv="0102030405060708"
    first_key=forth_param
    second_key=16*'F' #这个对应a函数，直接不随机选取16个F，用于二次加密
    encrypt_text=AES_encrypt(first_param,first_key, iv)
    encrypt_text=AES_encrypt(encrypt_text,second_key, iv)
    return encrypt_text

def get_SecKey():
    SecKey='257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c'
    return SecKey


def get_json(url,params,SecKey):
    data={"params":params,
          "encSecKey":SecKey

        }
    req=requests.post(url,headers=headers,data=data)
    return req.content

def auto_down(url,filename):
    try:
        urllib.urlretrieve(url,filename)
    except urllib.ContentTooShortError:
        print 'The song has no download(perhaps it need buy).Reloading.'
        auto_down(url,filename)

if __name__=="__main__":
    url='http://music.163.com/weapi/song/enhance/player/url?csrf_token='
    #url2='http://music.163.com/weapi/v3/song/detail?csrf_token='
    while(1):
        music_id=raw_input(unicode('请输入所要下载的音乐ID:','utf-8').encode('gbk'))
        first_param="{\"ids\":\"["+music_id+"]\",\"br\":128000,\"csrf_token\":\"\"}"
        second_param="010001"
        third_param='00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        forth_param='0CoJUm6Qyw8W8jud'
        params=get_param()
        SecKey=get_SecKey()
        json_text=get_json(url,params,SecKey)
        json_dict=json.loads(json_text)
        #print json_dict['data'][0]['url']#获取音乐地址
        down_url=json_dict['data'][0]['url']#获取音乐地址
        f=urllib.urlopen('http://music.163.com/#/song?id='+music_id)
        concent=f.read()
        res_em=r'<em class=\"f-ff2\">(.*?)</em>'
        m_em=re.findall(res_em,concent)
        down_music_name=''.join(m_em) #获取文件名
        down_music_name=down_music_name.replace('/',' ')
        down_music_name=unicode(down_music_name,'utf-8')
        #<em class="f-ff2">Numb</em
        try:
            save_name=r'd:/downmusic/'+down_music_name+'.mp3'
            auto_down(down_url, save_name)
        except Exception,e:
            print e.message
