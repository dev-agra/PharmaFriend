from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account, UserProfile
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from carts.models import Cart, CartItem
from carts.views import _cart_id
from orders.models import Order, OrderProduct
from .forms import UserForm, UserProfileForm
from django.shortcuts import get_object_or_404

# Verfification Mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

import requests

# Create your views here.
def RegisterUser(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            city = form.cleaned_data['city_location']
            password = form.cleaned_data['password']
            phone_no = form.cleaned_data['phone_no']
            username = str(email).split('@')[0]

            user = Account.object.create_user(first_name=first_name, last_name=last_name,username=username, email=email,password=password)
            user.city_location = city
            user.phone_no = phone_no
            user.save()

            # When user is created profile is also created in the back
            # Create user profile
            user_profile = UserProfile()
            user_profile.user_id = user.id
            user_profile.profile_pic = 'default/default-user.png'
            user_profile.save()
    
            # User Activation Mail and Activation
            current_site = get_current_site(request)
            mail_subject = "Please Activate your PharmaStore Account"
            message = render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = email
            send_mail = EmailMessage(mail_subject, message, to=[to_email])
            send_mail.send()
            
            context = {'email':email}
            return render(request, 'accounts/verify_msg.html', context=context)
    else:
        form = RegistrationForm()

    context = {
        'form':form,
    }

    return render(request, 'accounts/register.html', context=context)


def LoginUser(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email = email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # Getting the product variations by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variation.all()
                        product_variation.append(list(variation))

                    # Get the cart items from the user to access his product variations
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variation.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    # product_variation = [1, 2, 3, 4, 6]
                    # ex_var_list = [4, 6, 3, 5]

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                print("Entering in Except")
                pass
            login(request, user)
            messages.success(request, "You are logged in")
            # Grab url from where we came
            url = request.META.get('HTTP_REFERER')
            print(11, url)
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/ something similar
                params = dict(x.split('=') for x in query.split('&'))
                # next is key and rest is value
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('accounts:dashboarduser')
        else:
            messages.error(request, "Invalid Credentials Entered!")
            return redirect("accounts:loginuser")
    else:
        return render(request, 'accounts/signin.html')

@login_required(login_url = "accounts:loginuser")
def LogoutUser(request):
    logout(request)
    messages.success(request, "You are logged out!")
    return redirect('pharmastore:storepage')

def ActivateUser(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations!, Your Account is successfully Activated")
        return redirect("accounts:loginuser")
    else:
        messages.error(request, "Invalid Activation Link")    
        return redirect("accounts:registeruser")

@login_required(login_url = "accounts:loginuser")
def DashboardUser(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    userprofile = UserProfile.objects.get(user=request.user)

    context = {
        'order_count':orders_count,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/dashboard.html', context=context)

@login_required(login_url = "accounts:loginuser")
def UserOrders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    orders_count = orders.count()


    context = {
        'orders_count': orders_count,
        'orders': orders,
    }
    return render(request, 'orders/my_orders.html', context=context)

@login_required(login_url = "accounts:loginuser")
def EditProfile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        # In order to update current profile use instance
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your Profile has been updated!")
            return redirect("accounts:editprofile")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'userform': user_form,
        'profileform': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/edit_profile.html', context=context)

@login_required(login_url = "accounts:loginuser")
def ChangePassword(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        conf_new_password = request.POST['conf_new_password']

        user = Account.object.get(username__exact=request.user.username)

        if new_password == conf_new_password:
            # Since passwords are hashed we use check_password
            success = user.check_password(current_password)
            if success:
                # Inbuilt fn so as to hash the password
                user.set_password(new_password)
                user.save()
                # auth.logout If require, django will do by-default!
                messages.success(request, "Password Updated successfully")
                return redirect("accounts:changepassword")
            else:
                messages.error(request, "Wrong password entered!")
                return redirect("accounts:changepassword")
        else:
            messages.error(request, "Passwords entered doesn't match!")
            return redirect("accounts:changepassword")
    return render(request, 'accounts/change_password.html')

@login_required(login_url = "accounts:loginuser")
def OrderDetails(request, order_id):
    # Reason to write like this i.e. __ is since order is foreign key to Order from OrderProduct model, 
    # we can access the order_number of Order from OrderProduct using this __
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity
    shipping = 31.95
    context = {
        'orderdetail': order_detail,
        'order': order,
        'subtotal': subtotal,
        'subtotal_usd': float("{:.2f}".format(subtotal*0.0125)),
        'shipping': shipping,
        'shipping_usd': float("{:.2f}".format(shipping*0.0125)),
    }

    return render(request, "accounts/order_details.html", context=context)

def ForgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.object.filter(email=email).exists():
            # Case sensitive __exact method
            # Case insensitive __iexact method
            user = Account.object.get(email__exact=email)

            # User Activation Mail and Activation
            current_site = get_current_site(request)
            mail_subject = "Request for Password Reset"
            message = render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = email
            send_mail = EmailMessage(mail_subject, message, to=[to_email])
            send_mail.send()
            messages.success(request, "Link for password reset sent to registered email address")
            return redirect("accounts:loginuser")
        else:
            messages.error(request, "Account does not exists!")
            return redirect("accounts:registeruser")
    return render(request, 'accounts/forgotpassword.html')

def ResetPasswordValidateUser(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, "Please Reset Your Password!")
        return redirect('accounts:resetpassword')
    else:
        messages.error(request, "This Link has expired!")    
        return redirect("accounts:loginuser")

# If validation is not done then we wont have uid so it might fail
def ResetPasswordForm(request):
    if request.method == 'POST':
        password = request.POST['new_password']
        cnf_password = request.POST['conf_password']

        if password == cnf_password:
            uid = request.session.get('uid')
            user = Account.object.get(pk=uid)
            # Without .set_password it will not allow it as without it password won't be hashed
            user.set_password(password)
            user.save()
            messages.success(request,"Password Reset Successful")
            return redirect("accounts:loginuser")
        else:
            messages.error(request, "Passwords do not match!")
            return redirect("accounts:resetpassword")
    else:
        return render(request, 'accounts/reset_password.html')