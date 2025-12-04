from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    class Role(models.TextChoices):
        DONOR="DONOR", "Donor"
        RECEIVER="RECEIVER", "Receiver"
        VOLUNTEER="VOLUNTEER", "Volunteer"
    role= models.CharField(max_length=50, choices= Role.choices)
    location= models.CharField(max_length=255, blank=True, null=True)

 
class Donation(models.Model):
    class DonationStatus(models.TextChoices):
        PENDING="PENDING", "Pending"
        CLAIMED="CLAIMED", "Claimed"
        DELIVERED="DELIVERED", "Delivered"
        CANCELLED="CANCELLED", "Cancelled"
    donor =models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='donations' )
    title= models.CharField(max_length=200, help_text= "e.g. 'Surplus Bread and Pastries'")
    quantity = models.PositiveIntegerField()
    description=models.TextField(blank=True)
    pickup_location=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    status= models.CharField(max_length=30, choices= DonationStatus.choices, default=DonationStatus.PENDING)

    def __str__(self):
        return f"{self.title} from {self.donor.username}"
class Delivery(models.Model):
    class DeliveryStatus(models.TextChoices):
        PENDING="PENDING", "Pending"
        IN_PROGRESS="IN_PROGRESS", "In Progress"
        COMPLETED="COMPLETED", "Completed"
    donation = models.OneToOneField(Donation, on_delete=models.CASCADE, related_name="delivery")
    volunteer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="deliveries")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="received_items")
    status = models.CharField(max_length=20, choices=DeliveryStatus.choices, default=DeliveryStatus.PENDING)
    picked_up_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Delivery for {self.donation.title}"
    
