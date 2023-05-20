from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROLE_CHOICES = (
        ('Customer', 'Customer'),
        ('Rider', 'Rider'),
        ('Merchants', 'Merchants'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Customer')
    def __str__(self):
        return self.user.username
    
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=False)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    phone = models.IntegerField(default=0)
    state  = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.name

class Merchants(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    phone = models.IntegerField(default=0)
    address_rd = models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.name
       
class Product(models.Model):
    merchants =  models.ForeignKey(Merchants, on_delete=models.CASCADE,blank=True, null=True)
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    address = models.CharField(max_length=200,null=True)
    image = models.ImageField(null=True, blank=True)
    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    @property
    def total_cost(self):
        return self.quantity * self.product.price


STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the way','On the way'),
    ('Delivered', 'Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    @property
    def total_cost(self):
        return self.quantity * self.product.price + 30
    
Status_Choices = (
    ('CarNumber','CarNumber'),
    ('Car','Car'),
    ('motorbike','motorbike'),
)
class Rider(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    xe = models.CharField(max_length=50, choices=Status_Choices, default='CarNumber')
    phone = models.IntegerField(default=0)
    address_rd = models.CharField(max_length=200,null=True)
    image = models.ImageField(null=True, blank=True)
    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class RiderSavedOrders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE, blank=True, null=True)
    orders = models.ForeignKey(OrderPlaced, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    xe = models.CharField(max_length=50, choices=Status_Choices, default='CarNumber')
    phone = models.IntegerField(default=0)
    address_rd = models.CharField(max_length=200,null=True)
    image = models.ImageField(null=True, blank=True)
    def __str__(self):
        return self.name
