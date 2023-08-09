from django.contrib import admin

# create a new custom admin panel for the website admin
class CustomAdmin(admin.AdminSite):
    site_header = 'PlantNest'

custom_admin = CustomAdmin(name='custom-admin')