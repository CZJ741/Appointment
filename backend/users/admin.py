from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # 在管理后台中显示的字段
    list_display = ('username', 'email', 'full_name', 'is_active', 'is_staff')
    # 搜索字段
    search_fields = ('username', 'email', 'full_name')
    # 字段集配置
    fieldsets = UserAdmin.fieldsets + (
        ('个人信息', {'fields': ('full_name',)}),
    )
    # 添加用户时的字段配置
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('个人信息', {'fields': ('email', 'full_name')}),
    )
