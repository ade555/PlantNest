from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView, DetailView, CreateView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy

from .models import Plant, Products, Cart, CartItem, UserWishList, WishListItem, ProductReview, Accessory, PlantCategory
from .forms import ReviewForm

class PlantListView(ListView):
    model = Plant
    context_object_name = 'plants'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Get the default context
        
        plant_categories = list(PlantCategory.objects.values_list('plant_category_name', flat=True).distinct())
        products = Products.objects.filter(product_type="plant")
        product_id = [product.id for product in products]
        plants_and_ids = zip(context['plants'], product_id)
        context['plants_and_ids'] = plants_and_ids
        context['plant_categories'] = plant_categories
        return context
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Plant.objects.filter(product_name__icontains=query)
        else:
            return Plant.objects.all()

class WishListView(ListView):
    model = WishListItem
    context_object_name = 'wishes'

class RemoveFromWishlistView(View):
    def get(self, request, *args, **kwargs):
        product_id = request.GET.get("id")
        product = get_object_or_404(Products, id=product_id)

        wish = get_object_or_404(UserWishList, user=request.user)
        wish_item = WishListItem.objects.filter(wishlist=wish, product=product).first()

        if wish_item:
            wish_item.delete()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"error": "Item not found in the wishlist"}, status=400)

class PlantDetailView(DetailView):
    model = Plant
    context_object_name ='plant'
    template_name = 'plant_store/plant_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Get the default context
        
        plant = self.object  # The Plant instance for this view
        product_id = plant.products_ptr.id  # Get the ID of the associated Products instance

        context['product_id'] = product_id
        return context

class AccessoryListView(ListView):
    model = Accessory
    context_object_name = 'accessories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Get the default context
        
        products = Products.objects.filter(product_type="accessory")
        product_id = [product.id for product in products]
        accessories_and_ids = zip(context['accessories'], product_id)
        context['accessories_and_ids'] = accessories_and_ids
        return context
        
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Accessory.objects.filter(product_name__icontains=query)
        else:
            return Accessory.objects.all()

class AccessoryDetailView(DetailView):
    model = Accessory
    context_object_name = 'accessory'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Get the default context
        
        accessory = self.object  # The Accessory instance for this view
        product_id = accessory.products_ptr.id  # Get the ID of the associated Products instance

        context['product_id'] = product_id
        return context

@login_required
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

@login_required
def empty_cart(request):
    cart = Cart.objects.get(user=request.user)
    cart.cartitem_set.all().delete()
    cart.delete()
    return redirect('cart')  # Redirect back to the cart page

@login_required
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
        user = request.user

        cart_items = CartItem.objects.filter(cart__user=user) if user.is_authenticated else []
        total_amount = sum(cart_item.product.product_price * cart_item.quantity for cart_item in cart_items)

        context = {
            'cart_items': cart_items,
            'total_amount': total_amount,
        }
        return render(request, "plant_store/cart.html", context)
    
    def post(self, request, *args, **kwargs):
        cart_item_id = request.POST.get('cart_item_id')
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)

        # Check if a 'remove' action is provided. This will mean that the user wants to remove an item from their cart
        if 'remove' in request.POST:
            # Remove the cart item and the cart if it becomes empty
            cart = cart_item.cart
            cart_item.delete()
            if not cart.cartitem_set.exists():
                cart.delete()
            return redirect('cart')
        
        # Check if a 'update_quantity' action is provided. This will mean that the user wants to increase or reduce the number of an item in their cart
        elif 'update_quantity' in request.POST:
            # Get new quantity of product if user decides to update the quantity
            new_quantity = int(request.POST.get('new_quantity'))
            # update the new quantity
            cart_item.quantity = new_quantity
            # save the new quantity
            cart_item.save()
            return redirect('cart')

class ProductReview(CreateView):
    model = ProductReview
    form_class = ReviewForm
    context_object_name = 'product'
    success_url = reverse_lazy('plants')  # Redirect to the product list after submission
    

    def form_valid(self, form):
        product = get_object_or_404(Products, id=self.kwargs['product_id'])
        form.instance.product = product
        form.instance.user = self.request.user
        return super().form_valid(form)