import datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class QAItem(models.Model):
    title = models.CharField(max_length=255, verbose_name='题目')
    desc = models.TextField(verbose_name='描述', default='描述')
    answer = models.TextField(verbose_name='答案')

    def __str__(self):
        return self.title


class KeyItem(models.Model):
    keyword = models.CharField(max_length=60, verbose_name='关键字')

    def __str__(self):
        return self.keyword


class KeyToQA(models.Model):
    keyword = models.ForeignKey(KeyItem, on_delete=models.CASCADE, related_name='k2qa')
    qa = models.ForeignKey(QAItem, on_delete=models.CASCADE, related_name='k2qa')
    times = models.IntegerField(verbose_name='查询次数', default=0)

    def __str__(self):
        return self.times.__str__() + '-' + self.keyword.keyword + '-' + self.qa.title


class Comment(models.Model):
    qaitem = models.ForeignKey(to=QAItem, related_name="comments")
    description = models.TextField(default="")

    def __str__(self):
        return self.title
