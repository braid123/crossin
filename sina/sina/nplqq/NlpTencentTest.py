from QcloudApi.qcloudapi import QcloudApi
import json
'''
module: 设置需要加载的模块
已有的模块列表：
cvm      对应   cvm.api.qcloud.com
cdb      对应   cdb.api.qcloud.com
lb       对应   lb.api.qcloud.com
trade    对应   trade.api.qcloud.com
sec      对应   csec.api.qcloud.com
image    对应   image.api.qcloud.com
monitor  对应   monitor.api.qcloud.com
cdn      对应   cdn.api.qcloud.com
'''
module = 'wenzhi'

'''
action: 对应接口的接口名，请参考wiki文档上对应接口的接口名
'''
action = 'TextSentiment'

'''
config: 云API的公共参数
'''
config = {
    'Region': 'ap-guangzhou',
    'secretId': '',
    'secretKey': '',
    'method': 'GET',
    'SignatureMethod': 'HmacSHA1'
}

# 接口参数
action_params = {
    'content': '鹿晗我知道你是爱鹿饭的，你的好我们都是看在眼里的，你不会照顾自己，找个女朋友也好，'
               '关晓彤我想告诉你:“鹿晗不是你一个人的，而是所有像我一样爱他的鹿饭的，我们都十分羡慕你，'
               '不过你也要知道我们都把鹿晗当自己最重要的人，我们爱他，'
               '所以请你一定要好好去爱他，关心他，保护他，谢谢你',
    'type': 4
}

try:
    service = QcloudApi(module, config)
    # 生成请求的URL，不发起请求
    request_url = service.generateUrl(action, action_params)
    print(request_url)
    # 调用接口，发起请求
    s = service.call(action, action_params)
    print(s)
    dejson = json.loads(s)
    print(dejson["positive"])
except Exception as e:
    import traceback
    print('traceback.format_exc():\n%s' % traceback.format_exc())