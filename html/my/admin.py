# -*- coding: utf-8 -*-

from my.models import SNType
from django.contrib import admin

admin.site.register(SNType)


from django.contrib import admin
from my.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

class UserProfileInline(admin.StackedInline):
 model = UserProfile
 max_num = 1
 can_delete = False

class UserAdmin(AuthUserAdmin):
 inlines = [UserProfileInline]

# unregister old user admin
admin.site.unregister(User)
# register new user admin
admin.site.register(User, UserAdmin)