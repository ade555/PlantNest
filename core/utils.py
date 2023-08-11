from django.forms.utils import ErrorList
from django.shortcuts import redirect

# a custom error class for form errors
class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ""
        return f"""
                <div class="text-sm text-danger">
                      {''.join(['<p>%s</p>' % e for e in self])}
                </div>
         """
    

class GenericCartUtility:
    def __init__(self, cart_model, cart_item_model, plant_model):
        self.cart_model = cart_model
        self.cart_item_model = cart_item_model
        self.plant_model = plant_model

    def add_to_cart(self, request, plant_id):
        plant = self.plant_model.objects.get(pk=plant_id)
        cart, created = self.cart_model.objects.get_or_create(user=request.user)
        cart_item, item_created = self.cart_item_model.objects.get_or_create(plant=plant, cart=cart, defaults={'quantity': 1})
        
        if not item_created:
            cart_item.quantity += 1
            cart_item.save()
        
        return redirect('plant_detail', plant_id=plant_id)

    def get_cart_data(self, request):
        cart, created = self.cart_model.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
        total_price = sum(item.plant.price * item.quantity for item in cart_items)
        return cart_items, total_price


class GenericWishlistUtility:
    def __init__(self, wishlist_model, plant_model):
        self.wishlist_model = wishlist_model
        self.plant_model = plant_model

    def add_to_wishlist(self, request, plant_id):
        plant = self.plant_model.objects.get(pk=plant_id)
        wishlist, created = self.wishlist_model.objects.get_or_create(user=request.user)
        wishlist.plants.add(plant)
        return redirect('plant_detail', plant_id=plant_id)

    def get_wishlist_data(self, request):
        wishlist, created = self.wishlist_model.objects.get_or_create(user=request.user)
        wishlist_plants = wishlist.plants.all()
        return wishlist_plants
