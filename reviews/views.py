from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import HandshakeToken, Review
from .permissions import HandshakePermission
from .serializers import ReviewSerializer


class HandshakeView(APIView):
    """
    POST /api/dinasour/handshake/

    Step 1 of every write operation.
    Returns a one-time token the client must include as the
    X-Handshake-Token header when calling any write endpoint.
    Token expires after 60 seconds and is invalidated after one use.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        token = HandshakeToken.objects.create()
        return Response(
            {
                "status": "ready",
                "message": "Handshake successful. Use the token for your write request.",
                "token": str(token.token),
                "expires_in_seconds": HandshakeToken.EXPIRY_SECONDS,
                "usage": "Add header:  X-Handshake-Token: <token>",
            },
            status=status.HTTP_201_CREATED,
        )


class ReviewListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/dinasour/reviews/   → list all reviews      (no token needed)
    POST /api/dinasour/reviews/   → create a new review   (handshake required)
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [HandshakePermission]


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/dinasour/reviews/<id>/  → retrieve one review   (no token needed)
    PUT    /api/dinasour/reviews/<id>/  → full update            (handshake required)
    PATCH  /api/dinasour/reviews/<id>/  → partial update         (handshake required)
    DELETE /api/dinasour/reviews/<id>/  → delete                 (handshake required)
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [HandshakePermission]
