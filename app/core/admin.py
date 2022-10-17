"""
Django admin customisation
"""
from django.contrib import admin

# Importing UserAdmin as BaseUserAdmin so we can call our custom
# user admin as UserAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# This supports language translation in Django
# Thus translate _('Something')
from django.utils.translation import gettext_lazy as _

# Import our core models
from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users"""

    # Sort by id
    ordering = ["id"]
    # Show selected fields
    list_display = ["email", "name"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser",)}),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    readonly_fields = ["last_login"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


# Load the models in to the admin page
# Register User using our custom UserAdmin
admin.site.register(models.User, UserAdmin)
