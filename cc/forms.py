from django import forms
from .models import Transaction, User, Merchant

class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ('card_number', 'amount',)