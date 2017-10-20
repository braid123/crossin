【1】项目名称：
用Scrapy去抓取一条指定新浪微博的评论并进行情感分析

【2】前期环境准备与文件设置：

安装Python3和Scrapy，数据库选择mongodb

Settings.py：ROBOTSTXT_OBEY = False，数据库配置信息，USER-AGENTS等

pipelines.py：存储自己的数据

item.py：定义抓取数据的表字段，存储需要保存的数据

【3】实现思路和大概步骤：

1：确定爬取微博爬虫爬取网站，优先考虑m站>wap站>PC站。m.weibo.cn

2:打开开发者工具Network，单击微博内容，查看发抓包数据。

3：Request URL:
https://m.weibo.cn/api/comments/show?id=4160547165300149&page=1

4：请求网页Request URL，对返回的json数据进行解析（start_requests）

```    
def start_requests(self):
        single_weibo_id = '4160547165300149'
        post_comment_url = 'https://m.weibo.cn/api/comments/show?id=%s&page=4531' % single_weibo_id
        yield Request(url=post_comment_url, callback=self.get_comment_content) 
```
5：分析并保存数据，用正则或者BS4去匹配（get_comment_content）
```
# 获取评论内容
def get_comment_content(self, response):
    content = json.loads(response.body)
    if content.get('ok') == 1:
        for data in content.get('data'):
            post_id = re.findall('(\d+)', response.url)[0]
            commentid = data.get('id')
            # 将回复后的评论截取出
            text = re.sub('<.*?>', '', data.get('text'))
            text_2 = re.sub(r'.*?@.*?:', '', text)
            reply_text = re.sub('.*?@.*?:', '', re.sub('<.*?>', '', data.get('reply_text', '')))
            like_counts = data.get('like_counts')
            item = CommentItem()
            # 数据保存
            item['id'] = commentid
            item['comment'] = text_2
            item['refer'] = reply_text
            item['post_id'] = post_id
            item['like_counts'] = like_counts
            yield item
```
设立循环条件，取出各页评论：
```
max_page = content.get('max')
page_num_pattern = r'(\d+)'
page_num = re.findall(page_num_pattern, response.url)[1]

if int(max_page) > 1 and int(max_page) > int(page_num):
    post_id_pattern = r'.*?id=(\d+)&page=.*?'
    post_id = re.findall(post_id_pattern, response.url)[0]
    url = 'https://m.weibo.cn/api/comments/show?id=%s&page=%s' % (post_id, str(int(page_num) + 3))
    time.sleep(random.randint(0, 10))
    yield Request(url=url, callback=self.get_comment_content)

```
6：评论情感解析【1：snownlp   2：腾讯文智】

xmltotxt.py:将目录下的 xml 文件中的评论提取并保存于 txt 中，用作训练样本
```          
# 打开xml文档
dom = xml.dom.minidom.parse(file)
# 得到文档元素对象
sentences = dom.getElementsByTagName('sentence')
```
trainmynlp.py: 将训练好的文件存储为 seg.marshal
```
from snownlp import sentiment
sentiment.train('neg.txt', 'pos.txt')
sentiment.save('sentiment.marshal')
```
parsecomment.py:
提取数据库中的评论，并调用 snownlp 分析出每条评论情感值，最后利用 matplotlib 生成
图像
```
for li in textlist:
    s = SnowNLP(li)
    sentimentslist.append(s.sentiments)
fig1 = plt.figure("test")
plt.hist(sentimentslist, bins=np.arange(0, 1, 0.02))
plt.show()
```
nlptencentparse.py:利用腾讯文智提供的 API，分析出情感值

1）对已经存入数据库的数据进行提取
```
conn = pymysql.connect(host='localhost',user='root',password='root',charset="utf8")
with conn:
    cur = conn.cursor()
    # 随机选取表中数据
    cur.execute("SELECT * FROM sina.sinacomment order By Rand()")
    rows = cur.fetchall()
```
2）参考腾讯文智的 API 文档和说明设置参数
```
module = 'wenzhi'
action = 'TextSentiment'
config = {
    'Region': 'ap-guangzhou',
    'secretId': '腾讯云API申请的标识身份的 SecretId',
    'secretKey': '一个 SecretId 对应唯一的 SecretKey',
    'method': 'GET',
    'SignatureMethod': 'HmacSHA1'
}
```
3）调用接口
```
# 调用接口，发起请求
s = service.call(action, action_params)
dejson = json.loads(s)
```
4）生成图像
```
# 创建名为sentiment的figure对象
fig1 = plt.figure("sentiment")
# 生成Histograms直方图
plt.hist(sentimentslist, bins=np.arange(0, 1, 0.02))
# 展示图像
plt.show()
```
7：结论

【snownlp】：
情感值在接近0、1两端以及0.5左右位置频率较高(0.5可能为无法解析出情感值)
![Image text](https://github.com/braid123/crossin/blob/master/sina/sina/snownlp.png)

加入人为数据训练snownlp后，图片任无较大变化
![Image text](https://github.com/braid123/crossin/blob/master/sina/sina/snownlp_addmydata.png)

【腾讯文智】：

![Image text](https://github.com/braid123/crossin/blob/master/sina/sina/%E8%85%BE%E8%AE%AF%E6%96%87%E6%99%BA.png)

腾讯文智抽取1K并过滤掉0.5即无法解析的值：发现负面情绪较多

![Image text](https://github.com/braid123/crossin/blob/master/sina/sina/%E8%85%BE%E8%AE%AF%E6%96%87%E6%99%BA%E9%9A%8F%E6%9C%BA%E6%8A%BD%E5%8F%961K%E5%B9%B6%E8%BF%87%E6%BB%A4.png)
