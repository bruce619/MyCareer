from django.contrib import admin
from .models import Profile, User
from django.contrib.auth.admin import UserAdmin


class AccountAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email', 'datetimecreated', 'last_login', 'is_human_resources', 'is_applicant', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('datetimecreated', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    ordering = ('email',)
    fieldsets = (
        (None,
         {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'datetimecreated')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_human_resources', 'is_applicant',)}),
                 )


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date', 'phone_number')
    search_fields = ('user',)
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    ordering = ('user',)
    fieldsets = (
        (None,
         {'fields': ('user', 'image')}),
        ('Personal info', {'fields': ('sex', 'birth_date', 'phone_number', 'nationality')}),
    )


admin.site.register(Profile, ProfileAdmin)
admin.site.register(User, AccountAdmin)
