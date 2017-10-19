# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class CommentItem(Item):
    table_name = 'comments'
    id = Field()
    post_id = Field()
    comment = Field()
    refer = Field()
    like_counts = Field()
