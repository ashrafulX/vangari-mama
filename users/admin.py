from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "user_permissions":
            kwargs["queryset"] = (
                db_field.remote_field.model.objects
                .select_related("content_type")
            )

        return super().formfield_for_manytomany(
            db_field,
            request,
            **kwargs
        )


admin.site.register(CustomUser, CustomUserAdmin)