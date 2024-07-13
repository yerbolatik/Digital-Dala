from django.contrib import admin
from userauths.models import User, Profile


class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'username', 'email']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user']


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
