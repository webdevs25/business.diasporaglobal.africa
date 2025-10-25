from decimal import Decimal
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum

from main.forms import AppUserForm, UserForm, DonationForm
from main.models import AppUser, Contribution, Donation
from django.utils import timezone
from django.core.mail import send_mail

from datetime import datetime
import datetime as dt

import random
import string

def ray_randomiser(length=6):
    landd = string.digits
    return ''.join((random.choice(landd) for i in range(length)))

def IndexView(request):
    if request.method == "POST":
        pass
    else:
        donations = Donation.objects.all()
        context = {
            "donations": donations,
        }
        return render(request, "main/index.html", context)

def DonationsView(request):
    if request.method == "POST":
        pass
    else:
        donations = Donation.objects.all()
        context = {
            "donations": donations,
        }
        return render(request, "main/donation.html", context)

def DonationDetailsView(request, business_id):
    if request.method == "POST":
        pass
    else:
        donation = get_object_or_404(Donation, id=business_id)
        app_user = donation.app_user

        # Ensure template has explicit values even if properties are not evaluated
        try:
            days_since = max((timezone.now() - donation.pub_date).days, 0)
        except Exception:
            days_since = 0
        donators_count = donation.contributions.count()

        # Optionally assign dynamic attributes for direct template access
        setattr(donation, 'days_since_published', days_since)
        setattr(donation, 'donators_count', donators_count)

        related_donations = Donation.objects.filter(
            project_type=donation.project_type
        ).exclude(id=donation.id).order_by('-pub_date')[:4]

        context = {
            "donation": donation,
            "app_user": app_user,
            "donation_days": days_since,
            "donation_donators_count": donators_count,
            "related_donations": related_donations,
        }
        return render(request, "main/donation-detail.html", context)

def DonateNowView(request, business_id):
    donation = get_object_or_404(Donation, id=business_id)

    if request.method == "POST":
        amount = request.POST.get("amount")
        anonymous = request.POST.get("anonymous") == "on"

        try:
            amount = Decimal(amount)
            if amount <= 0:
                raise ValueError("Amount must be greater than 0.")
        except (ValueError, TypeError):
            messages.error(request, "Invalid donation amount. Please enter a valid number.")
            return redirect(reverse("main:donate_now", args=[business_id]))

        contribution = Contribution(
            donation=donation,
            donor=request.user if request.user.is_authenticated and not anonymous else None,
            amount=amount,
            anonymous=anonymous,
        )
        contribution.save()

        messages.success(request, "Thank you for investing in us!")
        return redirect(reverse("main:invest_now", args=[business_id]))

    context = {
        "donation": donation,
    }
    return render(request, "main/donate-now.html", context)

def SignUpView(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        app_user_form = AppUserForm(request.POST)

        email = request.POST.get("username")
        user_type = request.POST.get("user_type", "investor")

        if request.POST.get("password2") != request.POST.get("password1"):
            messages.warning(request, "Make sure both passwords match")
            return HttpResponseRedirect(reverse("main:sign_up"))

        try:
            AppUser.objects.get(user__email=email)
            messages.warning(request, "Email Address already taken, try another one!")
            return HttpResponseRedirect(reverse("main:sign_up"))
        except AppUser.DoesNotExist:
            pass

        if user_form.is_valid() and app_user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(request.POST.get("password1"))
            user.email = email
            user.save()

            app_user = app_user_form.save(commit=False)
            app_user.user = user
            app_user.otp_code = ray_randomiser()
            app_user.user_type = user_type
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
            messages.success(request, "Welcome Onboard!")
            return HttpResponseRedirect(reverse("main:dashboard"))

        else:
            messages.warning(request, "Sorry, Invalid OTP Code.")
            return HttpResponseRedirect(reverse("main:complete_sign_up"))

    else:
        context = {}
        return render(request, "main/complete_sign_up.html", context)

def LoginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect(reverse("main:dashboard"))
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect(reverse("main:login"))
    
    return render(request, "main/login.html")

def LogoutView(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect(reverse("main:index"))

@login_required
def DashboardView(request):
    try:
        app_user = AppUser.objects.get(user=request.user)
        
        if app_user.user_type == 'business_owner':
            # Business Owner Dashboard
            my_businesses = Donation.objects.filter(app_user=app_user)
            total_raised = Donation.objects.filter(app_user=app_user).aggregate(
                total=Sum('amount_donated')
            )['total'] or Decimal('0.00')
            
            # Get all contributions to my businesses
            business_contributions = []
            for business in my_businesses:
                contributions = Contribution.objects.filter(donation=business).select_related('donor')
                for contribution in contributions:
                    business_contributions.append(contribution)
            
            context = {
                'user_type': 'business_owner',
                'my_businesses': my_businesses,
                'total_raised': total_raised,
                'business_contributions': business_contributions,
            }
            
        else:
            # Investor Dashboard
            my_investments = Contribution.objects.filter(donor=request.user).select_related('donation')
            total_invested = my_investments.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
            
            context = {
                'user_type': 'investor',
                'my_investments': my_investments,
                'total_invested': total_invested,
            }
        
        return render(request, "main/dashboard.html", context)
        
    except AppUser.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect(reverse("main:index"))

@login_required
def CreateBusinessView(request):
    try:
        app_user = AppUser.objects.get(user=request.user)
        
        if app_user.user_type != 'business_owner':
            messages.error(request, "Only business owners can create business listings.")
            return redirect(reverse("main:dashboard"))
            
        if request.method == "POST":
            form = DonationForm(request.POST, request.FILES)
            if form.is_valid():
                business = form.save(commit=False)
                business.app_user = app_user
                business.save()
                messages.success(request, "Business listing created successfully!")
                return redirect(reverse("main:dashboard"))
            else:
                messages.error(request, "Please correct the errors below.")
        else:
            form = DonationForm()
        
        context = {
            'form': form,
        }
        return render(request, "main/create_business.html", context)
        
    except AppUser.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect(reverse("main:index"))

@login_required
def EditBusinessView(request, business_id):
    try:
        app_user = AppUser.objects.get(user=request.user)
        business = get_object_or_404(Donation, id=business_id, app_user=app_user)
        
        if request.method == "POST":
            form = DonationForm(request.POST, request.FILES, instance=business)
            if form.is_valid():
                form.save()
                messages.success(request, "Business listing updated successfully!")
                return redirect(reverse("main:dashboard"))
            else:
                messages.error(request, "Please correct the errors below.")
        else:
            form = DonationForm(instance=business)
        
        context = {
            'form': form,
            'business': business,
        }
        return render(request, "main/edit_business.html", context)
        
    except AppUser.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect(reverse("main:index"))