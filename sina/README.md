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

5：分析并保存数据，用正则或者BS4去匹配（get_comment_content）

6：评论情感解析【1：snownlp   2:腾讯文智】

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
