from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from apps.users.models import (
    User,
    Organization
)

class StaffAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (_("Permissions"), {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions", "role"),
            },
         ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("email",)


class OrganizationAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": ("name", "owner", "documents")
        }),
        (_("Статус"), {
            "fields": ("is_active",)
        }),
        (_("Временные метки"), {
            "fields": ("created_at",)
        }),
    )

    readonly_fields = ("created_at",)
    list_display = ("id", "name", "owner", "is_active", "created_at")
    search_fields = ("name", "owner__email")
    ordering = ("-created_at",)
    list_filter = ("is_active", "created_at")


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(User, StaffAdmin)