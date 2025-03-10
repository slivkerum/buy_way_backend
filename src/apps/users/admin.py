from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):


    model = User
    list_display = ("email", "phone", "is_seller", "is_staff", "date_joined")
    search_fields = ("email", "phone")
    ordering = ("-date_joined",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Личная информация", {"fields": ("phone",)}),
        ("Разрешения", {"fields": ("is_active", "is_staff", "is_superuser", "is_seller")}),
        ("Даты", {"fields": ("date_joined",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "phone", "is_seller", "is_staff"),
        }),
    )

    filter_horizontal = ()
