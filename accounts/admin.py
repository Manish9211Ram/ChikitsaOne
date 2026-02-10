from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Hospital, Role

class UserAdmin(BaseUserAdmin):
    # Customize UserAdmin to show custom fields
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'department')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Hospital Management', {'fields': ('hospital', 'roles')}),
    )
    list_display = ('email', 'first_name', 'last_name', 'hospital', 'phone', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    list_filter = ('hospital', 'is_staff', 'roles')

admin.site.register(User, UserAdmin)

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'status', 'admin_email')
    list_filter = ('status',)
    search_fields = ('name', 'domain', 'admin_email')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
