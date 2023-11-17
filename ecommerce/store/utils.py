import json
from .models import *
from django.shortcuts import render

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        
    print('Cart:', cart)
    items = []
    order = {'getCartItems':0, 'getCartTotal':0, 'Shipping':False}
    cartItems = order['getCartItems']

    for c in cart :
        try:
            cartItems += cart[c]['quantity']
            product = Product.objects.get(id=c)
            print('ID=', c)
            print('Quantity=',cart[c]['quantity'])
            print('Price=', product.price)
            total = product.price * cart[c]['quantity']
            print('Total=', total)

            order['getCartItems'] += cart[c]['quantity']
            order['getCartTotal'] += total

            item = {
                'product':{
                    'id':product.id,
                    'name': product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                },
                'quantity':cart[c]['quantity'],
                'get_total':total
            }
            items.append(item)
            if product.digital == False :
                order['Shipping'] = True

            
        except:
            pass  
    return{'cartItems':cartItems, 'order':order, 'items':items}






def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.getCartItems
    else:
        cookiesData = cookieCart(request)
        cartItems = cookiesData['cartItems']
        order = cookiesData['order']
        items = cookiesData['items']

    return{'cartItems':cartItems, 'order':order, 'items':items}






def guestOrder(request, data):
    print('User is not Logged in!')
    print('Cookies:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookiesData = cookieCart(request)
    items = cookiesData['items']
    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()
    order = Order.objects.create(customer=customer, coomplete=False)
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(produc=product, order=order, quantity=item['quantity'])


    return(customer, order)