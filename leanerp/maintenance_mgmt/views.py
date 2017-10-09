from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Maintenance
from advertisement_mgmt.models import Store
from django.contrib.auth.models import User
from datetime import datetime, timedelta

from notifications.signals import notify
from notifications.models import Notification

import json

from lfmarket.roles import STORE_MAINTENANCE_MGMT
from rolepermissions.verifications import has_permission
from helpdesk.models import Ticket, Queue
from operating_log.models import OperatingLog
# Create your views here.

@login_required(login_url='/index/')
def store_maintenance_mgmt(request):
	
	if not request.user.has_perm("maintenance_mgmt.maintenance_mgmt"):
		return render(request, 'control_panel/access_violation.html')

	maintainments = Maintenance.objects.all()
	maintain_data = []
	for maintain in maintainments:
		maintain_data.append({'code': maintain.code,
							  'description': maintain.description,
							  'creator': maintain.creator.last_name + maintain.creator.first_name,
						 	  'discover_date': maintain.discover_date,
							  'create_date': maintain.create_date,
							  'status': maintain.get_status(),
						 	  'picture': maintain.picture.url,
						 	  'store': maintain.store.name,
						 	  'validated': maintain.is_validated()})

	return render(request, 'control_panel/store_maintenance_mgmt.html', 
				  {'stores': [s.name for s in Store.objects.all()],
				   'maintainments': maintain_data,})


def add_store_maintenance(request):

	store_select = request.POST['store_select']
	discover_date = request.POST['discover_date']
	description = request.POST['maintain_description']
	image =request.FILES['maintain_image']

	# try to create or update Advertisement object
	import time
	maintain, created = Maintenance.objects.get_or_create(code=str(time.time()))
	if created:
		# create corresponding ticket
		queue = Queue.objects.get(slug='storejob')
		ticket = Ticket(title= store_select + "維修申請",
	                    submitter_email="",
	                    created=datetime.now(),
	                    status=Ticket.OPEN_STATUS,
	                    queue=queue,
	                    description=description,
	                    priority=3)
		ticket.save()
		# create maintain item itself
		maintain.store = Store.objects.get(name=store_select)
		maintain.creator = request.user
		maintain.description = description
		maintain.create_date = datetime.now()
		maintain.discover_date = datetime.strptime(discover_date, "%Y-%m-%d").date()
		maintain.picture = image
		maintain.ticket = ticket
		maintain.save()
		# make notification
		notify_new_maintenance()
		# log to system
		log = OperatingLog(date=maintain.create_date, 
						   operator=request.user,
						   on_module='maintenance_mgmt',
						   description='新增了一筆'+store_select+'維修申請')
		log.save()

	return redirect(store_maintenance_mgmt)

def notify_new_maintenance():

	for user in User.objects.all():
		if user.has_perm("maintenance_mgmt.maintenance_mgmt") and \
			Notification.objects.filter(unread=1, 
								   		recipient=user,
								   		verb='有新的維修申請').count() == 0:
				print("create new")
				notify.send(sender=user, 
							recipient=user, 
							verb='有新的維修申請',
							href='/user/store_maintenance_mgmt.html')

@csrf_exempt
def check_recent_maintenance(request):

	now = datetime.now()
	precaution = now - timedelta(days=3)

	maintains = Maintenance.objects.filter(create_date__gte=precaution)
	if len(maintains) > 0:
		notify_new_maintenance()

	return HttpResponse(json.dumps({}), content_type="application/json")


def validate_store_maintenance(request):

	if not request.user.has_perm("maintenance_mgmt.allow_maintenance_validate"):
		return render(request, 'control_panel/access_violation.html')

	if 'maintain_code' in request.POST:
		try:
			maintain_code = request.POST['maintain_code']
			validated = request.POST['validated'] == 'true'
			mt = Maintenance.objects.get(code=maintain_code)
			mt.set_validated(validated, request.user)
			mt.save()
			# log to system
			log = OperatingLog(date=mt.create_date, 
							   operator=request.user,
							   on_module='maintenance_mgmt',
							   description=':'.join(['審核了一筆維修申請', mt.store.name, mt.description]))
			log.save()
		except Maintenance.DoesNotExist:
			print("Maintenance.DoesNotExist")

	return HttpResponse(json.dumps({}), content_type="application/json")

