from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

class AppUser(models.Model):
    USER_TYPES = (
        ('investor', 'Investor'),
        ('business_owner', 'Business Owner'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_code = models.CharField(default="none", max_length=10)
    email = models.CharField(max_length=150, default="none")
    category = models.CharField(max_length=150, default="none")
    gender = models.CharField(max_length=150, default="none")
    phone_no = models.CharField(max_length=150, default="none")
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='investor')

    def __str__(self):
        return self.user.username

class Donation(models.Model):
    image_one = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
    image_three = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
    image_four = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
    title = models.CharField(max_length=50, default="none")
    description = models.TextField(default="none")
    goal = models.CharField(max_length=20, default="none")
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
    website = models.CharField(max_length=1020, default="none")
    project_type = models.CharField(max_length=1020, default="none")
    location = models.CharField(max_length=1020, default="none")

    app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)

    image_portriat = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
    amount_donated = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    status = models.BooleanField(default=False)
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def update_amount_donated(self):
        total = self.contributions.aggregate(models.Sum('amount'))['amount__sum']
        self.amount_donated = total if total is not None else Decimal('0.00')
        self.save()

    def percentage_raised(self):
        if self.goal and self.amount_donated:
            goal_amount = Decimal(self.goal)
            return (self.amount_donated / goal_amount) * 100
        return 0

class Contribution(models.Model):
    donor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name='contributions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)
    anonymous = models.BooleanField(default=False)

    def __str__(self):
        return f"${self.amount} by {self.donor.username if self.donor else 'Anonymous'} to {self.donation.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.donation.update_amount_donated()

    class Meta:
        ordering = ['-timestamp']