from django.utils import simplejson
from dajaxice.core import dajaxice_functions
import time

from ORM.models import logs

def example1(request,lastTime):
    """ First simple example """
    #~ return simplejson.dumps({'message': 'hello world'})
    print 'lastTime',lastTime
    data=logs.objects(time__gt=lastTime).order_by('-time')#[:10]
    #~ data=logs.objects.order_by('-time')#[:10]
    res=[]
    maxTime=time.time()
    for item in data:
		#~ if not maxTime:
			#~ maxTime=item.time
		print item.time,lastTime,item.time>lastTime
		res+=[[item.formattedTime,item.deviceId,item.formattedData]]
    print 'maxTime',maxTime
    return simplejson.dumps({'message': res,'lastTime':maxTime})

dajaxice_functions.register(example1)


def example2(request):
    """ Second simple example """
    return simplejson.dumps({'numbers': [1, 2, 3]})

dajaxice_functions.register(example2)


def example3(request, data, name):
    result = sum(map(int, data))
    return simplejson.dumps({'result': result})

dajaxice_functions.register(example3)


def error_example(request):
    raise Exception("Some Exception")

dajaxice_functions.register(error_example)
