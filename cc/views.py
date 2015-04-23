from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from .models import Transaction, Customer, Merchant

def home(request):
	return render(request, 'cc/home.html', {})

def user_log_in(request):
	context = RequestContext(request)
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user:
			login(request, user)
			return home(request)
		else:
			return user_log_in(request)
	else:
		return render_to_response('cc/login.html', {}, context)

def user_log_out(request):
	logout(request)
	return HttpResponseRedirect('/')

def transactions(request):
	if request.user.is_authenticated():
		if request.user.groups.filter(name="Customer").exists():
			return customer_transaction_list(request)
		elif request.user.groups.filter(name="Merchant").exists():
			return merchant_transaction_list(request)
	else:
		return user_log_in(request)

def customer_transaction_list(request):
	transactions = Transaction.objects.filter(card_number=Customer.objects.get(user=request.user).card_number)
	return render(request, 'cc/customer_transactions.html', {'transactions': transactions})

def merchant_transaction_list(request):
	return render(request, 'cc/merchant_transactions.html')