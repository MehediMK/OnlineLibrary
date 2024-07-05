from django.urls import path
from account.views import (user_login,logout_view,signup_view,changepass)


urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('changepass/', changepass, name='changepass'),
] 