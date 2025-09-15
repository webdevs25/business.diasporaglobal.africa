from django.contrib.auth.models import User
from django import forms
from .models import AppUser

class UserForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")
    
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password1", "password2"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        
        return password2


class AppUserForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ['category'] 