from django.shortcuts import render
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json

from .models import Clerk, ClerkMessage, ClerkMessageForm

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
		except:
			print("No store available when check_clerk_model_exist(user)")

@login_required(login_url='/index/')
@api_view(['POST'])
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

	return render(request, 'control_panel/send_clerk_message.html', {
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


