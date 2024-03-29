from django.utils import timezone

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from apps.accounts.serializers import UserSerializer, LoginSerializer, VerifyOtpSerializer, ProfileUpdateSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "mobile_number"

    permission_classes = (IsAuthenticated, )

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset

    @action(detail=False, methods=["GET", "PUT"])
    def me(self, request):
        if request.method == "GET":
            serializer = UserSerializer(request.user, context={"request": request})
            return Response(status=status.HTTP_200_OK, data={"status_code": 200, "success": True, "data": serializer.data})
        else:
            serializer = ProfileUpdateSerializer(data=request.data, instance=self.request.user)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"status_code": 200, "success": True}, status=status.HTTP_200_OK)


class LoginApiView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_otp(serializer.validated_data)
        return Response({"status_code": 200, "success": True}, status=status.HTTP_200_OK)


class VerifyOtpApiView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = VerifyOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.verify(serializer.validated_data)
        user = serializer.validated_data["user"]

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "status_code": 200, "success": True,
            "data": {
                "token": token.key,
                "name": user.name,
                "username": user.username,
                "id": user.id
            }
        }, status=status.HTTP_200_OK)
