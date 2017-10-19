from .sql import Sql
from ..items import CommentItem

class SinaPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, CommentItem):
            id = item['id']
            ret = Sql.select_id(id)
            if ret[0] == 1:
                print('已经存在了')
                pass
            else:
                post_id = item['post_id']
                comment = item['comment']
                refer = item['refer']
                like_counts = item['like_counts']
                print('评论id:', item['id'])
                print('评论:', item['comment'])
                print('引用:', item['refer'])
                print('点赞数:', item['like_counts'])
                Sql.insert_sina_comment(id, post_id, comment, refer, like_counts)
            return item