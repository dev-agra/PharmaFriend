from django.urls import path
from .import views

app_name = 'accounts'

urlpatterns = [
    path('user/register', views.RegisterUser, name="registeruser"),
    path('user/login', views.LoginUser, name="loginuser"),
    path('user/logout', views.LogoutUser, name="logoutuser"),
    path('user/dashboard', views.DashboardUser, name="dashboarduser"),

    # For Forgor and Rest password functionality
    path('user/forgotpassword', views.ForgotPassword, name="forgetpassword"),
    path('user/resetpassword', views.ResetPasswordForm, name="resetpassword"),

    # For user identification and validation in Account activation
    path('user/activate/<uidb64>/<token>/', views.ActivateUser, name="activateuser"),
    
    # For user identification and validation in Password Reset Request
    path('user/reset_password_validate/<uidb64>/<token>/', views.ResetPasswordValidateUser, name="reset_password_validate"),

    # To access user orders
    path('user/myorders/', views.UserOrders, name="myorders"),
    path('user/orderdetails/<int:order_id>/', views.OrderDetails, name="orderdetails"),
    path('user/editprofile/', views.EditProfile, name="editprofile"),
    path('user/changepasscode/', views.ChangePassword, name="changepassword"),
]