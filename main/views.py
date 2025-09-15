from decimal import Decimal
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages  # Correct import for Django messages framework

from main.forms import AppUserForm, UserForm
from main.models import AppUser, Contribution, Donation
from django.core.mail import send_mail

from datetime import datetime
import datetime as dt

# Create your views here.
import random
import string

def ray_randomiser(length=6):
    landd = string.digits
    return ''.join((random.choice(landd) for i in range(length)))

def IndexView(request):
    if request.method == "POST":
        pass
    else:
        # Fetch all donations from the database
        donations = Donation.objects.all()
        context = {
            "donations": donations,  # Pass donations to the template
        }
        return render(request, "main/index.html", context)
    
def DonationsView(request):
    if request.method == "POST":
        pass
    else:
        # Fetch all donations from the database
        donations = Donation.objects.all()
        context = {
            "donations": donations,  # Pass donations to the template
        }
        return render(request, "main/donation.html", context)
    
def DonationDetailsView(request, donation_id):
    if request.method == "POST":
        pass
    else:
        # Fetch the specific donation by its ID
        donation = get_object_or_404(Donation, id=donation_id)
        
        # Access the app_user who created the donation
        app_user = donation.app_user
        
        context = {
            "donation": donation,  # Pass the donation to the template
            "app_user": app_user,  # Pass the app_user to the template
        }
        return render(request, "main/donation-detail.html", context)

def DonateNowView(request, donation_id):
    # Fetch the donation object
    donation = get_object_or_404(Donation, id=donation_id)

    if request.method == "POST":
        # Get the donation amount and anonymous status from the POST data
        amount = request.POST.get("amount")
        anonymous = request.POST.get("anonymous") == "on"  # Check if the checkbox was checked

        # Validate the amount
        try:
            amount = Decimal(amount)
            if amount <= 0:
                raise ValueError("Amount must be greater than 0.")
        except (ValueError, TypeError):
            messages.error(request, "Invalid donation amount. Please enter a valid number.")
            return redirect(reverse("main:donate_now", args=[donation_id]))

        # Create a Contribution object
        contribution = Contribution(
            donation=donation,
            donor=request.user if request.user.is_authenticated and not anonymous else None,
            amount=amount,
            anonymous=anonymous,
        )
        contribution.save()  # This will trigger the save() method in the Contribution model

        messages.success(request, "Thank you for your donation!")
        return redirect(reverse("main:donation_details", args=[donation_id]))

    context = {
        "donation": donation,
    }
    return render(request, "main/donate-now.html", context)

def SignUpView(request):
    if request.method == "POST":
        # Handle both UserForm and AppUserForm
        user_form = UserForm(request.POST or None, request.FILES or None)
        app_user_form = AppUserForm(request.POST or None)

        email = request.POST.get("username")

        if request.POST.get("password2") != request.POST.get("password1"):
            messages.warning(request, "Make sure both passwords match")
            return HttpResponseRedirect(reverse("main:sign_up"))

        # Check if the email already exists in AppUser
        try:
            AppUser.objects.get(user__email=email)
            messages.warning(request, "Email Address already taken, try another one!")
            return HttpResponseRedirect(reverse("main:sign_up"))
        except AppUser.DoesNotExist:
            pass  # Proceed if no existing AppUser has the same email

        if user_form.is_valid() and app_user_form.is_valid():
            # Create and save the User object
            user = user_form.save(commit=False)
            user.set_password(request.POST.get("password1"))
            user.email = email
            user.save()

            # Create and save the AppUser object
            app_user = app_user_form.save(commit=False)
            app_user.user = user
            app_user.otp_code = ray_randomiser()  # Assuming you have this function for OTP
            app_user.save()

            if user.is_active:
                login(request, user)
                messages.success(request, "Account created! Your OTP code has been sent to your email.")
                return HttpResponseRedirect(reverse("main:complete_sign_up"))

        else:
            messages.error(request, "There was an error with your form submission.")

    else:
        user_form = UserForm()
        app_user_form = AppUserForm()

    context = {
        "user_form": user_form,
        "app_user_form": app_user_form,
    }

    return render(request, "main/sign_up.html", context)

def CompleteSignUpView(request):
    if request.method == "POST":
        otp = request.POST.get("otp")
        
        app_user = AppUser.objects.get(user__pk=request.user.id)
        if otp == app_user.otp_code:
            app_user.ec_status = True
            app_user.save()

            messages.warning(request, "Welcome Onboard!")
            return HttpResponseRedirect(reverse("main:index"))

        else:
            messages.warning(request, "Sorry, Invalid OTP Code.")
            return HttpResponseRedirect(reverse("main:complete_sign_up"))

    else:
        context = {}
        return render(request, "main/complete_sign_up.html", context)