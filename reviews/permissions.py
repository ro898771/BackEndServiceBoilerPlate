from rest_framework.permissions import BasePermission
from .models import HandshakeToken


class HandshakePermission(BasePermission):
    """
    Read operations (GET, HEAD, OPTIONS) are always allowed.
    Write operations (POST, PUT, PATCH, DELETE) require a valid
    one-time handshake token supplied in the X-Handshake-Token header.

    The token is consumed (marked used) immediately on first valid use.
    """

    SAFE_METHODS = ("GET", "HEAD", "OPTIONS")

    message = (
        "A valid X-Handshake-Token header is required for write operations. "
        "Call POST /api/dinasour/handshake/ first to obtain a token."
    )

    def has_permission(self, request, view):
        if request.method in self.SAFE_METHODS:
            return True

        token_value = request.headers.get("X-Handshake-Token")
        if not token_value:
            return False

        try:
            token = HandshakeToken.objects.get(token=token_value, used=False)
        except (HandshakeToken.DoesNotExist, ValueError):
            return False

        if not token.is_valid():
            return False

        # Consume the token — one-time use only
        token.used = True
        token.save(update_fields=["used"])
        return True
