from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import User

# Register your models here.


UserAdmin.fieldsets += (
    (None, {"fields": ("chat_id", ), }, ),
    )


admin.site.register(User, UserAdmin)

