from django.urls import path
from . import views
from .views import *
from .views import download_property_pdf
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('search/', views.search_property, name='search_property'),
    path('advanced-search/', views.advanced_search, name='advanced_search'),
    path('add-property/', login_required(views.add_property), name='add_property'),
    path('update-property/<int:pk>/', login_required(views.update_property), name='update_property'),
    path('delete-property/', login_required(views.delete_property), name='delete_property'),
    path('add-bank/', login_required(views.add_bank), name='add_bank'),
    path('about/', views.about, name='about'),
    path('privacy/', views.privacy, name='privacy'),
    path('contact/', views.contact, name='contact'),
    path('contact/success/', views.contact_success, name='contact_success'),
    path('property/download/<int:property_id>/', login_required(download_property_pdf), name='download_property_pdf'),
    path('download-excel/', login_required(download_search_results), name='download_search_results'),
    path('gold-auctions/', views.home_gold_auction, name='home_gold_auction'),
    path('gold-auctions/<int:pk>/', views.goldauction_detail, name='goldauction_detail'),
    path('gold-auction-data/', views.gold_auction_data, name='gold_auction_data'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('property-list/', views.property_list, name='property_list'),
    path('faqs/', views.faqs_view, name='faqs'),
    path('gold-auctions/', views.gold_auction_view, name='gold_auction'),
    path('download-auction-pdf/<int:auction_id>/', views.download_auction_pdf, name='download_auction_pdf'),
    path('gold-auctions/', views.gold_auction_list, name='gold_auction_list'),
]
