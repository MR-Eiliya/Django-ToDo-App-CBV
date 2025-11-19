from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUserModel

class CustomUserAdmin(UserAdmin):
    model = CustomUserModel
    list_display = ('email', 'username', 'is_superuser', 'is_active')
    list_filter = ('is_superuser', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)
    fieldsets = (
        ('Authentication', {
            "fields": ('username','email','password'),
        }),
        ('Permissions', {
            "fields": ('is_staff','is_active','is_superuser'),
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
            "fields": ("email","username","password1","password2","is_staff","is_active","is_superuser")
        }),
    )


admin.site.register(CustomUserModel, CustomUserAdmin)
