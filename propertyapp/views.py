from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from reportlab.pdfgen import canvas
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mail
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.lib.styles import *
import os
from django.conf import settings
from .models import *
from .forms import *
import pandas as pd
from io import BytesIO
from django.http import JsonResponse


def is_admin(user):
    return user.is_staff

def home(request):
    properties = Property.objects.all().order_by('-created_at')  # Ensures newest first
    return render(request, 'properties/home.html', {'properties': properties})

def property_list(request):
    return render(request, 'properties/property_list.html')


@login_required
def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    return render(request, 'properties/property_detail.html', {'property': property})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_staff:  # Redirect admin to the admin panel
                return redirect('/admin/')  # Django's built-in admin panel
            else:
                return redirect('home')  # Regular user goes to home page
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
            user = form.save()
            login(request, user)
            return redirect('home')
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
    category = request.GET.get('category', '')

    if category == "gold":
        properties = GoldAuction.objects.filter(
            Q(appl_apac__icontains=query) |
            Q(item__item_title__icontains=query) |
            Q(state__icontains=query) |
            Q(sub_location__icontains=query) |
            Q(branch_name__icontains=query)
        ).order_by('-created_at')
    else:
        properties = Property.objects.filter(
            Q(Title__icontains=query) |
            Q(Location__icontains=query) |
            Q(City__icontains=query) |
            Q(State__icontains=query)
        ).order_by('-created_at')

    return render(request, 'properties/search_property.html', {'properties': properties, 'query': query})

def advanced_search(request):
    form = AdvancedSearchForm(request.GET or None)
    category = request.GET.get('category', '')

    if category == "gold":
        properties = GoldAuction.objects.all().order_by('-auction_date')
    else:
        properties = Property.objects.all().order_by('-Auction_start_date')

    if form.is_valid():
        location = form.cleaned_data.get('location')
        bank = form.cleaned_data.get('bank')
        category_form = form.cleaned_data.get('category')
        from_date = form.cleaned_data.get('from_date')
        to_date = form.cleaned_data.get('to_date')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')

        if category == "gold":
            if location:
                properties = properties.filter(
                    Q(state__icontains=location) |
                    Q(sub_location__icontains=location) |
                    Q(branch_name__icontains=location)
                )

            if from_date:
                properties = properties.filter(auction_date__gte=from_date)

            if to_date:
                properties = properties.filter(auction_date__lte=to_date)

        else:
            if location:
                properties = properties.filter(
                    Q(Location__icontains=location) |
                    Q(City__icontains=location) |
                    Q(State__icontains=location)
                )

            if bank:
                properties = properties.filter(Bank=bank)

            if category_form:
                properties = properties.filter(Property_Title=category_form)

            if from_date:
                properties = properties.filter(Auction_start_date__gte=from_date)

            if to_date:
                properties = properties.filter(Auction_end_date__lte=to_date)

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


def property_list(request):
    properties = Property.objects.all().order_by('-created_at')  # Ensures newest first
    paginator = Paginator(properties, 10)  # Paginate results
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'properties/home.html', {'properties': page_obj, 'page_obj': page_obj})

def about(request):
    return render(request, 'about.html')

def privacy(request):
    return render(request, 'privacy.html')

from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from .forms import ContactForm

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            try:
                send_mail(
                    f'Support Request from {name}',
                    f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                    settings.EMAIL_HOST_USER,  # Uses Django settings
                    ['polasandeepreddyirctc@gmail.com'],  # Your recipient email
                    fail_silently=False,
                )
                messages.success(request, "Your message has been sent successfully!")
                return redirect(reverse('contact_success'))
            except BadHeaderError:
                messages.error(request, "Invalid email header found.")
            except Exception as e:
                messages.error(request, f"Error sending email: {str(e)}")
            return redirect('contact')

    else:
        form = ContactForm()
    return render(request, 'properties/contact.html', {'form': form})


def contact_success(request):
    return render(request, 'properties/contact_success.html')

def download_property_pdf(request, property_id):
    property = get_object_or_404(Property, pk=property_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="property_{property.Auction_id}.pdf"'
    pdf = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    description_paragraph = Paragraph(property.Description, styles["Normal"])
    data = [
        ['Field', 'Details'],
        ['Auction ID', property.Auction_id],
        ['Title', property.Title],
        ['Location', f"{property.Location}, {property.City}, {property.State}"],
        ['Reserve Price', f"Rs. {property.Reserve_price}"],
        ['EMD Amount', f"Rs. {property.EMD_amount}"],
        ['Bid Increment', f"Rs. {property.Bid_increment}"],
        ['Auction Start Date', property.Auction_start_date.strftime('%Y-%m-%d %H:%M')],
        ['Auction End Date', property.Auction_end_date.strftime('%Y-%m-%d %H:%M')],
        ['Description', description_paragraph],
    ]
    table = Table(data, colWidths=[150, 350])
    table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, -1), (0, 0), 'CENTER'),  # Center-align only the first column (Field)
    ('ALIGN', (1, 0), (1, -1), 'LEFT'),    # Left-align the second column (Details)
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 12),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))
    elements.append(table)
    pdf.build(elements)
    return response


def download_search_results(request):
    query = request.GET.get('query', '').strip()  # Get search query and strip whitespace

    # Fetch matching properties based on query
    properties = Property.objects.all()
    if query:
        properties = properties.filter(
            Q(Title__icontains=query) | Q(City__icontains=query) | Q(State__icontains=query)
        )

    # Debugging: Check how many results are fetched
    print(f"Total properties fetched: {properties.count()}")

    if not properties.exists():
        return HttpResponse("No data available for download.", content_type="text/plain")

    # Fetch related Bank details
    bank_details = Bank.objects.filter(Name__icontains=query)  # Adjust based on your model

    # Convert property queryset to list of dictionaries
    property_data = list(properties.values(
        'Auction_id', 'Title', 'Bank__Name', 'Location', 'City', 'State',
        'Amount', 'Reserve_price', 'EMD_amount', 'Bid_increment',
        'EMD_submission_date', 'Auction_start_date', 'Auction_end_date', 'Description'
    ))

    # Convert bank queryset to list of dictionaries
    bank_data = list(bank_details.values("Name", "Branch", "IFSC"))

    # Convert both to DataFrame
    property_df = pd.DataFrame(property_data)
    bank_df = pd.DataFrame(bank_data)

    # Handle missing values
    property_df.fillna('', inplace=True)
    bank_df.fillna('', inplace=True)

    # Convert date fields to a readable format
    date_fields = ['Auction_start_date', 'Auction_end_date', 'EMD_submission_date']
    for field in date_fields:
        if field in property_df.columns:
            property_df[field] = pd.to_datetime(property_df[field], errors='coerce').dt.strftime('%d-%m-%Y, %I:%M %p')

    # Create Excel response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="search_results.xlsx"'

    with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
        property_df.to_excel(writer, sheet_name='Properties', index=False)
        bank_df.to_excel(writer, sheet_name='Banks', index=False)

        # Adjust column width
        writer.sheets['Properties'].set_column('A:Z', 30)
        writer.sheets['Banks'].set_column('A:C', 30)

    return response

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from .models import GoldAuction  # Changed model name to GoldAuction

def download_auction_pdf(request, auction_id):
    # Fetch the GoldAuction object based on auction_id
    auction = get_object_or_404(GoldAuction, pk=auction_id)

    # Create the PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="auction_{auction.id}_details.pdf"'
    pdf = SimpleDocTemplate(response, pagesize=letter)

    elements = []
    styles = getSampleStyleSheet()

    # Title of the document
    title = Paragraph(f'Gold Auction Details for Auction #{auction.id}', styles["Title"])
    elements.append(title)
    
    # Create data for the table
    data = [
        ['Field', 'Details'],
        ['Application/Region', auction.appl_apac],
        ['Party Name', auction.party_name or "Not Available"],
        ['Item', auction.item],
        ['Gross Weight (kg)', f"{auction.gross_wgt:.2f}"],
        ['State', auction.state],
        ['Sub-Location', auction.sub_location],
        ['Branch Name', auction.branch_name],
        ['Auction Date', auction.auction_date.strftime('%Y-%m-%d %H:%M')],
    ]
    
    # Create the table
    table = Table(data, colWidths=[150, 350])
    table.setStyle(TableStyle([ 
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, -1), (0, 0), 'CENTER'),  # Center-align only the first column (Field)
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),    # Left-align the second column (Details)
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)

    # Build the PDF
    pdf.build(elements)
    return response


def goldauction_detail(request, pk):
    auction = get_object_or_404(GoldAuction, pk=pk)
    return render(request, 'properties/goldauction_detail.html', {'auction': auction})

def home_gold_auction(request):
    properties = GoldAuction.objects.all()
    return render(request, 'properties/home_GoldAuction.html', {'properties': properties})

def gold_auction_view(request):
    properties = GoldAuction.objects.all()
    return render(request, 'properties/gold_auction.html')

def gold_auction_data(request):
    auctions = GoldAuction.objects.values(
        'appl_apac', 'party_name', 'item__item_title', 'gross_wgt', 'state', 
        'sub_location', 'branch_name', 'auction_date'
    )
    
    data = {'properties': list(auctions)}
    return JsonResponse(data)


def gold_auction_list(request):
    auctions = GoldAuction.objects.all()
    return render(request, 'properties/home_GoldAuction.html', {'auctions': auctions})



def dashboard(request):
    return render(request, 'properties/dashboard.html')

def profile(request):
    return render(request, 'properties/profile.html')

def faqs_view(request):
    return render(request, 'properties/faqs.html')