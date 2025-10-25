from django.urls import path
from . import views

app_name = "main"

urlpatterns = [

	path("", views.IndexView, name="index"),
    path("businesses/", views.DonationsView, name="businesses"),
    path('businesses/<int:business_id>/', views.DonationDetailsView, name='business_details'),
    path('invest-now/<int:business_id>/', views.DonateNowView, name='invest_now'),
    path("sign-up/", views.SignUpView, name="sign_up"),
    path("complete/", views.CompleteSignUpView, name="complete_sign_up"),
    path("login/", views.LoginView, name="login"),
    path("logout/", views.LogoutView, name="logout"),
    path("dashboard/", views.DashboardView, name="dashboard"),
    path("create-business/", views.CreateBusinessView, name="create_business"),
    path("edit-business/<int:business_id>/", views.EditBusinessView, name="edit_business"),

]