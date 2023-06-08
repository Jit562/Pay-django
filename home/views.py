from django.shortcuts import redirect, render

from .models import Cart, CartItem, PizzaCat, Pizza
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# Create your views here.

'''
Payment getway instamojo

from instamojo_wrapper import Instamojo
from django.conf import settings
api = Instamojo(api_key=settings.API_KEY,
                auth_token=settings.AUTH_TOKEN, endpoint="https://test.instamojo.com/api/1.1/")

'''

def home(request):
    pizzas = Pizza.objects.all()

    context = {
        'pizzas':pizzas
    }
    return render(request, 'index.html', context)

def login_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user_obj = User.objects.filter(username=username)

            if not user_obj.exists():
                messages.warning(request, 'username not exists ')
                return redirect('/login/')
            
            user_obj = authenticate(username=username, password=password)
            if user_obj:
                login(request, user_obj)
                return redirect('/')
            messages.success(request, 'Wrong password try again')
            return redirect('/login/')
        
        except Exception as e:
            messages.warning(request, 'Somethings wrong try again:-')
            return redirect('/signup/')
    return render(request, 'login.html')

def singup_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user_obj = User.objects.filter(username=username)

            if user_obj.exists():
                messages.warning(request, 'username teken ')
                return redirect('/signup/')
            
            user_obj = User.objects.create(username=username)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request, 'Account created')
            return redirect('/login/')
        
        except Exception as e:
            messages.warning(request, 'Somethings wrong try again:-')
            return redirect('/signup/')
        
    return render(request, 'registration.html')


@login_required(login_url='/login/')
def add_cart(request, pizza_uid):
    user = request.user
    pizza = Pizza.objects.get(uid = pizza_uid)
    cart, _= Cart.objects.get_or_create(user=user, is_paid=False)
    cart_item = CartItem.objects.create(
        cart = cart,
        pizza = pizza
    )

    return redirect('/')


@login_required(login_url='/login/')
def cart(request):
    carts = Cart.objects.get(is_paid = False, user = request.user)
    
    '''
   Payment getway instamojo

    response = api.payment_request_create(
        amount=carts.get_cart_total(),
        purpose="orders",
        buyer_name=request.user.username,
        email="jitu1768@gmail.com",
        redirect_url="http://127.0.0.1:8000/success/"
    )

    print(response)
   
    cart.instamojo_id = response['payment_request']['id']
    cart.save()

    '''
    context ={
        'cart':carts,
        #'payment_url':response['payment_request']['longurl']
    }
    return render(request, 'cart.html' , context)


@login_required(login_url='/login/')
def cart_item_remove(request, cartitem_uid):

    try:
        CartItem.objects.get(uid = cartitem_uid).delete()

        return HttpResponseRedirect('/cart/')
    
    except Exception as e:
        print(e)


@login_required(login_url='/login/')
def orders(request):
    orders = Cart.objects.filter(is_paid=True, user=request.user)

    context = {
        'orders':orders
    }
    return render(request, 'order.html', context) 

'''
Payment getway instamojo

@login_required(login_url='/login/')
def success(request):
    payment_request = request.GET.get('payment_request_id')
    cart = Cart.objects.get(instamojo_id = payment_request)
    cart.is_paid = True
    cart.save()

    return redirect('/orders/')

'''    
