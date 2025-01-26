from django.contrib import admin
from .models import *

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ['Name', 'Branch', 'IFSC']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['Property_Title']

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['Auction_id', 'Title', 'Bank', 'Property_Title', 'Description', 'Location', 'City', 'State', 'Amount', 'Reserve_price', 'EMD_amount', 'Bid_increment', 'EMD_submission_date', 'Auction_start_date', 'Auction_end_date', 'Image']