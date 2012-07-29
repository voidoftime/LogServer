import sys
sys.path.append('..')
#~ from utils.dataUtils import *

from ORM.models import logs
from mongoengine import *
connect('logdb')
#~ logs.objects().delete()
#~ ls=logs.objects(data='myNewMsg')
ls=logs.objects.order_by('+time')
for l in ls:
	print l.deviceId,l.formattedTime
