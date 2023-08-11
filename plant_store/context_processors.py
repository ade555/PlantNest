# myapp/context_processors.py

from .models import Cart  # Make sure to import your Cart model here

def cart_quantity(request):
    total_cart_items = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            total_cart_items = cart.get_total_quantity()
    
    return {'total_cart_quantity': total_cart_items}

