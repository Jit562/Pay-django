from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models import Sum

# Create your models here.

class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class PizzaCat(BaseModel):

    cat_name = models.CharField(max_length=100)


class Pizza(BaseModel):
    category = models.ForeignKey(PizzaCat, on_delete=models.CASCADE, related_name='pizzas')
    pizza_name = models.CharField(max_length=80)
    prize = models.IntegerField(default=100)
    images = models.ImageField(upload_to='pizza')

class Cart(BaseModel):
    user = models.ForeignKey(User,null=True, blank=True, on_delete=models.SET_NULL, related_name='carts')
    is_paid = models.BooleanField(default=False)
    instamojo_id = models.CharField(max_length=1000) 

    def get_cart_total(self):
        return CartItem.objects.filter(cart = self).aggregate(Sum('pizza__prize'))['pizza__prize__sum']

class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_item')    
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)    





