from django.shortcuts import render
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from storehouse.models import Goods
import json
from datetime import datetime

from .models import Clerk, Task, ClerkMessage, ClerkMessageForm

User = get_user_model()

# Create your views here.
@api_view(['POST'])
def verify_app_login(request):

	# [seLain][note]
	# using json.loads(request.body) here will cause bytes-loading exception
	# it has to be decoded by request.read().decode('utf-8') first
	login_data = json.loads(request.read().decode('utf-8'))
	username = login_data['username']
	password = login_data['password']

	verification_data = {'verified': 'false',
	                     'message': ''}

	# CODE_SECTION
	#   verify the username and password
	try:
		user = User.objects.get(username=username)
		#   MOCK_CODE
		if user.check_password(password):
			check_clerk_model_exist(user)
			verification_data['verified'] = 'true'
		else:
			verification_data['verified'] = 'false'
		#   CODE_MOCK
	except User.DoesNotExist:
		verification_data = {'verified': 'false',
		                     'message': 'User.DoesNotExist'}
	# SECTION_CODE

	return HttpResponse(json.dumps(verification_data), content_type="application/json")

def check_clerk_model_exist(user):

	clerk, created = Clerk.objects.get_or_create(real_user=user)
	if created:
		try:
			clerk.store = Store.objects.all()[0]
			clerk.save()
		except IndexError:
			print("No store available when check_clerk_model_exist(user)")

@login_required(login_url='/index/')
def send_clerk_message(request):

	# deal with submitted message
	if 'content' in request.POST:
		ClerkMessage(content=request.POST['content']).save()

	# deal with message delete
	if 'del_id' in request.POST:
		try:
			ClerkMessage.objects.get(id=request.POST['del_id']).delete()
		except ClerkMessage.DoesNotExist:
			print("ClerkMessage.DoesNotExist")

	# prepare return message
	message_form = ClerkMessageForm
	messages = ClerkMessage.objects.all().order_by('-date')

	return render(request, 'inventorycheck/send_clerk_message.html', {
		          'message_form': message_form,
		          'messages': messages})

@api_view(['POST'])
def update_clerk_messages(request):

	messages = ClerkMessage.objects.all().order_by('-date')

	msg_data = {'list': []}
	for msg in messages:
		msg_data['list'].append({
			'content': msg.content,
			})

	return HttpResponse(json.dumps(msg_data), content_type="application/json")

def remove_tasks(clerk):

	# remove all tasks of this user
	Task.objects.filter(owner=clerk, status='ToDo').delete()
	Task.objects.filter(owner=clerk, status='InProgress').delete()

def goods_for_check_strategy():

	target_goods = []

	target_goods = Goods.objects.order_by('?')[:5]

	return target_goods


@api_view(['POST'])
def regenerate_tasks(request):

	data = json.loads(request.read().decode('utf-8'))
	username = data['username']

	# prepare model access
	user = User.objects.get(username=username)
	clerk = Clerk.objects.get(real_user=user)

	# remove tasks
	remove_tasks(clerk)

	# select goods by strategy
	target_goods = goods_for_check_strategy()

	# generate inventory check tasks of this user
	for goods in target_goods:
		task = Task(number=goods.barcode,
					name='盤點 '+goods.name,
					mission_type='SpecificInventoryCheck',
					owner=clerk,
					goods=goods,
					store=clerk.store)
		task.save()

	# return ok
	regen_result = {'status':'ok'}
	return HttpResponse(json.dumps(regen_result), content_type="application/json")

@api_view(['POST'])
def update_task(request):

	# [seLain][note] get username from request
	# using json.loads(request.body) here will cause bytes-loading exception
	# it has to be decoded by request.read().decode('utf-8') first
	login_data = json.loads(request.read().decode('utf-8'))
	username = login_data['username']

	# retrieve task by username
	user = User.objects.get(username=username)
	clerk = Clerk.objects.get(real_user=user)
	clerk_tasks = Task.objects.filter(
		             Q(owner=clerk, status='ToDo')|Q(owner=clerk, status='InProgress'))

	# prepare tasks to return
	task_data = {'list': []}
	for task in clerk_tasks.all():
		task_data['list'].append({
			'id': task.number,
			'name': task.name,
			'product': task.goods.name,
			'product_id': task.goods.barcode,
			'product_unit': 'None',
			'on_stock_count': str(task.on_stock_count),
			'storage_count': str(task.storage_count),
			'date':task.date.strftime("%Y-%m-%d"),
			'status': task.status,
			'store': task.store.name,
			})

	return HttpResponse(json.dumps(task_data), content_type="application/json")

@api_view(['POST'])
def report_inventory(request):

	check_data = json.loads(request.read().decode('utf-8'))
	task_id = check_data['task_id']
	on_stock_count = check_data['on_stock_count']
	storage_count = check_data['storage_count']
	date = check_data['date']

	# CODE_SECTION
	#   do inventory check data preservation
	task = Task.objects.get(number=task_id)
	task.on_stock_count = on_stock_count
	task.storage_count = storage_count
	date = date.split('-')
	task.date = datetime(int(date[0]), int(date[1]), int(date[2]))
	task.status = 'Done'
	task.save()

	#   prepare return status
	report_result = {'status':'ok'}
	# SECTION_CODE

	return HttpResponse(json.dumps(report_result), content_type="application/json")

@api_view(['POST'])
def inprogress_inventory(request):

	check_data = json.loads(request.read().decode('utf-8'))
	task_id = check_data['task_id']
	on_stock_count = check_data['on_stock_count']
	storage_count = check_data['storage_count']
	date = check_data['date']

	# CODE_SECTION
	#   do inventory check data preservation
	task = Task.objects.get(number=task_id)
	if on_stock_count != '':
		task.on_stock_count = on_stock_count
	if storage_count != '':
		task.storage_count = storage_count
	if date != '':
		date = date.split('-')
		task.date = datetime(int(date[0]), int(date[1]), int(date[2]))
	task.status = 'InProgress'
	task.save()

	#   prepare return status
	report_result = {'status':'ok'}
	# SECTION_CODE

	return HttpResponse(json.dumps(report_result), content_type="application/json")

@api_view(['POST'])
def update_done_task(request):

	# [seLain][note] get username from request
	# using json.loads(request.body) here will cause bytes-loading exception
	# it has to be decoded by request.read().decode('utf-8') first
	login_data = json.loads(request.read().decode('utf-8'))
	username = login_data['username']

	# CODE_SECTION

	# retrieve task by username
	user = User.objects.get(username=username)
	clerk = Clerk.objects.get(real_user=user)
	clerk_tasks = Task.objects.filter(owner=clerk, status='Done')

	# prepare tasks to return
	task_data = {'list': []}
	for task in clerk_tasks.all():
		task_data['list'].append({
			'id': task.number,
			'name': task.name,
			'product': task.goods.name,
			'product_id': task.goods.barcode,
			'product_unit': 'None',
			'on_stock_count': str(task.on_stock_count),
			'storage_count': str(task.storage_count),
			'date':task.date.strftime("%Y-%m-%d"),
			'store': task.store.name,
			})

	# SECTION_CODE

	return HttpResponse(json.dumps(task_data), content_type="application/json")
