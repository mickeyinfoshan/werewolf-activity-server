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
    max_participants = models.IntegerField("最大参与人数", default=15)
    description = models.TextField("活动描述", blank=True, null=True)

    def __str__(self):
        return "%s（%s - %s）" % (self.name, self.start, self.end)
    
    def has_expired(self):
        return self.end < timezone.now()
    
    def get_datetime_fields(self):
        return ["start", "end", "created_at", "updated_at"]

    class Meta:
        verbose_name = '狼人杀活动'
        verbose_name_plural = '狼人杀活动'
    pass

class Participation(models.Model):
    user_open_id = models.TextField("参与者微信OpenID")
    user_avatar = models.TextField("参与者头像")
    user_nickname = models.CharField("参与者昵称", max_length=200)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    created_at = models.DateTimeField("参与时间", auto_now_add=True)
    comment = models.TextField("留言", null=True, blank=True)
    paid = models.BooleanField("已付款", default=False)

    def __str__(self):
        return "%s - %s" % (self.activity.__str__(), self.user_nickname)
    
    def get_datetime_fields(self):
        return ["created_at"]
    
    class Meta:
        verbose_name = "活动参与"
        verbose_name_plural = "活动参与"