from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal


# from resume.models import Resume

class AppUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	otp_code = models.CharField(default="none",max_length=10)
	email = models.CharField(max_length=150, default="none")
	category = models.CharField(max_length=150, default="none")
	gender = models.CharField(max_length=150, default="none")
	phone_no = models.CharField(max_length=150, default="none")

	def __str__(self):
		return self.user.username


class Donation(models.Model):
    image_one = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
    title = models.CharField(max_length=50, default="none")
    description = models.TextField(default="none")
    goal = models.CharField(max_length=20, default="none")  # Target amount for the fundraiser
    about = models.TextField(default="none")
    summary = models.TextField(default="none")
    challenge = models.TextField(default="none")
    target_one = models.CharField(max_length=1020, default="none")
    target_two = models.CharField(max_length=1020, default="none", null=True)
    target_three = models.CharField(max_length=1020, default="none", null=True)
    target_four = models.CharField(max_length=1020, default="none", null=True)
    target_five = models.CharField(max_length=1020, default="none", null=True)
    target_six = models.CharField(max_length=1020, default="none")
    target_seven = models.CharField(max_length=1020, default="none")
    more_info = models.TextField(default="none")
    image_two = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")

    app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)  # Link to the fundraiser creator

    image_portriat = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
    amount_donated = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # Sum of donations

    status = models.BooleanField(default=False)  # Fundraiser status (e.g., active/inactive)
    pub_date = models.DateTimeField(default=timezone.now)  # Publication date

    def __str__(self):
        return self.title

    def update_amount_donated(self):
        """
        Update the amount_donated field by summing all contributions.
        """
        total = self.contributions.aggregate(models.Sum('amount'))['amount__sum']
        self.amount_donated = total if total is not None else Decimal('0.00')
        self.save()

    def percentage_raised(self):
        """
        Calculate the percentage of the goal that has been raised.
        """
        if self.goal and self.amount_donated:
            goal_amount = Decimal(self.goal)  # Convert goal to Decimal
            return (self.amount_donated / goal_amount) * 100
        return 0


class Contribution(models.Model):
    donor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Link to the donor (if authenticated)
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name='contributions')  # Link to the fundraiser
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Donation amount
    timestamp = models.DateTimeField(default=timezone.now)  # When the donation was made
    anonymous = models.BooleanField(default=False)  # Whether the donation is anonymous

    def __str__(self):
        return f"${self.amount} by {self.donor.username if self.donor else 'Anonymous'} to {self.donation.title}"

    def save(self, *args, **kwargs):
        """
        Override the save method to update the amount_donated field in the Donation model.
        """
        super().save(*args, **kwargs)
        self.donation.update_amount_donated()

    class Meta:
        ordering = ['-timestamp']  # Order contributions by most recent