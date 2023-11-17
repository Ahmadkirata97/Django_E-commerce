from django.shortcuts import render
from .models import *
from django.http import JsonResponse  
import json  
import datetime
from .utils import cookieCart, cartData, guestOrder

# Create your views here.



def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    items = data['items']
    order = data['order']
    product = Product.objects.all()
        
    context = {'items':items, 'order':order, 'cartItems':cartItems, 'products':product}
    return render(request, 'store/store.html', context)





def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    items = data['items']
    order = data['order']
    #print(order)
    print(items)
        
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)







def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    items = data['items']
    order = data['order']
        
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)






def updateItem(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']

    print('Action:', action)
    print('ProductID:', productID)

    customer = request.user.customer
    product = Product.objects.get(id=productID)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'Add' :
        orderitem.quantity = orderitem.quantity + 1
    elif action == 'Remove' :
        orderitem.quantity = orderitem.quantity - 1

    orderitem.save()

    if orderitem.quantity <= 0 :
        orderitem.delete()
    return JsonResponse('Item was added', safe=False)






def processOrder(request):

    transactionId = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated :
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
       
        
    else:
       customer, order = guestOrder(request, data)
        
    total = float(data['form']['total'])
    order.transaction_id = transactionId
    if total == float(order.getCartTotal):
        order.complete = True
    order.save()

    if order.Shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )


    
    return JsonResponse('Payment Was Completed!', safe=False) 