from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group

from sellstats.models import Supplier

from datetime import datetime, timedelta

import json

from .models import Advertisement, Store

from notifications.signals import notify
from notifications.models import Notification

from operating_log.models import OperatingLog

from lfmarket.roles import ADVERTISEMENT_MGMT
from rolepermissions.verifications import has_permission
# Create your views here.

@login_required(login_url='/index/')
def advertisement_mgmt(request):

	if not request.user.has_perm("advertisement_mgmt.advertisement_mgmt"):
		return render(request, 'control_panel/access_violation.html')

	suppliers = [sup.code + ' ' + sup.name for sup in Supplier.objects.all()]

	advertisements = Advertisement.objects.all()
	adv_data = []
	for adv in advertisements:
		print(adv.picture.url)
		adv_data.append({'supplier': adv.supplier.name,
						 'monthly_pay': adv.monthly_pay,
						 'end_date': adv.end_date,
						 'picture': adv.picture.url,
						 'store': adv.store.name,
						 'phone': adv.supplier.phone})

	return render(request, 'advertisement_mgmt/advertisement_mgmt.html', 
				  {'stores': [s.name for s in Store.objects.all()],
				   'suppliers': suppliers,
				   'advertisements': adv_data,})


def add_advertisement(request):

	store_select = request.POST['store_select']
	monthly_pay = request.POST['monthly_pay']
	supplier_select = request.POST['supplier_select']
	start_date = request.POST['start_date']
	end_date = request.POST['end_date']
	description = request.POST['adv_description']
	#user = request.POST['user']
	image =request.FILES['adv_image']

	# unique code generation

	# try to create or update Advertisement object
	import time
	sup_code = supplier_select.split(' ')[0]
	supplier = Supplier.objects.get(code=sup_code)
	adv, created = Advertisement.objects.get_or_create(code=str(time.time()))
	if created:
		adv.store = Store.objects.get(name=store_select)
		adv.supplier = supplier
		adv.monthly_pay = int(monthly_pay)
		adv.description = description
		adv.create_date = datetime.now()
		adv.start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
		adv.end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
		adv.picture = image
		adv.save()
		# log to system
		log = OperatingLog(date=adv.create_date, 
						   operator=request.user,
						   on_module='advertisement_mgmt',
						   description='新增了一筆'+store_select+'廣告紀錄')
		log.save()

	return redirect(advertisement_mgmt)

@csrf_exempt
def check_due_advertisement(request):

	now = datetime.now()
	precaution = now + timedelta(days=14)

	ads = Advertisement.objects.filter(end_date__gte=now)\
						 	   .filter(end_date__lte=precaution)
	if len(ads) > 0:
		for user in User.objects.all():
			if user.has_perm("advertisement_mgmt.advertisement_mgmt") and \
				Notification.objects.filter(unread=1, 
									   		recipient=user,
									   		verb='有即將到期的廣告').count() == 0:
					notify.send(sender=user, 
								recipient=user, 
								verb='有即將到期的廣告',
								href='/user/advertisement_mgmt.html')

	return HttpResponse(json.dumps({}), content_type="application/json")

