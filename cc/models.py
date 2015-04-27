from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator

class Transaction(models.Model):
	card_number = models.CharField(validators=[RegexValidator(regex='^.{16}$', message='Must be 16 digits', code='nomatch')], max_length=16)
	customer = models.ForeignKey('Customer', null=True)
	merchant_id = models.ForeignKey('Merchant')
	transaction_id = models.AutoField(primary_key=True)
	amount = models.FloatField()
	date = models.DateTimeField(default=timezone.now)
	safe = models.BooleanField(default=True)

	def __str__(self):
		return str(self.transaction_id)

class Customer(models.Model):
	user = models.OneToOneField(User)
	card_number = models.CharField(validators=[RegexValidator(regex='^.{16}$', message='Must be 16 digits', code='nomatch')], max_length=16, primary_key=True)
	zip = models.CharField(max_length=5)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=2)
	country = models.CharField(max_length=50)

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
		return self.user.first_name

	def __unicode__(self):
		return self.user.username


