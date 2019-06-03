from django.contrib import admin
from sign.models import Event,Guest

# Register your models here.

# 创建EventAdmin类ModelAdmin，只定义一项list_display，是一个字段名称的数组，
# 用于定义要在列表中显示那些字段，这些字段前提是在Event类中有的字段
class EventAdmin(admin.ModelAdmin):
    list_display = ('id','name','status','address','start_time')
#     快速生成搜索栏和过滤器
# 搜索栏
    search_fields = ['name']
#     过滤器
    list_filter = ['status']

class GuestAdmin(admin.ModelAdmin):
    list_display = ('realname','phone','email','sign','create_time','event')
    search_fields = ['realname','phone']
    list_filter = ['sign']

# 通知admin管理工具为这些模块逐一提供界面
admin.site.register(Event,EventAdmin)
admin.site.register(Guest,GuestAdmin)













