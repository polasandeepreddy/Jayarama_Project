from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import *

# Customize the Django admin site
admin.site.site_header = _("Jayarama Associates Administration")
admin.site.site_title = _("Jayarama Admin Portal")
admin.site.index_title = _("Welcome to Admin Panel")

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ['Name', 'Branch', 'IFSC']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['Property_Title']

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = [
        'Auction_id', 'Title', 'Bank', 'Property_Title', 'Location', 
        'City', 'State', 'Amount', 'Reserve_price', 'EMD_amount', 
        'Bid_increment', 'EMD_submission_date', 'Auction_start_date', 
        'Auction_end_date', 'created_at', 'Image'
    ]
    list_filter = ['Bank', 'City', 'State', 'Auction_start_date', 'Auction_end_date']
    search_fields = ['Title', 'Auction_id', 'Location', 'City', 'State']
    ordering = ['-created_at']
    list_per_page = 20

@admin.register(Items)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['item_title']

@admin.register(GoldAuction)
class GoldAuctionAdmin(admin.ModelAdmin):
    list_display = ('appl_apac', 'party_name', 'item', 'gross_wgt', 'state', 'auction_date')
    search_fields = ('appl_apac', 'state', 'branch_name')
    list_filter = ('state', 'branch_name', 'auction_date')