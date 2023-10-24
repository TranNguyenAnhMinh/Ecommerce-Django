from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',views.home, name ='home'),
    path('register/',views.register, name='register'),
    path('login/',views.loginPage, name='login'),
    path('logout/',views.logoutPage, name='logout'),
    path('search/',views.search, name='search'),
    path('detail/',views.detail, name='detail'),
    path('category/',views.category, name='category'),
    path('cart/',views.cart, name='cart'),	
    path('checkout/',views.checkout, name="checkout"),	
    path('update_item/',views.updateItem, name="update_item"),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('send_order_email/', views.send_order_email, name='send_order_email'),
    path('purchase-history/', views.purchase_history, name='purchase_history'),
    path('thankyou/', views.thankyou, name='thankyou'),
]
