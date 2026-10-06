from datetime import timedelta

from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle


class ExpiringObtainAuthToken(ObtainAuthToken):
    """Issue one rotating DRF token with an explicit expiry timestamp."""

    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'token'

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        expires_at = token.created + timedelta(
            seconds=settings.API_TOKEN_LIFETIME_SECONDS
        )
        response = Response({
            'token': token.key,
            'expires_at': expires_at.isoformat(),
            'expires_in': settings.API_TOKEN_LIFETIME_SECONDS,
        })
        response['Cache-Control'] = 'no-store'
        response['Pragma'] = 'no-cache'
        return response
