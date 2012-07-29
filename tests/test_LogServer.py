#coding=utf8

import sys,time

__author__ = 'void'


sys.path.append('..')
from LogClient.logClient import LogClient
from ORM.models import logs
from ORM.models import Device
from mongoengine import *
from mongoengine.queryset import DoesNotExist

import unittest

class Test(unittest.TestCase):

	def setUp(self):
		self.deviceId='unittest'
		connect('logdb')

		self.logClient=LogClient(serverAddress='127.0.0.1')

	def test_sendRusText(self):
		texts=['utf string','русский текст']
		for inThread in [True,False]:
			for text in texts:
				self.sendText(text,text,inThread)

	def sendText(self,text='default log message',deviceId='unitTestDevice',inThread=False):
		logs.objects().delete()
		Device.objects().delete()
		self.logClient.deviceId=deviceId
		self.assertTrue(self.logClient.sendText(text))


		lastTime=time.time()
		res=None
		while not res:
			if time.time()-lastTime>2:
				break
			time.sleep(0.01)
			res=Device.objects()

#		print 'res',res

		self.assertEqual(len(res),1)
		self.assertEqual(res[0].deviceId.encode('utf8','ignore'),deviceId)

		res=logs.objects()

#		print 'res',res

		self.assertEqual(len(res),1)
		self.assertEqual(res[0].deviceId.encode('utf8','ignore'),deviceId)
		self.assertEqual(res[0].data.encode('utf8','ignore'),text)

if __name__=="__main__":
	unittest.main()
