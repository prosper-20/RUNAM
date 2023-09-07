from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "is_active", "staff"]
    list_filter = ["is_active"]
    search_fields = ["email"]

admin.site.register(User, UserAdmin)