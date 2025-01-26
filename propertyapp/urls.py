from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('search/', views.search_property, name='search_property'),
    path('advanced-search/', views.advanced_search, name='advanced_search'),
    path('add-property/', views.add_property, name='add_property'),
    path('update-property/<int:pk>/', views.update_property, name='update_property'),
    path('delete-property/', views.delete_property, name='delete_property'),
    path('add-bank/', views.add_bank, name='add_bank'),
    path('about', views.about, name= 'about'),
    path('privacy', views.privacy, name= 'privacy'),

]

