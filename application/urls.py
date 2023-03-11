from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

app_name = 'pharmafriend'

urlpatterns = [
    #Home page for the user
    path('', views.Homepage, name="homepage"),

    # To search for medicines and get a price comparision
    path('Search/', views.Search, name="searchpage"),

    # To view different medicines
    path('Store/', views.Store, name="storepage"),

    path('Doctor/', views.Doctor, name="doctorpage"),

    path('About/', views.About, name="aboutpage"),

    path('Contact/', views.Contact, name="contactpage"),

    # To get info for website
    path('Medicine/', views.Medicine, name="medicinepage"),

    # Locate the medical store with the required medicines
    path('Locate/', views.Locate, name="locatepage"),

    path('Addmeds/', views.AddMeds, name="addnames"),

    path('GovMeds/', views.GovMeds, name="govmeds"),

    path('SignupMedical/', views.signupaction, name="signupmed"),

    path('LoginMedical/', views.loginaction, name="loginmed"),

    path('Pharmacy/', views.Pharmacy, name="pharmacy"),

    path('Logoutmeds/', views.logoutmeds, name="logoutmeds"),
    
    ]