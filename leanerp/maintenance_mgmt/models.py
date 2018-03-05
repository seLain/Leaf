from django.db import models
from datetime import datetime
from django.utils import timezone

from storehouse.models import Store
from .settings import ADV_IMAGE_BASE, DEFAULT_IMAGE

from django.contrib.auth.models import User
from helpdesk.models import Ticket, FollowUp

# Create your models here.

class Maintenance(models.Model):

	code = models.TextField(blank=True, primary_key=True)
	store = models.ForeignKey(Store, blank=True, null=True)
	creator = models.ForeignKey(User, blank=True, null=True)
	discover_date = models.DateTimeField(default=timezone.now)
	create_date = models.DateTimeField(default=timezone.now)
	description = models.TextField(blank=True)
	picture = models.ImageField(upload_to = ADV_IMAGE_BASE,
								default = DEFAULT_IMAGE,
								blank=True,
								null=True)
	ticket = models.ForeignKey(Ticket, blank=True, null=True)
	# marked as processed or not yet
	# - the (blank=True, null=True) allows processed_date to be empty
	# - if the processed_date is empty, this bill is not processed yet 
	validate_date = models.DateTimeField(blank=True, null=True)

	class Meta:
		permissions = (
			("maintenance_mgmt", "可以新增維修及查看當前維修"),
			("allow_maintenance_validate", "可以審核維修申請單")
		)

	def get_status(self):
		if self.ticket:
			return self.ticket.get_status
		else:
			return "Unknown"

	def is_validated(self):
		if self.validate_date:
			return True
		else:
			return False

	def set_validated(self, validated, user):
		if validated == True:
			self.validate_date = datetime.now()
			# append follow up to ticket
			follow = FollowUp(ticket=self.ticket,
							  date=self.validate_date,
							  title="已進行審核",
							  user=user)
			follow.save()
		elif validated == False:
			self.validate_date = None
