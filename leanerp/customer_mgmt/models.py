from django.db import models
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class VIPMember(models.Model):

	member_id = models.TextField(blank=True, primary_key=True)
	name = models.TextField(blank=True)
	create_date = models.DateTimeField(default=datetime(1900, 1, 1))

	def __str__(self):
		# [seLain] change this to self.name if we have current supplier name in the future
		return self.name

class VIPCard(models.Model):

	card_id =models.TextField(blank=True, primary_key=True)
	owner = models.ForeignKey(VIPMember)
	points = models.FloatField(
		default=0,
		validators=[
            MinValueValidator(0)
        ])
	points_last_update_date = models.DateTimeField(default=datetime(1900, 1, 1))