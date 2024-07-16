from django.contrib import admin
from .models import SystemUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class SystemUserCreationForm(UserCreationForm):
    class Meta:
        model = SystemUser
        fields = ('email',)


class SystemUserChangeForm(UserChangeForm):
    class Meta:
        model = SystemUser
        fields = ('email', 'is_staff', 'is_email_confirmed', 'is_superuser', 'groups', 'user_permissions')


class SystemUserAdmin(BaseUserAdmin):
    form = SystemUserChangeForm
    add_form = SystemUserCreationForm

    list_display = ('email', 'is_email_confirmed', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_email_confirmed')
    readonly_fields = ('last_login',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_email_confirmed', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(SystemUser, SystemUserAdmin)
