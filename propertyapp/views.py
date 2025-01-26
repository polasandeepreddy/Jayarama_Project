from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import *
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q

def is_admin(user):
    return user.is_staff

def home(request):
    properties = Property.objects.all().order_by('-created_at')
    return render(request, 'properties/home.html', {'properties': properties})

@login_required
def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.user.is_authenticated:
        return render(request, 'properties/property_detail.html', {'property': property})
    else:
        return render(request, 'login.html', {'error': 'Please login to view property details.'})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'properties/login.html', {'error': 'Invalid credentials'})
    return render(request, 'properties/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'properties/signup.html', {'form': form})

@user_passes_test(is_admin)
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.created_by = request.user
            property.save()
            return redirect('home')
    else:
        form = PropertyForm()
    return render(request, 'properties/add_property.html', {'form': form})

@user_passes_test(is_admin)
def update_property(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PropertyForm(instance=property)
    return render(request, 'properties/add_property.html', {'form': form, 'property': property})

@user_passes_test(is_admin)
def delete_property(request):
    if request.method == 'GET':
        property_id = request.GET.get('t1', None)
        if property_id:
            try:
                property = Property.objects.get(pk=property_id)
                property.delete()
                return render(request, 'properties/delete_property.html', {'message': 'Property deleted successfully!'})
            except Property.DoesNotExist:
                return render(request, 'properties/delete_property.html', {'message': 'Property not found.'})
    return render(request, 'properties/delete_property.html', {'message': ''})

@user_passes_test(is_admin)
def add_bank(request):
    if request.method == 'POST':
        form = BankForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BankForm()
    return render(request, 'properties/add_bank.html', {'form': form})

def search_property(request):
    query = request.GET.get('query', '')
    properties = Property.objects.filter(
        Q(Title__icontains=query) |
        Q(Location__icontains=query) |
        Q(City__icontains=query) |
        Q(State__icontains=query)
    )
    return render(request, 'properties/search_property.html', {'properties': properties, 'query': query})

def advanced_search(request):
    form = AdvancedSearchForm(request.GET or None)
    properties = Property.objects.all().order_by('-Auction_start_date')
    
    if form.is_valid():
        location = form.cleaned_data.get('location')
        bank = form.cleaned_data.get('bank')
        category = form.cleaned_data.get('category')
        from_date = form.cleaned_data.get('from_date')
        to_date = form.cleaned_data.get('to_date')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        possession_type = form.cleaned_data.get('possession_type')
        
        if location:
            properties = properties.filter(
                Q(Location__icontains=location) |
                Q(City__icontains=location) |
                Q(State__icontains=location)
            )
        
        if bank:
            properties = properties.filter(Bank=bank)
        
        if category:
            properties = properties.filter(Property_Title=category)
        
        if from_date:
            properties = properties.filter(Auction_start_date_date_gte=from_date)
        
        if to_date:
            properties = properties.filter(Auction_end_date_date_lte=to_date)
        
        if min_price:
            properties = properties.filter(Amount__gte=min_price)
        
        if max_price:
            properties = properties.filter(Amount__lte=max_price)
    
    paginator = Paginator(properties, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'properties': page_obj,
        'total_results': properties.count(),
    }
    
    return render(request, 'properties/advanced_search.html', context)

def about(request):
    return render(request, 'about.html')

def privacy(request):
    return render(request, 'privacy.html')