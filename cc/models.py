from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator
from django.db.models import Avg, StdDev, Count

class Transaction(models.Model):
	card_number = models.CharField(validators=[RegexValidator(regex='^.{16}$', message='Must be 16 digits', code='nomatch')], max_length=16)
	customer = models.ForeignKey('Customer', null=True)
	merchant_id = models.ForeignKey('Merchant')
	transaction_id = models.AutoField(primary_key=True)
	amount = models.FloatField()
	date = models.DateTimeField(default=timezone.now)
	safe_size = models.BooleanField(default=True)
	subscription = models.BooleanField(default=False)
	suspicious = models.BooleanField(default=False)
	blocked_merchant = models.BooleanField(default=False)

	def check_size(self):
		mean = self.customer.mean
		stdev = self.customer.stdev
		if self.amount > (mean+stdev):
			return False
		else:
			return True

	def check_subscription(self):
		transactions = Transaction.objects.filter(card_number=self.card_number, amount=self.amount)
		if transactions.count() >= 3:
			return True
		else:
			return False

	def check_suspicious(self):
		if self.amount < 1:
			return True
		else:
			return False

	def masked_card_number(self):
		return '************'+self.card_number[12:16]

	def __str__(self):
		return str(self.transaction_id)

class Customer(models.Model):
	user = models.OneToOneField(User)
	card_number = models.CharField(validators=[RegexValidator(regex='^.{16}$', message='Must be 16 digits', code='nomatch')], max_length=16, primary_key=True)
	zip = models.CharField(max_length=5)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=2)
	country = models.CharField(max_length=50)
	mean = models.FloatField(default=0)
	variance = models.FloatField(default=0)
	stdev = models.FloatField(default=0)

	def init_stats(self):
		transactions = Transaction.objects.filter(customer=self)
		count = transactions.count()
		mean = 0
		variance = 0
		for t in transactions:
			mean += t.amount
		mean = mean / float(count)
		self.mean = mean
		for t in transactions:
			variance += (t.amount-mean)**2
		self.variance = variance
		self.stdev = variance**(1/2.0)

	def calc_mean(self, new_transaction):
		transactions = Transaction.objects.filter(customer=self).count()
		if transactions > 1:
			return ((self.mean*transactions)+new_transaction.amount) / (transactions+1)
		else:
			return new_transaction.amount

	def calc_variance(self, new_transaction):
		transactions = Transaction.objects.filter(customer=self).count()
		if transactions > 1:
			return self.variance + (new_transaction.amount**2)
		else:
			return new_transaction.amount**2

	def calc_stdev(self):
		return self.variance**(1/2.0)		

	def __str__(self):
		return self.user.first_name+" "+self.user.last_name

	def __unicode__(self):
		return self.card_number

class Merchant(models.Model):
	user = models.OneToOneField(User)
	merchant_id = models.AutoField(primary_key=True)
	zip = models.CharField(max_length=5)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=2)
	country = models.CharField(max_length=50)

	def __str__(self):
		return self.user.first_name+', '+self.city+', '+self.state+' '+self.zip

class Block(models.Model):
	customer = models.ForeignKey('Customer')
	merchant = models.ForeignKey('Merchant')

	def __str__(self):
		return self.customer.user.get_full_name()+' has blocked '+self.merchant.__str__()
