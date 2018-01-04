from django.db import models
from datetime import datetime

# Create your models here.

class Goods(models.Model):

	barcode = models.TextField(blank=True, primary_key=True)
	name = models.TextField(blank=True)
	internal_code = models.TextField(blank=True)
	last_update_date = models.DateTimeField(default=datetime(1900, 1, 1))

	# overwrite save to force last_update_date updated when save()
	def save(self, *args, **kwargs):
		self.last_update_date = datetime.now()
		super(Goods, self).save(*args, **kwargs)

	def __str__(self):
		return ' '.join([str(self.internal_code), 
						 str(self.name),
						 str(self.barcode)])

class Supplier(models.Model):

	internal_code = models.TextField(blank=True, primary_key=True)
	name = models.TextField(blank=True)
	phone = models.TextField(blank=True)

	def __str__(self):
		return ' '.join([str(self.internal_code), 
						 str(self.name),
						 str(self.phone)])

