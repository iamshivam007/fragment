from django.utils import timezone
import os
import random
import uuid

from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.auctions.models import Auction, Bid
from apps.accounts.serializers import UserSerializer

User = get_user_model()


class AuctionListSerializer(serializers.ModelSerializer):
    user_detail = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Auction
        fields = '__all__'

    def get_user_detail(self, instance):
        return UserSerializer(instance.user).data


class AuctionDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    bids = serializers.SerializerMethodField()
    user_detail = serializers.SerializerMethodField()
    winner_bid = serializers.SerializerMethodField()

    class Meta:
        model = Auction
        fields = '__all__'

    def get_bids(self, instance):
        return BidSerializer(instance.bid_set.all(), many=True).data

    def get_winner_bid(self, instance):
        if instance.end_time < timezone.now() and instance.bid_set.exists():
            return BidSerializer(
                Bid.objects.filter(auction=instance).prefetch_related("user").order_by("-bid_amount").first(),
                context=self.context,
            )

    def get_user_detail(self, instance):
        return UserSerializer(instance.user).data


class BidSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user_detail = serializers.SerializerMethodField()

    class Meta:
        model = Bid
        fields = '__all__'

    def validate(self, attrs):
        if attrs['auction'].end_time < timezone.now():
            raise ValidationError("Bid can not be placed on ended auction")

        if attrs["bid_amount"] < attrs["auction"].min_bid:
            raise ValidationError("Bid amount should not be less than minimum bid amount")

        return attrs

    def get_user_detail(self, instance):
        return UserSerializer(instance.user).data
