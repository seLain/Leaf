from django.db import models
from django.utils import timezone
from erpadmin.models import Supplier
from .settings import ADV_IMAGE_BASE, DEFAULT_IMAGE

# Create your models here.

class Store(models.Model):

	ss8_id = models.TextField(default='', null=True)
	ss12_id = models.TextField(default='', null=True)
	name = models.TextField(primary_key=True)


class Advertisement(models.Model):

	code = models.TextField(blank=True, primary_key=True)
	store = models.ForeignKey(Store, blank=True, null=True)
	supplier = models.ForeignKey(Supplier, blank=True, null=True)
	monthly_pay = models.IntegerField(default=0)
	description = models.TextField(blank=True)
	create_date = models.DateTimeField(default=timezone.now)
	start_date = models.DateTimeField(default=timezone.now)
	end_date = models.DateTimeField(default=timezone.now)
	picture = models.ImageField(upload_to = ADV_IMAGE_BASE, 
								default = DEFAULT_IMAGE,
								blank=True,
								null=True)

	class Meta:
		permissions = (
			("advertisement_mgmt", "可以新增廣告及查看當前廣告"),
		)

