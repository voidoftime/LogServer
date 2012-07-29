from django.http import HttpResponse
# from polls.models import Device
# from polls.models import LogMsg
from ORM.models import logs
from ORM.models import Device
from django.template import Context, loader
from django.shortcuts import render_to_response

from forms import FilterForm
from ORM.models import AllDevicesId

import time
# from MongoDb import *
# from pymongo import Connection
# from pymongo.errors import ConnectionFailure

from django.middleware.csrf import get_token

def index(request):
	
	#~ devices_list = logs.objects.distinct('deviceId')
	#~ devices_list = Device.objects.order_by('deviceid')
	get_token(request)
	filterForm=FilterForm()
	#~ print filterForm.as_table()
	
	devices_list = Device.objects.all()
	
	devices_list=list(devices_list)
	#~ devices_list=[Device(deviceId=AllDevicesId,lastActivityTime=max([x.lastActivityTime for x in devices_list if hasattr(x,'lastActivityTime')]))]+devices_list
	
	#~ devices_list.sort()
	latest_poll_list = logs.objects.order_by('+time')
	return render_to_response('polls/logList.html', {
		'latest_poll_list': latest_poll_list,
		'devices_list':devices_list,
		'error_message':'',
		'filterForm':filterForm,
	})

def detail(request, poll_id):
	get_token(request)
	# m=MongoDb()
	# return HttpResponse("You're looking at poll %s." % poll_id)
	# latest_poll_list=m.db.logs.find({})
	# latest_poll_list = LogMsg.objects.all()#.order_by('-deviceId')[:5]
	# l=logs(deviceId='00fe00898989',data='hi at '+str(time.time()))
	# l.save()
	#~ devices_list = logs.objects.values('deviceId')
	
	
	#~ devices_list=devices_list.sort()
	#~ latest_poll_list = logs.objects.all()#.order_by('-deviceId')[:5]
	#~ latest_poll_list = logs.objects(data='myNewMsg')
	#~ devices_list = logs.objects.distinct('deviceId')
	#~ devices_list.sort()
	devices_list = Device.objects.all()

	devices_list=list(devices_list)
	devices_list=[Device(deviceId=AllDevicesId,lastActivityTime=min([x.lastActivityTime for x in devices_list]))]+devices_list

	
	latest_poll_list = logs.objects(deviceId=poll_id).order_by('+time')
	#~ print 'formattedTime',latest_poll_list[-1].formattedTime
	return render_to_response('polls/logList.html', {
		'latest_poll_list': latest_poll_list,
		'devices_list':devices_list,
		'error_message':'',
	})
