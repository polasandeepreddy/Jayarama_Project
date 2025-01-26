from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from django.utils import timezone
from django import forms

# Create your models here.
class Bank(models.Model):
    Name = models.CharField(max_length=30)
    Branch = models.CharField(max_length=50)
    IFSC = models.CharField(max_length=11, validators=[RegexValidator(regex='[A-Z]{4}0[A-Z0-9]{6}', message='Invalid IFSC code')])

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name_plural = "Banks"

class Category(models.Model):
    Property_Title = models.CharField(max_length=30)

    def __str__(self):
        return self.Property_Title

    class Meta:
        verbose_name_plural = "Categories"

class Property(models.Model):
    Auction_id = models.CharField(max_length=10)
    Title = models.CharField(max_length=200)
    Bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name = "properties")
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
   
    Auction_end_date = models.DateTimeField(default=timezone.now)
     # Adding the created_at field to track when the property is added
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation

    Image = models.ImageField(upload_to='images/', default='default.jpg')

    def _str_(self):
        return self.Auction_id

    def get_absolute_url(self):
        return reverse('property_detail', args=[str(self.id)])

class Meta:
    verbose_name_plural = "properties"

