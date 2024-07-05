from django.urls import path
from .views import (
    Index, Shop, user_profile, book_details, my_pack, book_take, 
    Cart,IncDec, Checkout, OrderView, Add_to_cart, ProductSearch,
    EditUserInfo
)


urlpatterns = [
    path('',Index.as_view(),name='home'),
    path('shop/',Shop.as_view(),name='shop'),
    path('ProductSearch/',ProductSearch.as_view(),name='ProductSearch'),
    path('Add_to_cart/',Add_to_cart.as_view(),name='addtocart'),
    path('details/<int:id>/',book_details,name='details'),
    path('profile/',user_profile,name='profile'),
    path('create/',my_pack,name='mypack'),
    path('takebook/<int:id>/',book_take,name='takebook'), 
    path('cart/',Cart.as_view(),name='cart'), 
    path('IncDec/',IncDec.as_view(),name='incdec'), 
    path('Checkout/',Checkout.as_view(),name='checkout'), 
    path('OrderView/',OrderView.as_view(),name='orderView'), 
    path('EditUserInfo/',EditUserInfo,name='edituserinfo'),
] 