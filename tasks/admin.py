from django.contrib import admin
from .models import Task, TaskReview, Keyword, Bidder, NewBidder, Support, Category, Shop, ShopProfile, ShopImages, ShopDocuments


class ShopProfileAdmin(admin.ModelAdmin):
    list_display = ["shop"]
    search_fields = ["shop"]
    list_filter = ["shop"]


admin.site.register(ShopProfile, ShopProfileAdmin)


@admin.register(Shop)
class ShopAmin(admin.ModelAdmin):
    list_display = ["name", "location", "rating"]
    prepopulated_fields = {'slug': ('name',)}



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active", "being_delivered", "picked_up", "completed"]
    list_filter = ["completed", "sender", 'is_active', "paid", "date_posted"]
    search_fields = ["name", "body"]


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Bidder)
class BidderAdmin(admin.ModelAdmin):
    list_display = ["task","user", "message"]


@admin.register(NewBidder)
class BidderAdmin(admin.ModelAdmin):
    list_display = ["task","user", "message"]





@admin.register(TaskReview)
class TaskRevieewAdmin(admin.ModelAdmin):
    list_display = ["task", "errander", "errandee", "comment"]



@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    list_display = ["user", "category"]
    list_filter = ["user", "category"]
    search_fields = ["user", "category"]
    
