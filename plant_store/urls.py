from django.urls import path
from .views import PlantListView, add_to_cart, PlantDetailView, CartView, add_to_wishlist, ProductReview

urlpatterns = [
    path('plants/', PlantListView.as_view(), name = 'plants'),
    path('plants/<int:pk>/', PlantDetailView.as_view(), name='plant-detail'),
    path('cart/', add_to_cart, name='add_to_cart'),
    path('wish/', add_to_wishlist, name='wish'),
    path('product/<int:product_id>/add_review/', ProductReview.as_view(), name='add_review'),
]
