from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUserModel, Profile

class CustomUserAdmin(UserAdmin):
    model = CustomUserModel
    list_display = ('email', 'username', 'is_superuser', 'is_active','is_verified')
    list_filter = ('email','is_superuser', 'is_active','is_verified')
    search_fields = ('email', 'username')
    ordering = ('email',)
    fieldsets = (
        ('Authentication', {
            "fields": ('username','email','password'),
        }),
        ('Permissions', {
            "fields": ('is_staff','is_active','is_superuser','is_verified'),
        }),
        ('Groups & Permissions', {
            "fields": ('groups','user_permissions'),
        }),
        ('Important dates', {
            "fields": ('last_login','date_joined'),
        }),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email","username","password1","password2","is_staff","is_active","is_superuser","is_verified")
        }),
    )

admin.site.register(Profile)
admin.site.register(CustomUserModel, CustomUserAdmin)
