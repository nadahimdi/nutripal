from django.urls import path
from . import views
urlpatterns = [
    path('',views.yourbasket, name='yourbasket'),
    path('add/',views.basketadd, name='basketadd'),
    path('delete/',views.basket_delete, name='basketdelete'),
     path('update/',views.basket_update, name='basketupdate')
]