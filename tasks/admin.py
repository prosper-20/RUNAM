from django.contrib import admin
from .models import Task, TaskReview, Keyword, Bidder, NewBidder


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active", "being_delivered", "picked_up", "completed"]
    list_filter = ["completed", "sender", 'is_active', "paid"]
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
    
