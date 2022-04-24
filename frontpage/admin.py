from django.contrib import admin
from .models import UserInfo, Group, Chat, DailyReport, UserGroupRequest, UserGroupJoinTable

# Register your models here.

admin.site.register(UserInfo)
admin.site.register(Group)
admin.site.register(Chat)
admin.site.register(DailyReport)
admin.site.register(UserGroupRequest)
admin.site.register(UserGroupJoinTable)
