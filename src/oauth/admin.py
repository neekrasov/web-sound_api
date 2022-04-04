from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class MyUserAdmin(UserAdmin):
    model = User
    list_display = ('id', 'email', 'display_name', 'join_date', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active',)
    search_fields = ('id', 'email', 'is_staff', 'is_superuser',)
    ordering = ('id',)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("display_name", "country", "city", "bio")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                ),
            },
        ),
    )


admin.site.register(User, MyUserAdmin)
