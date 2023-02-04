from django.urls import path
from django.conf import settings

from apps.auctions import views as auctions_views
from rest_framework.routers import DefaultRouter, SimpleRouter

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("auctions", auctions_views.AuctionViewSet)
router.register("bids", auctions_views.BidViewSet)

urlpatterns = [
    # API base url
] + router.urls
