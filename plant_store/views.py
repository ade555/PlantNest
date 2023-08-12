from django.http import JsonResponse
from django.views.generic import View, ListView, DetailView, CreateView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy

from .models import Plant, Products, Cart, CartItem, UserWishList, WishListItem, ProductReview
from .forms import ReviewForm


class PlantListView(ListView):
    model = Plant
    context_object_name = 'plants'

class WishListView(ListView):
        model = UserWishList

class PlantDetailView(DetailView):
    model = Plant
    context_object_name ='plant'
    template_name = 'plant_store/plant_detail.html'

def add_to_cart(request):
    product_id = request.GET.get('id')
    quantity = request.GET.get('quantity')
    product_name = request.GET.get('product_name')

    product = get_object_or_404(Products, id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        cart_item.quantity += int(quantity)
        cart_item.save()
    

    return JsonResponse({
        'total_cart_items': cart.get_total_quantity()
    })


def add_to_wishlist(request):
    product_id = request.GET.get('id')
    product_name = request.GET.get('product_name')

    product = get_object_or_404(Products, id=product_id)

    wish, created = UserWishList.objects.get_or_create(user=request.user)

    # Check if the item already exists in the wishlist
    wish_item = WishListItem.objects.filter(wishlist=wish, product=product).first()

    if wish_item:
        # Item already exists, no need to add it again
        return JsonResponse({
            'error': 'Item already exists in the wishlist'
        }, status=400)
    else:
        # Create a new wishlist item since it doesn't exist
        wish_item = WishListItem.objects.create(wishlist=wish, product=product)

    return JsonResponse({
        'total_wish_items': wish.get_total_items()
    })


class CartView(View):
    def get(self, request, *args, **kwargs):
        products = Products.objects.all()
        user = request.user
        cart_item_count = CartItem.objects.filter(cart__user=user).count() if user.is_authenticated else 0

        context = {
            'products': products,
            'cart_item_count': cart_item_count,
        }
        return render(request, 'product_listing.html', context)
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        product = Products.objects.get(id=product_id)
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)

        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not item_created:
            cart_item.quantity += quantity
            cart_item.save()

        response_data = {'message': 'Item added to cart'}
        return JsonResponse(response_data)

class ProductReview(CreateView):
    model = ProductReview
    form_class = ReviewForm
    success_url = reverse_lazy('plants')  # Redirect to the product list after submission

    def form_valid(self, form):
        product = get_object_or_404(Products, id=self.kwargs['product_id'])
        form.instance.product = product
        form.instance.user = self.request.user
        return super().form_valid(form)