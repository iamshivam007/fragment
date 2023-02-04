from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model
User = get_user_model()


class Auction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country_code = CharField(_("User Country Code"), blank=True, max_length=4)
    mobile_number = models.CharField(max_length=20)
    min_bid = models.DecimalField(max_digits=10, decimal_places=3)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()

    def __str__(self):
        return f"${self.user} | ${self.mobile_number} -> ${self.end_time}"

    class Meta:
        unique_together = ['user', 'mobile_number']


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=3)
    token = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"${self.user} | ${self.auction} -> ${self.bid_amount}"
