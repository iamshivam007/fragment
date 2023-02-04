from django.contrib import admin

from apps.auctions.models import Auction, Bid

admin.site.register(Auction)
admin.site.register(Bid)
