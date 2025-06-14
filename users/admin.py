from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Payments


@admin.register(User)
class MaterialsAdmin(UserAdmin):
    list_display = ('id', 'email', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email',)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "usable_password", "password1", "password2"),
            },
        ),
    )
    ordering = ('pk', )
    readonly_fields = ("last_login", "date_joined")


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'lesson', 'payment_date', 'payment_amount',
                    'payment_method')
    list_filter = ('id', 'user','course', 'lesson',)
    search_fields = ('user',)
