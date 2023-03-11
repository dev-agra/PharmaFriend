from django.shortcuts import render, redirect, get_object_or_404
from pharmastore.models import Product, Variation
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import UserProfile

# To get ID of cart from the sessions key
def _cart_id(request):
    # Get Session key 
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

# To add products int he cart
def add_cart(request, product_id):
    current_user = request.user #Get the current user
    product = Product.objects.get(id=product_id) #get the product
    
    if current_user.is_authenticated:
        # If user is authenticated get cart_item on basis of user and product
        product_variation = []
        # Code segment to get variation
        # request.POST = <QueryDict: {'csrfmiddlewaretoken': ['bgbAnmmOWKnc0RH2PGokfuisFg8Y5bR0G7vGjGyg6mKqNXH7ICk2B1Gy2KAXlifC'], 'strips': ['strip of 20'], 'power': ['xt']}> 
        if request.method == 'POST':
            for item in request.POST:
                # item is key something like 'csrfmiddlewaretoken'
                key = item

                # value is taken from dictionary when key is given
                value = request.POST[key]
                try:
                    # get variation from given values
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    
                    # append the said variation to list [this is done one by one first for strips then for power]
                    product_variation.append(variation)
                except:
                    pass

        # Code Segment to get Cart Item
        # check if cartitem exists, returns a boolean value
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        # if cartitem exists in the gven cart
        if is_cart_item_exists:
            # Will provide us with a single product
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            
            # existing_variations -> database
            # current variation -> product_variation
            # item_id -> database
            
            # Will give all variation associated with the product added in cart
            ex_var_list = []
            id = []
            for item in cart_item:
                # get all variations associated with this item, does this one by one
                existing_variation = item.variation.all()
                
                # Add the variation in the existing one
                ex_var_list.append(list(existing_variation))
                
                # Append the Item ID of the CartItem
                id.append(item.id)

            """product_variation consists of variations done at time of adding to cart and ex_var consists
            of all the variations associated with the item at that particular instant"""
            # So if product variation is found in exiting one just increase quantity by 1            
            
            if product_variation in ex_var_list:
                # get index of product variation found in pehle se hi ex_var_list
                index = ex_var_list.index(product_variation)
                # Since at time of appending the existing variation we also append the id the indexes are same hence access the index
                item_id = id[index]
                # Get the item and increase quantity by 1
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            
            # If item is not found create one
            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                # Say for 1 item we are selecting two diff. variations of "XM" n "XT" in that case product_variation list will have 2 variations in it
                if len(product_variation) > 0:
                    # Clear all the variations for the item
                    item.variation.clear()
                    # Add the product_variation list to the item
                    item.variation.add(*product_variation)
                item.save()

        # If cartitem doesn't exist 
        else:
            # Create a cartitem
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user=current_user,
            )
            # If any variations clear all the add the variation
            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
            cart_item.save()
        return redirect('carts:cartpage')
    else:
        # If user is not authenticated then get cartitem on basis of product and cart
        product_variation = []
        # Code segment to get variation
        # request.POST = <QueryDict: {'csrfmiddlewaretoken': ['bgbAnmmOWKnc0RH2PGokfuisFg8Y5bR0G7vGjGyg6mKqNXH7ICk2B1Gy2KAXlifC'], 'strips': ['strip of 20'], 'power': ['xt']}> 
        if request.method == 'POST':
            for item in request.POST:
                # item is key something like 'csrfmiddlewaretoken'
                key = item

                # value is taken from dictionary when key is given
                value = request.POST[key]
                try:
                    # get variation from given values
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    
                    # append the said variation to list [this is done one by one first for strips then for power]
                    product_variation.append(variation)
                except:
                    pass
            
        # Code Segment to get cart
        try:
            # Get Cart on basis of session key
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
            # Save cart in db
        cart.save()

        # Code Segment to get Cart Item
        # check if cartitem exists, returns a boolean value
        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        # if cartitem exists in the gven cart
        if is_cart_item_exists:
            # Will provide us with a single product
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            
            # existing_variations -> database
            # current variation -> product_variation
            # item_id -> database
            
            # Will give all variation associated with the product added in cart
            ex_var_list = []
            id = []
            for item in cart_item:
                # get all variations associated with this item, does this one by one
                existing_variation = item.variation.all()
                
                # Add the variation in the existing one
                ex_var_list.append(list(existing_variation))
                
                # Append the Item ID of the CartItem
                id.append(item.id)

            """product_variation consists of variations done at time of adding to cart and ex_var consists
            of all the variations associated with the item at that particular instant"""
            # So if product variation is found in exiting one just increase quantity by 1            
            
            if product_variation in ex_var_list:
                # get index of product variation found in pehle se hi ex_var_list
                index = ex_var_list.index(product_variation)
                # Since at time of appending the existing variation we also append the id the indexes are same hence access the index
                item_id = id[index]
                # Get the item and increase quantity by 1
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            # If item is not found create one
            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                # Say for 1 item we are selecting two diff. variations of "XM" n "XT" in that case product_variation list will have 2 variations in it
                if len(product_variation) > 0:
                    # Clear all the variations for the item
                    item.variation.clear()
                    # Add the product_variation list to the item
                    item.variation.add(*product_variation)
                item.save()

        # If cartitem doesn't exist 
        else:
            # Create a cartitem
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            # If any variations clear all the add the variation
            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
            cart_item.save()
        return redirect('carts:cartpage')

# To decrement a item from cart one by one or remove a item from the cart if only one instance present
def remove_cart(request, product_id, cart_item_id):
    # Get Cart from cart id
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:        
            cart= Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect("carts:cartpage")

# To completely remove a product and all its quantity
def remove_cart_item(request, product_id, cart_item_id):

    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart= Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)

    
    cart_item.delete()
    return redirect("carts:cartpage")

#  To view the cart page with all the details mentioned of the product
def Cartpage(request, total=0, quantity=0, cart_items=None):
    try:
        tax= 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        
        tax = (total*18)/100
        grand_total = tax + total
        
    except:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        "grnd_tot": grand_total
    }

    return render(request, 'carts/cart.html', context=context)

@login_required(login_url = "accounts:loginuser")
def checkout_cart(request, total=0, quantity=0, cart_items=None):
    userprofile = UserProfile.objects.get(user=request.user)
    userprofile_json = userprofile.to_json()
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            request.session['userprofile'] = userprofile_json
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            
        tax = (2 * total)/100
        grand_total = tax + total
    except ObjectDoesNotExist:
        tax=0
        grand_total = 0
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        "grnd_tot": grand_total
    }

    return render(request, 'carts/checkoutcart.html', context=context)