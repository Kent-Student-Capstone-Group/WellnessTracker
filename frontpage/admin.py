from django.contrib import admin
from .models import UserInfo, Group, Message, DailyReport, UserGroupRequest, UserGroupJoinTable

# Register your models here.

admin.site.register(UserInfo)
admin.site.register(Group)
admin.site.register(Message)
admin.site.register(DailyReport)
admin.site.register(UserGroupRequest)
admin.site.register(UserGroupJoinTable)