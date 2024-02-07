
from django.contrib import admin
from django.urls import path
from  worldbank.views import (home,)
from account.views import (login, register,logout,profile,card,under_review)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),

    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('card/', card, name='card'),
    path('profile/', profile, name='profile'),
    path('review/', under_review, name='under_review'),

]
