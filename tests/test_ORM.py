#coding=utf8

import sys,time

__author__ = 'void'


sys.path.append('..')
from ORM.models import logs
from ORM.models import Device
from mongoengine import *
from mongoengine.queryset import DoesNotExist

import unittest

class Test(unittest.TestCase):

	def setUp(self):
		self.deviceId='unittest'
		connect('logdb')

	def test_logUtf(self):
		texts=['utf string','русский текст']
		for text in texts:
			self.test_logData(text)
			self.test_addDevice(text)

	def test_logData(self,text='default test string'):
		logs.objects().delete()
		testTime=int(time.time())
		l=logs(deviceId=text.decode('utf8','ignore'),data=text.decode('utf8','ignore'),time=testTime)
		l.save()
		res=logs.objects().get(time=testTime)
		self.assertEqual(res.deviceId.encode('utf8','ignore'),text)
		self.assertEqual(res.data.encode('utf8','ignore'),text)

	def test_addDevice(self,text='default test string'):
		Device.objects().delete()
		testTime=int(time.time())
		l=Device(deviceId=text.decode('utf8','ignore'))
		l.save()
		res=Device.objects().get(deviceId=text)
		self.assertEqual(res.deviceId.encode('utf8','ignore'),text)

if __name__=="__main__":
	unittest.main()
