from django.urls import path, re_path
from . import views
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from django.conf.urls.static import static
# from django.conf import settings

app_name = 'Consult'

urlpatterns = [
    # Send Request to admin requesting room
    path('requestconsult/', views.RequestConsult, name="request_new_consult"),

    path('sendconsult/', views.SendConsult, name="send_consult"),

    # Stream site
    path('room/', views.Consult, name="consult"),

    # My lobby
    path('', views.CreateRoom, name="create_room"),
    
    # Generate Token
    path('tokengen/', views.gettoken, name="tokengen"),
]