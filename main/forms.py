from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from main.models import AppUser, Donation

class UserForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter your password',
            'required': 'required'
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Confirm your password',
            'required': 'required'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        widgets = {
            'username': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your email address',
                'required': 'required'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your first name',
                'required': 'required'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your last name',
                'required': 'required'
            }),
        }
        labels = {
            'username': 'Email Address',
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with this email already exists.")
        return username

class AppUserForm(forms.ModelForm):
    USER_TYPES = (
        ('', 'Select Account Type'),
        ('investor', 'Investor'),
        ('business_owner', 'Business Owner'),
    )
    
    GENDER_CHOICES = (
        ('', 'Select Gender'),
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say'),
    )
    
    user_type = forms.ChoiceField(
        choices=USER_TYPES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'required'
        }),
        label='Account Type'
    )
    
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        required=False
    )
    
    class Meta:
        model = AppUser
        fields = ['phone_no', 'gender', 'category']
        widgets = {
            'phone_no': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your phone number',
                'required': 'required'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'e.g., Technology, Healthcare, Retail'
            }),
        }
        labels = {
            'phone_no': 'Phone Number',
            'category': 'Industry/Category',
        }
    
    def clean_phone_no(self):
        phone_no = self.cleaned_data.get('phone_no')
        if not phone_no or phone_no == 'none':
            raise ValidationError("Phone number is required.")
        return phone_no

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = [
            'title', 'description', 'goal', 'about', 'summary', 'challenge',
            'target_one', 'target_two', 'target_three', 'target_four', 'target_five',
            'target_six', 'target_seven', 'more_info', 'website', 'project_type', 
            'location', 'image_one', 'image_two', 'image_three', 'image_four', 
            'image_portriat'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter business/project title',
                'required': 'required'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Brief description of your business/project',
                'required': 'required'
            }),
            'goal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 50000 (fundraising goal in dollars)',
                'required': 'required'
            }),
            'about': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4,
                'placeholder': 'Tell us more about your business/project',
                'required': 'required'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Executive summary'
            }),
            'challenge': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'What challenges are you facing?'
            }),
            'target_one': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Primary goal or target'
            }),
            'target_two': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Secondary goal or target'
            }),
            'target_three': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Additional goal or target'
            }),
            'target_four': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Additional goal or target'
            }),
            'target_five': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Additional goal or target'
            }),
            'target_six': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Additional goal or target'
            }),
            'target_seven': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Additional goal or target'
            }),
            'more_info': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4,
                'placeholder': 'Any additional information for potential investors'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://yourwebsite.com'
            }),
            'project_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Tech Startup, Restaurant, Retail Store'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City, State, Country',
                'required': 'required'
            }),
            'image_one': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'image_two': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'image_three': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'image_four': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'image_portriat': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'title': 'Business/Project Title',
            'description': 'Description',
            'goal': 'Funding Goal ($)',
            'about': 'About',
            'summary': 'Executive Summary',
            'challenge': 'Challenges',
            'target_one': 'Target 1',
            'target_two': 'Target 2',
            'target_three': 'Target 3',
            'target_four': 'Target 4',
            'target_five': 'Target 5',
            'target_six': 'Target 6',
            'target_seven': 'Target 7',
            'more_info': 'Additional Information',
            'website': 'Website URL',
            'project_type': 'Project Type',
            'location': 'Location',
            'image_one': 'Main Image',
            'image_two': 'Additional Image 1',
            'image_three': 'Additional Image 2',
            'image_four': 'Additional Image 3',
            'image_portriat': 'Portrait/Logo Image',
        }
    
    def clean_goal(self):
        goal = self.cleaned_data.get('goal')
        if goal:
            try:
                # Try to convert to number to validate
                float(goal)
            except ValueError:
                raise ValidationError("Please enter a valid number for the funding goal.")
        return goal
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title or title.strip() == '':
            raise ValidationError("Title is required.")
        return title.strip()
    
    def clean_location(self):
        location = self.cleaned_data.get('location')
        if not location or location.strip() == '':
            raise ValidationError("Location is required.")
        return location.strip()

# Additional form for investment/donation
class InvestmentForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=1.00,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter investment amount',
            'step': '0.01',
            'min': '1.00',
            'required': 'required'
        }),
        label='Investment Amount ($)'
    )
    
    anonymous = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Make this investment anonymous'
    )
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount and amount < 1:
            raise ValidationError("Investment amount must be at least $1.00")
        return amount

# Form for user profile updates
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class AppUserUpdateForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ['phone_no', 'gender', 'category']
        widgets = {
            'phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
        }