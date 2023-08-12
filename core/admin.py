from django.contrib import admin
from django.db.models import Sum
from plant_store.models import Products, Cart, User

class CustomAdmin(admin.AdminSite):
    site_header = 'PlantNest'

    def index(self, request, extra_context=None):
        # Calculate the required data for the dashboard
        total_users = User.objects.count()
        total_products = Products.objects.count()
        total_orders = Cart.objects.count()
        total_stock = Products.objects.aggregate(total_stock=Sum('quantity_available'))['total_stock']

        context = {
            'total_users': total_users,
            'total_products': total_products,
            'total_orders': total_orders,
            'total_stock': total_stock,
        }

        return super().index(request, extra_context=context)

custom_admin = CustomAdmin(name='custom-admin')
