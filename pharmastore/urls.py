from django.urls import path
from . import views

app_name = 'pharmastore'

urlpatterns = [
    #Home page for the user
    path('', views.Homepage, name="homepage"),
    path('store/', views.Storepage, name="storepage"),
    path('store/category/<slug:category_slug>/', views.Storepage, name="products_by_category"),
    path('store/category/<slug:category_slug>/<slug:product_slug>/', views.Productpage, name="products_view_page"),
    path('store/search/', views.Search, name="searchpage"),
    path('submitreview/<int:product_id>/', views.SubmitReview, name="submit_review"),
    ]