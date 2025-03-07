from django.db import models
from django.urls import reverse
from django.core.validators import *


class PropertyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')

# Bank Model
class Bank(models.Model):
    Name = models.CharField(max_length=30)
    Branch = models.CharField(max_length=50)
    IFSC = models.CharField(
        max_length=11, 
        validators=[RegexValidator(regex=r'^[A-Z]{4}0[A-Z0-9]{6}$', message='Invalid IFSC code')]
    )

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name_plural = "Banks"

# Category Model
class Category(models.Model):
    Property_Title = models.CharField(max_length=30)

    def __str__(self):
        return self.Property_Title

    class Meta:
        verbose_name_plural = "Categories"

# Property Model
class Property(models.Model):
    Auction_id = models.CharField(max_length=10)
    Title = models.CharField(max_length=200)
    Bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name="properties")
    Property_Title = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="properties")
    Description = models.TextField()
    Location = models.CharField(max_length=30)
    City = models.CharField(max_length=20)
    State = models.CharField(max_length=20)
    Amount = models.DecimalField(max_digits=10, decimal_places=2)
    Reserve_price = models.DecimalField(max_digits=10, decimal_places=2)
    EMD_amount = models.DecimalField(max_digits=10, decimal_places=2)
    Bid_increment = models.DecimalField(max_digits=10, decimal_places=2)
    EMD_submission_date = models.DateTimeField()
    Auction_start_date = models.DateTimeField()
    Auction_end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    Image = models.ImageField(upload_to='images/', default='default.jpg')

    objects = PropertyManager()  # Apply ordering

    def __str__(self):
        return self.Auction_id

    def get_absolute_url(self):
        return reverse('property_detail', args=[str(self.id)])

    class Meta:
        verbose_name_plural = "Properties"


class Items(models.Model):
    item_title = models.CharField(max_length=255)

    def __str__(self):
        return self.item_title

class GoldAuction(models.Model):
    appl_apac = models.CharField(max_length=100)
    party_name = models.CharField(max_length=255, null=True, blank=True)
    item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name="gold_auctions")
    gross_wgt = models.FloatField(validators=[MinValueValidator(0)])
    state = models.CharField(max_length=100)
    sub_location = models.CharField(max_length=100)
    branch_name = models.CharField(max_length=100)
    auction_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.item.item_title} - {self.auction_date}"

    def get_absolute_url(self):
        return reverse('goldauction_detail', args=[str(self.id)])  # Ensure you have a corresponding URL pattern

def get_absolute_url(self):
        return reverse('goldauction_detail', args=[str(self.id)])