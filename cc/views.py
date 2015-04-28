from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.utils import timezone
from .models import Transaction, Customer, Merchant
from .forms import TransactionForm, CustomerUserForm, CustomerForm, MerchantUserForm, MerchantForm

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
		print('username & password received')
		user = authenticate(username=username, password=password)
		if user is not None:
			print('authentication successful')
			login(request, user)
		else:
			print('authentication failed')
		return home(request)
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
	customer = Customer.objects.get(user=request.user)
	card_number = customer.card_number
	transactions = Transaction.objects.filter(card_number=card_number, safe=True)
	return render(request, 'cc/customer_transactions.html', {'transactions': transactions})

def merchant_transaction_list(request):
	merchant = Merchant.objects.get(user=request.user)
	transactions = Transaction.objects.filter(merchant_id=merchant)
	return render(request, 'cc/merchant_transactions.html', {'transactions': transactions})

def submit_transaction(request):
	if request.method == 'POST' :
		form = TransactionForm(request.POST)
		if form.is_valid():
			t = form.save(commit=False)
			n = form.cleaned_data['card_number']
			print(n)
			t.safe = True
			t.merchant_id = Merchant.objects.get(user=request.user)
			print('merchant found')
			customer = Customer.objects.get(card_number=n)
			print('customer query')
			if customer is not None:
				t.customer = Customer.objects.get(card_number=n)
			else:
				t.customer = null
			t.date = timezone.now()
			t.save()
		return HttpResponseRedirect('/transactions')
	else:
		form = TransactionForm()
	return render(request, 'cc/submit_transaction.html', {'form': form})

def register(request):
	return render(request, 'cc/register.html')

def customer_register(request):
	context = RequestContext(request)
	if request.method == 'POST':
		user_form = CustomerUserForm(request.POST)
		customer_form = CustomerForm(request.POST)

		if user_form.is_valid():
			if customer_form.is_valid():
				user = user_form.save(commit=False)
				user.set_password(user_form.cleaned_data['password'])
				user.save()

				customer = customer_form.save(commit=False)
				customer.user = user
				customer.save()
				group = Group.objects.get(name='Customer')
				group.user_set.add(user)
				return HttpResponseRedirect('/login')
	else:
		user_form = CustomerUserForm()
		customer_form = CustomerForm()
	return render_to_response('cc/customer_register.html', {'user_form': user_form, 'customer_form': customer_form}, context)

def merchant_register(request):
	context = RequestContext(request)
	if request.method == 'POST':
		user_form = MerchantUserForm(request.POST)
		merchant_form = MerchantForm(request.POST)

		if user_form.is_valid():
			print('user form valid')
			if merchant_form.is_valid():
				user = user_form.save(commit=False)
				user.set_password(user_form.cleaned_data['password'])
				user.save()

				merchant = merchant_form.save(commit=False)
				merchant.user = user
				merchant.save()
				group = Group.objects.get(name='Merchant')
				group.user_set.add(user)
				return HttpResponseRedirect('/login')
	else:
		user_form = MerchantUserForm()
		merchant_form = MerchantForm()
	return render_to_response('cc/merchant_register.html', {'user_form': user_form, 'merchant_form': merchant_form}, context)
