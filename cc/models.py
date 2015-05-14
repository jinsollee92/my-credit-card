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
		if mean==0 and stdev==0:
			self.safe_size = True
			return True
		elif self.amount > (mean+stdev):
			self.safe_size = False
			return False
		else:
			self.safe_size = True
			return True

	def check_subscription(self):
		transactions = Transaction.objects.filter(card_number=self.card_number, amount=self.amount)
		if transactions.count() >= 3:
			for t in transactions:
				t.subscription = True
			self.subscription = True
			return True
		else:
			self.subscription = False
			return False

	def check_suspicious(self):
		if self.amount < 1:
			self.suspicious = True
			return True
		else:
			self.suspicious = False
			return False

	def check_blocked(self):
		b = Block.objects.filter(customer=self.customer, merchant=self.merchant_id).count()
		if b > 0:
			self.blocked_merchant = True
			return True
		else:
			self.blocked_merchant = False
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

	def calc_mean(self, amount):
		transactions = Transaction.objects.filter(customer=self).count()
		if transactions > 1:
			m = ((self.mean*transactions)+amount) / (transactions+1)
			self.mean = m
			return m
		else:
			self.mean = amount
			return amount

	def calc_variance(self, amount):
		transactions = Transaction.objects.filter(customer=self).count()
		if transactions > 1:
			v = self.variance + (amount**2)
			self.variance = v
			return v
		else:
			self.variance = amount**2
			return amount**2

	def calc_stdev(self):
		self.stdev = self.variance**(1/2.0)
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
	transactions = models.IntegerField(default=0)

	def count(self):
		t = Transaction.object.filter(customer=self.customer, merchant=self.merchant).count()
		self.transactions = t

	def __str__(self):
		return self.customer.user.get_full_name()+' has blocked '+self.merchant.__str__()
