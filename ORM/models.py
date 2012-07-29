# from django.db import models
from mongoengine import *
import datetime,time

AllDevicesId='All devices'

RecentTime=10

def timestampToStr(timestamp):
	res=''
	try:
		res=datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
	except:
		pass
	return res

class Device(Document):
	deviceId =StringField(max_length=200)
	ipAddress = StringField(max_length=200)
	lastActivityTime = IntField()

	def __unicode__(self):
		return 'Device '+self.deviceId
	
	@property
	def isRecent(self):
		return self.lastActivityTime and time.time()-self.lastActivityTime<RecentTime
		
	class Meta:
		ordering = ["deviceId"]

class LogMsg(Document):
	deviceId = StringField(max_length=200)
	data = StringField(max_length=200)
	time =StringField(max_length=200)

class logs(Document):
	deviceId=StringField(max_length=200)
	data=StringField(max_length=65535)
	ipAddress=StringField(max_length=50)
	time=IntField()
	
	#~ def getFormattedTime(self):
	@property
	def formattedTime(self):
		#~ print 'j',timestampToStr(int(self.time))
		return timestampToStr(self.time)
	#~ formattedTime=property(getFormattedTime)
	@property
	def formattedData(self):
		#~ print 'j',timestampToStr(int(self.time))
		return self.data.replace('\n','<br>')
	#~ formattedTime=property(getFormattedTime)
	
	@property
	def isRecent(self):
		return self.time and time.time()-self.time<RecentTime

	def __unicode__(self):
		try:
			#~ return 'from {}: {}'.format(self.deviceId,self.data)
			return 'from {}: {}'.format(self.deviceId,self.data)
		except:
			return 'bad data'

