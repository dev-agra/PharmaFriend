"""Pharmafriend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404, handler500

urlpatterns = [

    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),

    # For user to go to Admin site
    path('securelogin/', admin.site.urls),

    # For User Access to PharmaFriend
    path('', include('application.urls')),

    # For User Access to  Pharmastore
    path('pharmastore/', include('pharmastore.urls')),

    # To User Access to cart of Pharmastore
    path('pharmastore/cart/', include('carts.urls')),

    # For User Access to account in Pharmastore
    path('pharmastore/accounts/', include('accounts.urls')),
                                          
    # For User to access Order pages
    path('pharmastore/orders/', include('orders.urls')),

    # For user Consulting Doctor
    path('Consult/', include('consultvideo.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler500 = 'application.views.error_500'
handler400 = 'application.views.error_400'
handler404 = 'application.views.error_404'