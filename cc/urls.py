from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^$', views.home),
	url(r'login/', views.user_log_in),
	url(r'logout/', views.user_log_out),
	url(r'transactions/', views.transactions),
	url(r'^customer/', views.customer_transaction_list),
	url(r'^merchant/', views.merchant_transaction_list),
]