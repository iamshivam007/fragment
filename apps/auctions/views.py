from django.utils import timezone

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from apps.auctions.models import Auction, Bid
from apps.auctions.serializers import AuctionListSerializer, AuctionDetailSerializer, BidSerializer

User = get_user_model()


class AuctionViewSet(RetrieveModelMixin, ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = AuctionListSerializer
    queryset = Auction.objects.all().prefetch_related("user")
    lookup_field = "id"

    permission_classes = (IsAuthenticatedOrReadOnly, )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = AuctionDetailSerializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def mine(self, request):
        assert isinstance(self.request.user.id, int)
        serializer = AuctionListSerializer(
            Auction.objects.filter(user=request.user),
            context={"request": request},
            many=True
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False, methods=["GET"])
    def live(self, request):
        serializer = AuctionListSerializer(
            Auction.objects.filter(end_time__gt=timezone.now()),
            context={"request": request},
            many=True
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=True, methods=["GET"])
    def top_ten_bids(self, request, *args, **kwargs):
        serializer = BidSerializer(
            Bid.objects.filter(auction=self.get_object()).prefetch_related("user").order_by("-bid_amount")[:10],
            context={"request": request},
            many=True
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class BidViewSet(RetrieveModelMixin, ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = BidSerializer
    queryset = Bid.objects.all().prefetch_related("user")
    lookup_field = "id"

    permission_classes = (IsAuthenticated, )

    @action(detail=False, methods=["GET"])
    def mine(self, request):
        serializer = BidSerializer(
            Bid.objects.filter(user=request.user),
            context={"request": request},
            many=True
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False, methods=["GET"])
    def mine_active(self, request):
        serializer = BidSerializer(
            Bid.objects.filter(user=request.user, auction__end_time__gt=timezone.now()),
            context={"request": request},
            many=True
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)
