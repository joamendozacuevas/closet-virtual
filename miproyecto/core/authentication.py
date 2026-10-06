from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class ExpiringTokenAuthentication(TokenAuthentication):
    """DRF tokens with a fixed lifetime; clients obtain a fresh token on expiry."""

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed('Token inválido.')

        if not token.user.is_active:
            raise AuthenticationFailed('La cuenta está desactivada.')

        lifetime = timedelta(seconds=settings.API_TOKEN_LIFETIME_SECONDS)
        if timezone.now() >= token.created + lifetime:
            token.delete()
            raise AuthenticationFailed('El token expiró. Solicita uno nuevo.')

        return token.user, token
