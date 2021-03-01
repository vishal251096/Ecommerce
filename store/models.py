from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from .utils import unique_order_id_generator

CATEGORY_CHOICES = (
    ('M&F', 'Meat and Fish'),
    ('F&V', 'Fruits and Vegetables'),
    ('Cooking', 'Cooking'),
    ('Beverages', 'BEVERAGES'),
    ('H&C', 'Home and Cleaning'),
    ('Pest Control', 'Pest Control'),
    ('Ofc Prod', 'Office Products'),
    ('Bt Prod', 'Beauty Products'),
    ('Hea Prod', 'Health Products'),
    ('PetCare', 'Pet Care'),
    ('Home App', 'Home Appliances'),
    ('Babycare', 'Baby Care'),
    ('fashion','Fashion'),
    ('TW', 'Top Wear'),
    ('BW', 'Bottom Wear'),
)


class Product(models.Model):
    name = models.CharField(max_length = 100)
    selling_price = models.FloatField()
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    brand = models.CharField(max_length=30)
    quantity = models.PositiveIntegerField(default=1)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)


class Profile(User):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_profile', null=True, blank=True)
    mobile = models.IntegerField()
    alternate_mobile = models.IntegerField()
    


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    address_line_1 = models.CharField(max_length=200)
    address_line_2 = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.quantity * self.product.selling_price)

    @property
    def item_total(self):
        return self.quantity * self.product.selling_price


ORDER_STATUS = (
    ('Accepted','Accepted'),
    ('Pending','Pending'),
    ('Shipped','Shipped'),
    ('Cancelled','Cancelled'),
    ('Delivered','Delivered')
)

class OrderList(models.Model):
    order_id = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='Pending')
    date = models.DateTimeField(auto_now_add=True)

def pre_save_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)

pre_save.connect(pre_save_order_id, sender=OrderList)