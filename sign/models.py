from django.db import models

# Create your models here.
# 发布会

class Event(models.Model):
#     发布会标题
    name = models.CharField(max_length=100)
# 参加人数
    limit = models.IntegerField()
# 状态
    status = models.BooleanField()
# 地址
    address = models.CharField(max_length=200)
# 发布会时间
    start_time = models.DateTimeField('events time')
# 创建时间（自动获取当前时间）
    create_time = models.DateTimeField(auto_now=True)

# 在后台显示的字段
    def __str__(self):
        return self.name

# 嘉宾表
class Guest(models.Model):
#     关联发布会的ID
    event = models.ForeignKey(Event)
# 姓名
    realname = models.CharField(max_length=64)
# 手机号
    phone = models.CharField(max_length=16)
# 邮箱
    email = models.EmailField()
# 签到状态
    sign = models.BooleanField()
# 创建时间（自动获取当前时间）
    create_time = models.DateTimeField(auto_now=True)

# Mete是Django的内部类，用来定义一些Django模型类的行为特性，unique_together用于设置两个字段为联合主键
    class Meta:
        unique_together = ("event","phone")

    def __str__(self):
        return self.realname
















