from django.contrib import admin
from .models import (
    Task, 
    TaskReview, 
    Keyword, 
    Bidder, 
    NewBidder, 
    Support, 
    Category, 
    Shop, 
    ShopProfile, 
    ShopImages, 
    ShopDocuments, 
    DeliveryTask, 
    LabReportTask,
    LaundryTask)

from .models import CommissionPercentage, Commission

admin.site.register(Commission)

admin.site.register(CommissionPercentage)

@admin.register(LaundryTask)
class LaundryTaskAdmin(admin.ModelAdmin):
    list_display = ["sender", "clothes", "price", "receiver"]
    list_filter = ["sender", "clothes",]
    prepopulated_fields = {"task_slug": ("clothes", "price", "due_date")}
    list_editable = ("clothes",)



class LabReportTaskAdmin(admin.ModelAdmin):
    list_display = ["course", "no_of_pages", "sender", "receiver"]
    list_filter = ["course"]
    list_editable = ["no_of_pages"]
    prepopulated_fields = {"task_slug": ("course",)}


admin.site.register(LabReportTask, LabReportTaskAdmin)
    

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
    
