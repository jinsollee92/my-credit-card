from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.utils import timezone
from .models import Transaction, Customer, Merchant
from .forms import TransactionForm

def home(request):
	groups = []
	if request.user.is_authenticated():
		groups = request.user.groups.filter(name="Merchant")
	return render(request, 'cc/home.html', { 'groups': groups })

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
		is_customer = request.user.groups.filter(name="Customer").exists()
		is_merchant = request.user.groups.filter(name="Merchant").exists()
		if is_customer:
			return customer_transaction_list(request)
		elif is_merchant:
			return merchant_transaction_list(request)
		else:
			return HttpResponseRedirect('/admin')
	else:
		return user_log_in(request)

def customer_transaction_list(request):
	customer = Customer.objects.filter(user=request.user)
	transactions = Transaction.objects.filter(card_number=customer.card_number, safe=True)
	return render(request, 'cc/customer_transactions.html', {'transactions': transactions})

def merchant_transaction_list(request):
	merchant = Merchant.objects.filter(user=request.user)
	transactions = Transaction.objects.filter(merchant_id=merchant)
	return render(request, 'cc/merchant_transactions.html', {'transactions': transactions})

def submit_transaction(request):
	if request.method == 'POST' :
		form = TransactionForm(request.POST)
		if form.is_valid():
			t = form.save(commit=False)
			n = t.card_number
			t.safe = True
			t.merchant_id = Merchant.objects.get(user=request.user)
			t.customer = Customer.objects.get(card_number=n)
			t.date = timezone.now()
			t.save()
		return HttpResponseRedirect('/transactions')
	else:
		form = TransactionForm()
	return render(request, 'cc/submit_transaction.html', {'form': form})

def register(request):
	return HttpResponseRedirect('/login')