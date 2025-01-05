from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email','is_admin_coop', 'is_student', 'is_active')
    list_filter = ('is_admin_coop', 'is_student')
    fieldsets = (
        (None, {'fields': ('email','password')}),
        ('Roles', {'fields': ('is_admin_coop', 'is_student')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_admin_coop', 'is_student', 'is_active'),
        }),
    )
    search_fields = ('email'),
    ordering = ('email',)
