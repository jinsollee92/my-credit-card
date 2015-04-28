from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^$', views.home),
	url(r'login/', views.user_log_in),
	url(r'logout/', views.user_log_out),
	url(r'transactions/', views.transactions),
	url(r'submit-new/', views.submit_transaction),
	url(r'customer-register/', views.customer_register),
	url(r'merchant-register/', views.merchant_register),
	url(r'register/', views.register),
]