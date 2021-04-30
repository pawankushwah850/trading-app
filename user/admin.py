from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import *


@admin.register(Referral)
class CustomReferralAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Referral._meta.fields]


@admin.register(Notification)
class CustomNotificationAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Notification._meta.fields]


class CustomUserAdmin(UserAdmin):
    list_display = [f.name for f in User._meta.fields]
    ordering = ('created_at',)


admin.site.register(User, CustomUserAdmin)
