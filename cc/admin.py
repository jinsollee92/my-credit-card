from django.contrib import admin
from .models import Transaction, Customer, Merchant

# Register your models here.

admin.site.register(Transaction)
admin.site.register(Customer)
admin.site.register(Merchant)