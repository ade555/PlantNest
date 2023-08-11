from django.urls import path
from .views import PlantListView, add_to_cart, PlantDetailView, CartView

urlpatterns = [
    path('plants/', PlantListView.as_view(), name = 'plants'),
    path('plants/<int:pk>/', PlantDetailView.as_view(), name='plant-detail'),
    path('cart/', add_to_cart, name='add_to_cart'),
]
