from django.contrib import admin
from .models import Role, Permission, RolePermission, UserAccount, UserAccessLogs

# Register your models here.
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(RolePermission)
admin.site.register(UserAccount)
admin.site.register(UserAccessLogs)
