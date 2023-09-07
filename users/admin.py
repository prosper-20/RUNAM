from django.contrib import admin

# Register your models here.
from .models import CustomUser, Profile, Referral

admin.site.register(CustomUser)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user"]
    search_fields = ["user"]



@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ["user", "code", "used"]
