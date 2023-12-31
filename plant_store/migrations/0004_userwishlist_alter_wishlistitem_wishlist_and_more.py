# Generated by Django 4.2.4 on 2023-08-12 06:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('plant_store', '0003_wishlist_alter_cart_options_wishlistitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserWishList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Wishlist',
                'verbose_name_plural': 'Wishlists',
            },
        ),
        migrations.AlterField(
            model_name='wishlistitem',
            name='wishlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plant_store.userwishlist'),
        ),
        migrations.DeleteModel(
            name='WishList',
        ),
    ]
