from django.db import models

class Supplier(models.Model):
	name = models.TextField(blank=True)
	phone = models.TextField(blank=True)

	def __str__(self):
		return self.name