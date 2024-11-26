from django.urls import path
from . import views

urlpatterns=[
    path('',views.project1_login),
    
    path('shop_home',views.shop_home),
    path('logout',views.project1_shop_logout),
    path('addproduct',views.add_product),
    path('edit_product/<pid>', views.add_product),  
    path('delete_product/<pid>',views.delete_product),
    path('view_bookings',views.view_bookings),
    
    path('register',views.register), 
    path('user_home',views.user_home),
    path('product_dtls/<pid>',views.view_product),
    path('add_to_cart/<pid>',views.add_to_cart),
    path('view_cart',views.view_cart),
    path('qty_in/<cid>',views.qty_in),
    path('qty_dec/<cid>',views.qty_dec),
    path('cart_pro_buy/<cid>',views.cart_pro_buy),
    path('booking',views.booking),
    path('pro_buy/<pid>',views.pro_buy),
    
]
  
