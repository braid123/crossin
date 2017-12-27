自动问答服务系统文档说明
-----
代码地址： AutoQASystem

主要技术： [Python3.5](https://www.python.org/downloads/release/python-352/)+
           [django1.10](https://www.djangoproject.com/start/)+ [mysql5.7](https://dev.mysql.com/doc/)+ [whoosh](https://whoosh.readthedocs.io/en/latest/)+ [jieba](https://github.com/fxsjy/jieba)+ [haystack](http://django-haystack.readthedocs.io/en/master/)+ [requests](http://cn.python-requests.org/zh_CN/latest/)/[beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/)

参考资料： Whoosh + jieba 中文检索、实现Django的全文检索功能 

django + haystack:<br /> 
项目主体网站，提供问题、关键字等，查询、储存接口

requests + beautifulsoup:<br /> 
问题收集爬虫，提供问题数据

主要文件说明：

[qa_spider.py](https://github.com/braid123/crossin/blob/master/AutoQASystem/qa_index/qa_spider.py)——常见问答的抓取及存储，后续要加入更多问答数据获取爬虫

[views.py](https://github.com/braid123/crossin/blob/master/AutoQASystem/qa_index/views.py)——接口函数部分可以复用，已完成问题的新增及评论的添加

[models.py](https://github.com/braid123/crossin/blob/master/AutoQASystem/qa_index/models.py)——问答及评论的数据模型定义

[urls.py](https://github.com/braid123/crossin/blob/master/AutoQASystem/qa_index/urls.py)——定义views.py中相关的网址路由

[templates](https://github.com/braid123/crossin/tree/master/AutoQASystem/qa_index/templates)——问答与评论的展示