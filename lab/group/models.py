from django.db import models
# Create your models here.


class StudentGroup(models.Model):
    """
    学员群组划分
    """
    # group_id = models.IntegerField(verbose_name='群组ID', default=1)
    group_name = models.CharField(verbose_name='群组名', max_length=30)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    group_note = models.CharField(verbose_name='群组备注',default='', max_length=255)
