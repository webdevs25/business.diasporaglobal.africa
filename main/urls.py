from django.urls import path
from . import views

app_name = "main"

urlpatterns = [

	path("", views.IndexView, name="index"),
    path("donations/", views.DonationsView, name="donations"),
    path('donations/<int:donation_id>/', views.DonationDetailsView, name='donation_details'),
    path('donate-now/<int:donation_id>/', views.DonateNowView, name='donate_now'),
    path("sign-up/", views.SignUpView, name="sign_up"),
    path("complete/", views.CompleteSignUpView, name="complete_sign_up"),

]