from django.contrib import admin

# Register your models here.
from .models import User, Profile, Referral

admin.site.register(User)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user"]
    search_fields = ["user"]



@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ["user", "code", "used"]
