from django.urls import path
from .views import HandshakeView, ReviewListCreateView, ReviewDetailView

urlpatterns = [
    path('handshake/', HandshakeView.as_view(), name='handshake'),
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]
