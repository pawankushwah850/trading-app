from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import *


@admin.action(description="Make super user")
def make_super_user(modeladmin, request, queryset):
    queryset.update(is_superuser=True)


@admin.action(description="Make normal user")
def make_normal_user(modeladmin, request, queryset):
    queryset.update(is_superuser=False)


IGNORE_FIELDS = ['id']


@admin.register(Referral)
class CustomReferralAdmin(admin.ModelAdmin):
    readonly_fields = list_display = sorted([f.name for f in Referral._meta.fields \
                                             if (f.name not in IGNORE_FIELDS)])[::-1]
    ordering = ('-created_at',)
    search_fields = ('referred_to__email', 'referred_by__email',)
    list_filter = ('created_at',)
    fieldsets = (
        (('Refer Information'), {
            'fields': ('referred_to', 'referred_by',)
        }),
        (('Creadted dates'), {'fields': ('created_at',)}),
    )


IGNORE_FIELDS = ['id']


@admin.register(Notification)
class CustomNotificationAdmin(admin.ModelAdmin):
    list_display = sorted([f.name for f in Notification._meta.fields if (f.name not in IGNORE_FIELDS)])[::-1]
    ordering = ('-created_at',)
    readonly_fields = [f.name for f in Notification._meta.fields]
    list_filter = ('category',)
    search_fields = ('user__email',)
    fieldsets = (
        (('Notification info'), {
            'fields': ('user', 'message',)
        }),
        (('Other info'), {
            'fields': ('category', 'is_ack',)
        }),
        (('Creadted dates'), {'fields': ('created_at',)}),
    )


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['name', 'email', 'phone_number', 'verification_status',
                    'language', 'last_updated']
    ordering = ('-created_at', '-last_updated',)
    search_fields = ('name', 'email', 'phone_number',)
    list_filter = ('last_login', 'is_superuser', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email',)}),
        (('Personal info'), {'fields': ('name', 'profile_photo', 'user_role', 'phone_number',
                                        'date_of_birth', 'language', 'identity_document',)}),
        (('Permissions'), {
            'fields': ('verification_status', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined',)}),
    )
    change_list_template = 'user/change_list_graph.html'
    actions = (make_super_user, make_normal_user,)
