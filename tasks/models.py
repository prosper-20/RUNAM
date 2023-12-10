from django.db import models
from users.models import CustomUser
from accounts.models import User
import uuid
from decimal import Decimal

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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
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

    class Meta:
        ordering = ("-date_posted",)


    def __str__(self):
        return self.name


class CommissionPercentage(models.Model):
    percentage = models.DecimalField(default=0.10, max_digits=12, decimal_places=2)

    def __str__(self):
        return str(self.percentage)

class Commission(models.Model):
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    
    # def save(self, *args, **kwargs):
    #     # Generate a slug based on the title
    #     self.amount = Decimal(CommissionPercentage.objects.last().percentage) * self.task.bidding_amount
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.task.name 


class DeliveryTask(models.Model):
    tracking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    sender_address = models.TextField()
    recipient_name = models.CharField(max_length=100)
    recipient_address = models.TextField()
    delivery_date = models.DateField(auto_now=True)
    delivery_time = models.TimeField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    package_description = models.TextField(blank=True, null=True)
    package_weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # You can adjust the precision as needed
    is_delivered = models.BooleanField(default=False)
    delivery_notes = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"Delivery {self.tracking_id}"
    

class LabReportTask(models.Model):
    course = models.CharField(max_length=100)
    task_slug = models.SlugField(max_length=200)
    no_of_pages = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    sender = models.ForeignKey(User, related_name="lab_report_sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="lab_report_receiver", on_delete=models.CASCADE, blank=True, null=True)
    extra_notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    task_bidders = models.ManyToManyField("Bidder", related_name="lab_report_bidders", blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.no_of_pages * 100
        super(LabReportTask, self).save(*args, **kwargs)

    def __str__(self):
        return self.task_slug

class LaundryTask(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    task_slug = models.SlugField()
    clothes = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    extra_notes = models.TextField(blank=True, null=True)
    sender = models.ForeignKey(User, related_name="laundry_sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="laundry_receiver", on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    task_bidders = models.ManyToManyField("Bidder", related_name="laundry_bidders", blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()


    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.clothes * 100
        super(LaundryTask, self).save(*args, **kwargs)

    def __str__(self):
        return self.task_slug


    
    # def calculate_price(self):
    #     if self.no_of_pages is not None:
    #         self.price = self.no_of_pages * 100
    #         self.save()

    # def save(self, *args, **kwargs):
    #     self.calculate_price()
    #     super(LabReportTask, self).save(*args, **kwargs)



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
        return self.user.profile.username
    

class NewBidder(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=150)

    def __str__(self):
        return self.CustomUser.CustomUsername

     

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
