from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('login/', login_page, name='login'),
    path('signup/', singup_page, name='signup'),
    path('addcart/<pizza_uid>/', add_cart, name='addcart'),
    path('cart/', cart, name='cart'),
    path('cart_item_remove/<str:cartitem_uid>/', cart_item_remove, name='cart_item_remove'),
    path('orders/', orders, name='orders'),

    
] 