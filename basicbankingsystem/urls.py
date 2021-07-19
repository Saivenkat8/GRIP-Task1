from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('customers', views.customers, name='customers'),
    path('transaction', views.transaction, name='transaction'),
]
