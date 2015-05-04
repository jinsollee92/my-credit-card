from django.contrib import admin
from .models import Transaction, Customer, Merchant, Block

# Register your models here.

admin.site.register(Transaction)
admin.site.register(Customer)
admin.site.register(Merchant)
admin.site.register(Block)