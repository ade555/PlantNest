from django.urls import path
from .views import PlantListView, add_to_cart, PlantDetailView, CartView, add_to_wishlist, ProductReview, WishListView, RemoveFromWishlistView, empty_cart, AccessoryListView, AccessoryDetailView
app_name = "plant_store"
urlpatterns = [
    path('plants/', PlantListView.as_view(), name = 'plants'),
    path('plants/<int:pk>/', PlantDetailView.as_view(), name='plant-detail'),
    path('cart/', add_to_cart, name='add_to_cart'),
    path('cart/list/', CartView.as_view(), name='cart'),
    path('wish/', add_to_wishlist, name='wish'),
    path('product/<int:product_id>/add_review/', ProductReview.as_view(), name='add_review'),
    path('wish/list/', WishListView.as_view(), name='wishlist'),
    path('remove_from_wishlist/', RemoveFromWishlistView.as_view(), name='remove_from_wishlist'),
    path('cart/empty/', empty_cart, name='empty_cart'),
    path('accessories/', AccessoryListView.as_view(), name='accessories'),
    path('accessories/<int:pk>/', AccessoryDetailView.as_view(), name='accessory-detail'),
]
