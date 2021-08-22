from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import datetime

class BaseEntity(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Category(BaseEntity):
    name = models.CharField(max_length=90, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='sub_category')
    category_image = models.ImageField(upload_to='category/%Y/%m/%d', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_children(self):
        return Category.objects.filter(parent=self)


class ATM(BaseEntity):
    title = models.CharField(max_length=180)
    price = models.IntegerField(default=0)
    addon = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    other_info = models.TextField(null=True)
    date = models.DateField(null=True, auto_now=True)
    def __str__(self):
        return self.title

class Tag(BaseEntity):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name


class Inventory(BaseEntity):
    name = models.CharField(max_length=120)
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='productCategory')
    short_description = models.CharField(max_length=250)
    full_description = models.TextField()
    current_stock = models.IntegerField(default=0)
    purchase_price = models.IntegerField(default=0)
    sales_price = models.IntegerField(default=0)
    promotional_price = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True, related_name='inventory_tag')
    picture = models.ImageField(upload_to='inventory/%Y/%m/%d', default="avatar.png", blank=True)

    def __str__(self):
        return self.name



class Cart(BaseEntity):
    products = models.ManyToManyField(Inventory, null=True)
    method = models.CharField(max_length=250,default='cash',null=True,blank=True)
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.total


class Customer(BaseEntity):
    owner = models.OneToOneField(User, related_name='customers', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=14, unique=True)
    shop_name = models.CharField(max_length=90, unique=True)
    nid_number = models.IntegerField(max_length=20, unique=True)
    trea_liance = models.CharField(max_length=50, unique=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='customer/%Y/%m/%d', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.shop_name[:15]
   



class Invocie(BaseEntity):
    pass



# order by user
class Order(BaseEntity):
    full_name = models.CharField(max_length=60, blank=True, null=True)
    phn_number = models.CharField(max_length=14, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f'{self.id} {self.full_name}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


# order Item list
class OrderItem(BaseEntity):
    orderItem = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    method    = models.CharField(max_length=60, blank=True, null=True)
    products = models.ForeignKey(Inventory, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    date = models.DateField(null=True, auto_now=True)
    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        return self.price * self.quantity


