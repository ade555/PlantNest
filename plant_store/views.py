from django.http import JsonResponse
from django.views.generic import View, ListView, DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Plant, Products, Cart, CartItem


class PlantListView(ListView):
    model = Plant
    context_object_name = 'plants'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        for plant in context['plants']:
            plant.out_of_stock = plant.quantity_available == 0
        
        return context

class PlantDetailView(DetailView):
    model = Products
    context_object_name ='plant'
    template_name = 'plant_store/plant_detail.html'

# @login_required
# def add_to_cart(request):
#     cart_item = {}
#     cart_item[str(request.GET['id'])] = {
#         "item_name": request.GET['product_name'],
#         "quantity": request.GET['quantity'],
#     }
#     if 'cart_data_session_obj' in request.session:
#         if str(request.GET['id']) in request.session['cart_data_session_obj']:
#             cart_info_data = request.session['cart_data_session_obj']
#             cart_info_data[str(request.GET['id'])]['quantity'] = cart_item[str(request.GET['id'])]
#             cart_info_data.update(cart_info_data)
#             request.session['cart_data_session_obj'] = cart_info_data
#         else:
#             cart_info_data = request.session['cart_data_session_obj']
#             cart_info_data.update(cart_item)
#             request.session['cart_data_session_obj'] = cart_info_data
#     else:
#         request.session['cart_data_session_obj'] = cart_item
#     return JsonResponse({
#         'data':request.session['cart_data_session_obj'],
#         'total_cart_items': len(request.session['cart_data_session_obj'])
#         })

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