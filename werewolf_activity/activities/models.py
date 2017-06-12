from django.db import models

from django.utils import timezone

import json

# Create your models here.
class Activity(models.Model):
    name = models.CharField("名字", max_length=200, blank=False)
    start = models.DateTimeField("开始", auto_now=False)
    end = models.DateTimeField("结束", auto_now=False)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("最后修改时间", auto_now=True)
    address = models.TextField("活动地址")
    creator_avatar = models.TextField("创建者头像地址", blank=True, null=True)
    creator_nickname = models.CharField("创建者昵称", blank=True, null=True, max_length=200)
    creator_open_id = models.TextField("创建者微信openID", blank=True, null=True)
    price = models.DecimalField("费用", default=0, decimal_places=2, max_digits=5)

    def __str__(self):
        return "%s（%s - %s）" % (self.name, self.start, self.end)
    
    def has_expired(self):
        return self.end < timezone.now()
    
    def to_plain(self):
        normal_attrs = ["name", "address", "creator_avatar", "creator_nickname", "price"]
        datetime_attrs = ["start", "end", "created_at"]
        plain = {}
        for attr in normal_attrs:
            plain = self[attr]
        for attr in datetime_attrs:
            plain = datetime_to_unix(self[attr])
        return plain

    class Meta:
        verbose_name = '狼人杀活动'
        verbose_name_plural = '狼人杀活动'
    pass


def datetime_to_unix(dt):
    if dt.year < 1900:
        return 0
    return int(dt.strftime("%s"))