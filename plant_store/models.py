from django.db import models
from django.db.models import Sum


from users.models import User

# a tuple to hold the product types
PRODUCT_TYPE = (
('plant', 'Plant'),
('accessory', 'Accessory'),
)
PLANT_CATEGORIES = (
    ('flowering', 'Flowering'),
    ('non-flowering', 'Non-flowering'),
    ('indoor', 'Indoor'),
    ('outdoor', 'Outdoor'),
    ('succulents', 'Succulents'),
    ('medicinal', 'Medicinal'),
)

ACCESSORY_CATEGORIES = (
    ('tools', "Tools"),
    ('vase', "Vase"),
    ('supplies', 'Supplies')
)

class PlantCategory(models.Model):
    plant_category_name = models.CharField(max_length=20, choices=PLANT_CATEGORIES, unique=True)

    def __str__(self):
        return self.plant_category_name
    class Meta:
        verbose_name_plural = "Plants Categories"
        verbose_name = "Plant Category"

class AccessoryCategory(models.Model):
    acessory_category_name = models.CharField(max_length=20, choices=ACCESSORY_CATEGORIES, unique =True)

    def __str__(self):
        return self.acessory_category_name
    class Meta:
        verbose_name_plural = "Accessories Categories"
        verbose_name = "Acessory Category"

class Products(models.Model):
    product_name = models.CharField(max_length=255)
    product_price = models.PositiveIntegerField()
    product_type = models.CharField(max_length=30, choices=PRODUCT_TYPE)
    is_available = models.BooleanField(default=True)
    product_description = models.TextField()
    product_image = models.ImageField(upload_to="product_images")
    quantity_available = models.PositiveIntegerField()

    def get_product_availability(self):
        return self.quantity_available == 0

    def __str__(self):
        return f"{self.product_name}"

class Plant(Products):
    plant_category = models.ForeignKey(PlantCategory, on_delete=models.CASCADE)
    plant_species = models.CharField(max_length=60)

    def __str__(self):
        return self.product_name

class Accessory(Products):
    accessory_category = models.ForeignKey(AccessoryCategory, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Plant Accessory"
        verbose_name_plural = "Plant Acessories"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"
    
    def get_cart_items(self):
        return CartItem.objects.filter(cart=self)

    def get_total_price(self):
        cart_items = self.get_cart_items()
        total_price = sum(item.product.product_price * item.quantity for item in cart_items)
        return total_price
    
    def get_total_quantity(self):
        cart_items = self.get_cart_items()
        total_quantity = sum(item.quantity for item in cart_items)
        return total_quantity
    
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Cart items for - {self.product.product_name} - Quantity: {self.quantity}"

class UserWishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_items(self):
        return self.wishlistitem_set.count()

    class Meta:
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"

class WishListItem(models.Model):
    wishlist = models.ForeignKey(UserWishList, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    def __str__(self):
        return f"Wish list item - {self.product.product_name}"


class ProductReview(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.product.product_name} by {self.user.username}"
