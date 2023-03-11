from django.shortcuts import render, get_object_or_404, redirect
from pharmastore.models import Product, ReviewRating, ProductGalllery
from category.models import Category
from django.shortcuts import HttpResponse
from carts.models import Cart, CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib import messages
from .forms import ReviewForm
from orders.models import Order, OrderProduct

# Create your views here.
def Homepage(request):
    reviews = None
    products = Product.objects.all().filter(is_available=True).order_by('-created_date')

    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        'products': products,
        'reviews': reviews,
    }

    return render(request, 'pharmastore/index.html', context=context)

def Storepage(request, category_slug=None):
    categories = None
    products = None
    product_count = 0

    if category_slug != None:
        # Get products on the basis of category
        categories = get_object_or_404(Category, slug = category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page') #Get the 'page' keyword from the URL i.e. ?page=2
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        # Get products irrespective of category
        products = Product.objects.all().filter(is_available=True).order_by('-created_date')
        paginator = Paginator(products, 6)
        page = request.GET.get('page') #Get the 'page' keyword from the URL i.e. ?page=2
        paged_products = paginator.get_page(page)
        product_count = products.count()

    # To add false or inflated value so as to strike it through
    for i in range(len(paged_products)):
        paged_products[i].infprice = paged_products[i].price + (paged_products[i].price * 15/100)

    context = {
        'products': paged_products,
        'products_count': product_count,
    }
    
    return render(request, 'pharmastore/store.html', context=context)

def Productpage(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    
    except Exception as e:
        raise e
    
    if request.user.is_authenticated:
        try:
            order_product = OrderProduct.objects.filter(user=request.user, product_id = single_product.id).exists()
        except OrderProduct.DoesNotExist:
            order_product = None
    else:
        order_product = None

    product_review = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    product_gallery = ProductGalllery.objects.filter(product_id=single_product.id)
    
    context = {
        'single_product': single_product,
        'in_cart':in_cart,
        'order_product': order_product,
        'product_review': product_review,
        'product_gallery': product_gallery,
    }

    return render(request, 'pharmastore/product-detail.html', context=context)

def Search(request, category_slug=None):
    keyword = None
    products = None
    product_count = None
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
            
            for i in range(len(products)):
                products[i].infprice = products[i].price + (products[i].price * 15/100)

    context = {
        "keyword": keyword,
        "products": products,
        "products_count":product_count,
    }
    return render(request, 'pharmastore/search-result.html', context=context)

def SubmitReview(request, product_id):
    url = request.META.get('HTTP_REFERER')
    print(1, url)
    if request.method == 'POST':
        try:
            review = ReviewRating.objects.get(user__id = request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=review)
            form.save()
            messages.success(request, "Thank You! Your review has been updated")
            return redirect(url)

        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thank You! Your review has been updated")
                
                return redirect(url)
            
 