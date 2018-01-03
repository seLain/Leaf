from django.shortcuts import render
from rest_framework.decorators import api_view


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

