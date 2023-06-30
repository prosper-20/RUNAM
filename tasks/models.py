from django.db import models
from users.models import User
import uuid


class Keyword(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.name 


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    



class Task(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    keywords = models.ManyToManyField(Keyword, blank=True)
    bidding_amount = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="task_images", blank=True, null=True)
    sender =models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    task_bidders = models.ManyToManyField("Bidder", related_name="single_task_bidders", blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    picked_up = models.BooleanField(default=False)
    being_delivered =models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    messenger = models.ForeignKey(User, related_name="the_task_messenger", on_delete=models.CASCADE, blank=True, null=True)
    shop = models.ForeignKey("Shop", on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return self.name
    

class TaskImages(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="task_images", blank=True, null=True)

    def __str__(self):
        return self.task.name 
    

class Bidder(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=150)

    def __str__(self):
        return self.user.username
    

class NewBidder(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=150)

    def __str__(self):
        return self.user.username

     

class TaskReview(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    errander = models.ForeignKey(User, related_name="task_errander", on_delete=models.CASCADE, blank=True, null=True)
    errandee = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.task}"
    
    



class AcceptTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="tasks")
    receiver = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE)
    time_picked = models.DateTimeField(auto_now_add=True)
    receiver_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.task



SUPPORT_CATEGORY = (
    ("Inquiry", "Inquiry"),
    ("Complaint", "Complaint"),
    ("Others", "Others")
)
    


class Support(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True)
    category = models.CharField(choices=SUPPORT_CATEGORY, max_length=20)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username
    


class Shop(models.Model):
    owner = models.ForeignKey(User, related_name="the_shop_owner", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    location = models.CharField(max_length=100)
    tasks = models.ManyToManyField(Task, related_name="shop_subscribers", blank=True)
    subscribers = models.ManyToManyField(User, blank=True)
    rating = models.CharField(max_length=10, default=10)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ShopImages(models.Model):
    image = models.FileField(upload_to="shop_images")

class ShopDocuments(models.Model):
    document = models.FileField(upload_to="shop_documents")

class ShopProfile(models.Model):
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)
    other_images = models.ManyToManyField(ShopImages, blank=True)
    documents = models.ManyToManyField(ShopDocuments)

    def __str__(self):
        return f"{self.shop.name} profile"
