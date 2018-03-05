from django.shortcuts import render
from helpdesk.models import Queue, Ticket
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json 

# Create your views here.
def get_queue_progress():

	# prepare working progress data
	# the data is acquired from helpdesk queue and tickets
	progress_data = []
	queues = Queue.objects.all()
	for queue in queues:
		num_all_tickets = Ticket.objects.filter(queue=queue).count()
		num_done_tickets = Ticket.objects.filter(queue=queue)\
										 .filter(status=Ticket.CLOSED_STATUS).count()
		if num_all_tickets == 0:
			rate = 0
		else:
			rate = round(float(num_done_tickets)/num_all_tickets, 4) * 100
		rate = float('%.2f' % rate)
		progress_data.append({'queue': queue.title,
							  'rate': rate})

	return progress_data

@csrf_exempt
def get_queue_progress_api(request):

	progress_data = get_queue_progress()

	return HttpResponse(json.dumps(progress_data), content_type="application/json")
