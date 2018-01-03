from django.db import models
from datetime import datetime

from advertisement_mgmt.models import Store
from django.contrib.auth.models import User
from storehouse.models import Goods
from helpdesk.models import Ticket
# Create your models here.

class Clerk(models.Model):
	# one-to-one mapping to connect to real user of ERP system
	real_user = models.ForeignKey(User, unique=True)
	store = models.ForeignKey(Store, null=True)  # the beloning store

class Task(models.Model):

	number = models.TextField(blank=True, primary_key=True)
	name = models.TextField(blank=True)
	mission_type = models.TextField(
		choices=(('0','Unknown'),
				 ('1','SpecificInventoryCheck')),
		default='Unknown'
		)
	status = models.TextField(
		choices=(('0','ToDo'),
				 ('1','InProgress'),
				 ('2','Done')),
		default='ToDo'
		)
	redo_count = models.IntegerField(default=0)
	owner = models.ForeignKey(Clerk)
	goods = models.ForeignKey(Goods, null=True) # null=True to avoid non-nullfield exception
	ticket = models.ForeignKey(Ticket, null=True)
	# inventory check data
	on_stock_count = models.FloatField(default=0)
	storage_count = models.FloatField(default=0)
	date = models.DateTimeField(
					default=datetime(1900, 1, 1))
	# belonging store
	store = models.ForeignKey(Store)

	class Meta:
		permissions = (
			("view_clerk_jobs", "permission to check jobs assigned to clerks"),
		)
