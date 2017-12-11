import requests
from bs4 import BeautifulSoup
import json
import threading
# from time import sleep

root_url = 'http://crossincode.com'
cookies = {
    # 间隔更新cookie,代优化
    'Cookie': 'UM_distinctid=15fed6e0c25bf-0d92fdaae2f5b2-7b113d-100200-15fed6e0c2646a; '
              'sessionid=vivze4x49mnb16br8plvdo32ciaw2tip; '
              'csrftoken=51uTgkCNv1U6PekLiRp1xcnUpu80sbEy'
}
error = []


def _get_answer(url):
    """
    储存答案及描述
    """
    r = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(r.text, 'html.parser')
    desc = soup.find(class_='panel-body').prettify()
    # print(desc.prettify())
    print('DESC-len:\t', len(desc))
    answer = soup.find(class_='panel-footer').prettify()
    # print(answer.prettify())
    # answer = ''.join(answer.stripped_strings)
    print('ANSWER-len:\t', len(answer))
    return desc, answer


def _save_item(title, desc, answer):
    """
    保存条目
    """
    url = 'http://127.0.0.1:8000/faq/save'
    data = {
        'title': title,
        'desc': desc,
        'answer': answer,
    }
    r = requests.post(url, data=data)
    reply = json.loads(r.text)
    print('SAVE-item:\t', reply)
    return reply.get('qid')


def _save_keyword(key, qid):
    """
    保存关键字
    """
    url = 'http://127.0.0.1:8000/faq/k2qa'
    data = {
        'key': key,
        'qid': qid
    }
    r = requests.get(url, params=data)
    reply = json.loads(r.text)
    print('SAVE-key:\t', reply)


def thr_item(item):
    """
    信息储存线程函数
    """
    h4 = item.find('h4')
    title = h4.string
    item_url = h4.parent['href']
    tags = item.find_all('a', class_='tag')
    print('TITLE:\t', title)
    print('URL:\t', root_url + item_url)
    desc, answer = _get_answer(root_url + item_url)
    qid = _save_item(title, desc, answer)
    if qid:
        for tag in tags:
            print('TAG:\t', tag.string)
            _save_keyword(tag, qid)
    else:
        error.append(item_url)


def faq_spider():
    """
    爬取学习站问答记录并调用 qa_sys 接口储存信息
    """
    r = requests.get(root_url + '/faq/')
    soup = BeautifulSoup(r.text, 'html.parser')
    items = soup.find_all(attrs={'class': 'list-group-item'})
    tts = []
    numb = 0
    for item in items:
        numb += 1
        thr = threading.Thread(target=thr_item, args=(item,))
        tts.append(thr)
        if numb > 4:
            [t.start() for t in tts]
            [t.join() for t in tts]
            numb = 0
            tts = []

if __name__ == '__main__':
    faq_spider()
    for i in error:
        print(i)