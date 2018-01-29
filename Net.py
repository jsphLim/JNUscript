import base64
import re

import requests
import json

from bs4 import BeautifulSoup


def getInfo(session):

    cookie = 'JSESSIONID=' + session
    return requests.post(
        'http://itsm.jnu.edu.cn/itsf/todos/list.action',
        data=json.dumps({'flag': 1}),
        headers={
            'Referer': 'http://itsm.jnu.edu.cn/itsf/edulogin',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Content-Length': '6',
            'Cookie': cookie
        }
    )

def detail(session):

    cookie = 'JSESSIONID=' + session
    return requests.post(
        'http://itsm.jnu.edu.cn/itsf/todos/getEventTodo.action',
        data=json.dumps({'draw':1,'columns[0][data]':'','columns[0][name]':'','columns[0][searchable]':'true','columns[0][orderable]':'false'
        ,'columns[0][search][value]':'','columns[0][search][regex]':'false','columns[1][data]':'STATUS_ID','columns[1][name]':'','columns[1][searchable]':'true'
        ,'columns[1][orderable]':'false','columns[1][search][value]':'','columns[1][search][regex]':'false','columns[2][data]':'APPID','columns[2][name]':''
        ,'columns[2][searchable]':'true','columns[2][orderable]':'false','columns[2][search][value]':'','columns[2][search][regex]':'false','columns[3][data]':'TITLE'
        ,'columns[3][name]':'','columns[3][searchable]':'true','columns[3][orderable]':'false','columns[3][search][value]':'','columns[3][search][regex]':'false'
        ,'columns[4][data]':'CONTACTS_NAME','columns[4][name]':'','columns[4][searchable]':'true','columns[4][orderable]':'false','columns[4][search][value]':''
        ,'columns[4][search][regex]':'false','columns[5][data]':'CONTACTS_PHONE','columns[5][name]':'','columns[5][searchable]':'true','columns[5][orderable]':'false'
        ,'columns[5][search][value]':'','columns[5][search][regex]':'false','columns[6][data]':'OPEN_TIME','columns[6][name]':'','columns[6][searchable]':'true'
        ,'columns[6][orderable]':'false','columns[6][search][value]':'','columns[6][search][regex]':'false','columns[7][data]':'PRIORITY_CODE','columns[7][name]':''
        ,'columns[7][searchable]':'true','columns[7][orderable]':'false','columns[7][search][value]':'','columns[7][search][regex]':'false','start':0,'length':10,'search[value]':''
        ,'search[regex]':'false','listType':''}),
        headers={
            'Referer': 'http://itsm.jnu.edu.cn/itsf/edulogin',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Cookie': cookie
        }
    ).text

def addSecret(strs):
    ss = ''
    for i in strs:
        m = ord(i)
        m+=64
        i = chr(m)
        ss+=i
    return ss

if __name__ == '__main__':
    user = (base64.b64encode(b'学号'))
    print(str(user,'utf-8'))
    password = addSecret('密码')
    print(password)
    str1 = requests.post("http://itsm.jnu.edu.cn/itsf/edulogin",
                        data={'username':user,'password':password},
                        headers={'Referer': 'http://itsm.jnu.edu.cn/itsf/', 'Content-Type': 'application/x-www-form-urlencoded'}).cookies['JSESSIONID']

    html = getInfo(str1).text
    soup = BeautifulSoup(html, 'html.parser')
    res = soup.find_all('p',"index-num")
    nums = re.findall(r'\d+', str(res))
    print("故障报修:"+nums[0])
    print("业务申请:"+nums[1])
    print("问题管理:"+nums[2])
    print("变更管理:"+nums[3])
    print("知识审核:"+nums[4])
    print("计划任务:"+nums[5])

    res = detail(str1)
    res = json.loads(res)
    list = []
    list = res['data']
    for item in list:
        print(item['CONTACTS_NAME']+' '+item['DESCRIPTION'])
