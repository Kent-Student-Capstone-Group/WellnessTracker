from django.contrib import admin
from .models import User, Group, Message, DailyReport, UserGroupRequest, UserGroupJoinTable

# Register your models here.

admin.site.register(User)
admin.site.register(Group)
admin.site.register(Message)
admin.site.register(DailyReport)
admin.site.register(UserGroupRequest)
admin.site.register(UserGroupJoinTable)