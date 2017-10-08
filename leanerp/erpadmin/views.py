from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url="/")
def index(request):

	current_user = request.user

	return render(request, 'erpadmin/index.html', {'user': current_user})