from django.shortcuts import render,redirect
from .models import *
from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import  get_object_or_404
# Create your views here.


def logout_view(request):
    logout(request)
    return redirect('store')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            # Display an error message or handle authentication failure
            pass

    return render(request, 'store/login.html')



def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Add validation and error handling as needed
        # For simplicity, we'll assume the passwords match

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password1)

        # Log the user in
        login(request, user)
        return redirect('store')

    return render(request, 'store/register.html')

def store(request):
	if request.user.is_authenticated : 
		customer =request.user.customer
		order,created= Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
		cartItems =order.get_cart_items
	else:
		items=[]
		order ={'get_cart_total':0,'get_cart_items':0,'shipping':False}
		cartItems=order['get_cart_items']
	products = Product.objects.all()
	context = {'products':products,'cartItems':cartItems,}
	return render(request, 'store/store.html', context)

def cart(request):
	if request.user.is_authenticated :
		customer = request.user.customer
		order ,created = Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
		cartItems =order.get_cart_items

	else:
		items=[]
		order ={'get_cart_total':0,'get_cart_items':0,'shipping':False}
		cartItems=order['get_cart_items']
	context = {'items':items,'order':order,'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	if request.user.is_authenticated : 
		customer =request.user.customer
		order,created= Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
		cartItems =order.get_cart_items
	else:
		items=[]
		order ={'get_cart_total':0,'get_cart_items':0,'shipping':False}
		cartItems=order['get_cart_items']

	context = {'items':items,'order':order,'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)




def updateItem(request):
	data = json.loads(request.body)
	productId= data['productId']
	action  = data ['action']
	print('Action',action)
	print('Product Id',productId)


	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order,created =Order.objects.get_or_create(customer= customer, complete= False )
	orderItems,created= OrderItem.objects.get_or_create(order=order,product=product)
	if action == 'add':
		orderItems.quantity = (orderItems.quantity)+1
	elif action == 'remove':
		orderItems.quantity = (orderItems.quantity)-1
	
	orderItems.save()

	if orderItems.quantity <= 0:
		orderItems.delete()

	return JsonResponse("Item was Added",safe=False)


def processOrder (request):
	print('data ',request.body)
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)
	if request.user.is_authenticated:
		customer = request.user.customer
		order,created =Order.objects.get_or_create(customer= customer, complete= False )
		total = float(data['form']['total'])
		order.transaction_id = transaction_id

		if total == order.get_cart_total:
			order.complete=True
		order.save()
		if order.shipping == True :
			ShippingAddress.objects.create(
				customer = customer,
				order=order,
				address = data['shipping']['address'],
				city = data['shipping']['city'],
				state = data['shipping']['state'],
				zipcode = data['shipping']['zipcode'],
			)
	return JsonResponse("Payment completed" ,safe=False)



def product(request,id):
	products=Product.objects.filter(id=id)
	print(products)
	context = {'products':products}
	return render(request, 'store/product.html', context)


def checkout_product(request, product_id):
    # Get the product based on the product_id
    product = get_object_or_404(Product, id=product_id)

    # Assuming you have a checkout view that handles the checkout process
    # Here you would process the checkout for the specific product
    # This is a placeholder, modify this according to your actual checkout logic
    # For demonstration purposes, we'll redirect to the main checkout page
    return redirect('checkout')