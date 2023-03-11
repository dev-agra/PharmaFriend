from django.shortcuts import render, redirect
from carts.models import CartItem
from .forms import OrderForm
from pharmastore.models import Product
from .models import Order, Payment, OrderProduct
import datetime
import json
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from accounts.models import UserProfile
from django.shortcuts import get_object_or_404

def returncap(str):
    str1 = ' '
    for i in range(len(str.split(" "))):
        str1 += str.split(" ")[i].title() + ' '
    return str1.strip()

def PaymentOrder(request):
    body = json.loads(request.body)
    print(1, body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        status = body['status'],
        amount_paid = order.order_total
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the cart item to the Order Product Table
    cart_item = CartItem.objects.filter(user=request.user)

    for item in cart_item:
        order_product = OrderProduct()
        order_product.order_id = order.id
        order_product.payment = payment
        order_product.user_id = request.user.id
        order_product.product_id = item.product_id
        order_product.quantity = item.quantity
        order_product.product_price = item.product.price
        order_product.ordered = True
        
        # To store many to may field first store then save/alot
        order_product.save()
        # order_product.variations = item.variation
        # order_product.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variation.all()
        order_product = OrderProduct.objects.get(id=order_product.id)
        order_product.variations.set(product_variation)
        order_product.save()

        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # Delete Cart Instance
    CartItem.objects.filter(user=request.user).delete()

    # current_site = get_current_site(request)
    # Send email to customer
    mail_subject = "Thank you for your order"
    message = render_to_string('orders/order_receive_mail.html',{
        'user':request.user,
        'order': order,
    })

    to_email = request.user.email
    send_mail = EmailMessage(mail_subject, message, to=[to_email])
    send_mail.send()

    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)


# Create your views here.
# Fn to place order
def PlaceOrder(request, total=0, quantity=0):
    current_user = request.user
    # If the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('pharmastore:storepage')
    
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        grand_total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    
    total = grand_total
    tax = (grand_total*18)/100
    shipping = 31.95 #In INR
    grand_total = total + shipping + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phoneno = form.cleaned_data['phoneno']
            data.email = form.cleaned_data['email']
            data.address_line_1 = returncap(str(form.cleaned_data['address_line_1']))
            data.address_line_2 = returncap(str(form.cleaned_data['address_line_2']))
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.pin = form.cleaned_data['pin']
            data.note = form.cleaned_data['note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            
            order = Order.objects.get(user=current_user, is_ordered=False, order_number = order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': float("{:.2f}".format(total*0.0125)),
                'grand_total': float("{:.2f}".format(grand_total*0.0125)),
                'shipping': float("{:.2f}".format(shipping*0.0125)),
                'tax': float("{:.2f}".format(tax*0.0125))
            }
            return render(request, 'orders/payment_order.html', context=context)
    else:
        return redirect('carts:checkout_cart')

def OrderComplete(request):
    order_number = request.GET.get('order_number')
    cart_items = CartItem.objects.filter(user=request.user)
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        payment = Payment.objects.get(payment_id=transID)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity
        shipping = 31.95
        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
            'subtotal_usd': float("{:.2f}".format(subtotal*0.0125)),
            'shipping': shipping,
            'shipping_usd': float("{:.2f}".format(shipping*0.0125)),
        }
        return render(request, 'orders/order_complete.html', context=context)
    
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('pharmastore:storepage')
