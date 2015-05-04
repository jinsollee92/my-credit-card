from django import forms
from django.contrib.auth.models import User
from .models import Transaction, Customer, Merchant, Block

class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ('card_number', 'amount',)

class CustomerUserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email',)

class CustomerForm(forms.ModelForm):

	class Meta:
		model = Customer
		fields = ('card_number', 'city', 'state', 'zip', 'country',)

class MerchantUserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'first_name', 'email',)

class MerchantForm(forms.ModelForm):

	class Meta:
		model = Merchant
		fields = ('city', 'state', 'zip', 'country',)

class BlockForm(forms.ModelForm):

	class Meta:
		model = Block
		fields = ('merchant',)