from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['Auction_id', 'Title', 'Bank', 'Property_Title', 'Description', 'Location', 'City', 'State', 'Amount', 'Reserve_price', 'EMD_amount', 'Bid_increment', 'EMD_submission_date', 'Auction_start_date', 'Auction_end_date', 'Image']
        

class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['Name', 'Branch', 'IFSC']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['Property_Title']
    
class PropertySearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label="Search")


class AdvancedSearchForm(forms.Form):
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter location',
        })
    )
    
    bank = forms.ModelChoiceField(
        queryset=Bank.objects.all(),
        required=False,
        empty_label="List of bank",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Select a category",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    from_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'dd-mm-yyyy'
        })
    )
    
    to_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'dd-mm-yyyy'
        })
    )
    
    min_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min price'
        })
    )
    
    max_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max price'
        })
    )
    
    POSSESSION_CHOICES = [
        ('all', 'All Possession'),
        ('physical', 'Physical'),
        ('symbolic', 'Symbolic')
    ]
    
    possession_type = forms.ChoiceField(
        choices=POSSESSION_CHOICES,
        initial='all',
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        })
    )

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class GoldAuctionForm(forms.ModelForm):
    class Meta:
        model = GoldAuction
        fields = ['appl_apac', 'party_name', 'item', 'gross_wgt', 'state', 
                  'sub_location', 'branch_name', 'auction_date']
        widgets = {
            'auction_date': forms.DateInput(attrs={'type': 'date'}),
        }