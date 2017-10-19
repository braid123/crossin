import numpy as np
import matplotlib.pyplot as plt
import pymysql
from QcloudApi.qcloudapi import QcloudApi
import json

module = 'wenzhi'
action = 'TextSentiment'
config = {
    'Region': 'ap-guangzhou',
    'secretId': '腾讯云API申请的标识身份的 SecretId',
    'secretKey': '一个 SecretId 对应唯一的 SecretKey',
    'method': 'GET',
    'SignatureMethod': 'HmacSHA1'
}


def SelectDataFromMysql():
    commentlist = []
    textlist = []
    conn = pymysql.connect(host='localhost',user='root',password='root',charset="utf8")
    with conn:
        cur = conn.cursor()
        # 随机选取表中数据
        cur.execute("SELECT * FROM sina.sinacomment order By Rand()")
        rows = cur.fetchall()
        for row in rows:
            row = list(row)
            if row not in commentlist:
                commentlist.append([row[0], row[1], row[2], row[3], row[4]])
                id = row[0]
                post_id = row[1]
                comment = row[2]
                refer = row[3]
                like_counts = row[4]
                if comment:
                    # 将评论添加到textlist中
                    textlist.append(comment)
                print("id:%s post_id:%s comment:%s refer:%s like_counts:%s"
                         % (id, post_id, comment, refer, like_counts))
    return textlist


def NlpTencent(textlist):
    sentimentslist = []
    iTotalCount = 0
    iSuccessCount = 0
    iFailCount = 0
    iNoSentiment = 0
    for li in textlist:
        service = QcloudApi(module, config)
        action_params = {
            'content': li,
            'type': 4
        }
        # 生成请求的URL，不发起请求
        # request_url = service.generateUrl(action, action_params)
        # 调用接口，发起请求
        s = service.call(action, action_params)
        dejson = json.loads(s)
        # 调用次数多了以后就会报错，4500重放攻击/504服务故障/5100资源操作失败
        if dejson["code"] != 0:
            print('调用失败，此条不处理')
            iFailCount += 1
        else:
            iSuccessCount += 1
            if dejson["positive"] == 0.5:
                print('情绪值无法解析出')
                iNoSentiment += 1
            else:
                print(dejson["positive"])
                print(dejson["negative"])
                print(dejson["code"])
                print(dejson["message"])
                sentimentslist.append(dejson["positive"])
        iTotalCount += 1
        print('调用次数 iTotalCount:', iTotalCount)
        print('调用成功次数 iSuccessCount:', iSuccessCount)
        print('情绪值无法解析次数 iNoSentiment:', iNoSentiment)
        print('调用失败次数 iFailCount:', iFailCount)
        if iTotalCount > 1000:
            break
    # 创建名为sentiment的figure对象
    fig1 = plt.figure("sentiment")
    # 生成Histograms直方图
    plt.hist(sentimentslist, bins=np.arange(0, 1, 0.02))
    # 展示图像
    plt.show()


if __name__ == '__main__':
    textlist = SelectDataFromMysql()
    NlpTencent(textlist)
