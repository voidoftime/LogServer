#coding=utf8

from twisted.internet import reactor, protocol
from twisted.protocols import basic

import sys
sys.path.append('..')
from utils.dataUtils import *
from utils.logProtocol import *

from ORM.models import logs
from ORM.models import Device
from mongoengine import *
from mongoengine.queryset import DoesNotExist


connect('logdb')



class EchoProtocol(basic.LineReceiver):
	def lineReceived(self, line):
		if line == 'quit':
			self.sendLine("Goodbye.")
			self.transport.loseConnection( )
		else:
			self.sendLine("You said: " + line)

class DataProtocol(protocol.Protocol):
	def __init__(self):
		self.logProtocol=LogProtocol()
		self.fulldata=''
	#	 self.output = None
	#	 self.normalizeNewlines = False

	#~ def preparePacket(self):
		#~ pass

	def dataReceived(self, data):
#		print 'recv',data
		self.fulldata+=data
		#~ if self.logProtocol.parsePacket(self.fulldata):
		try:
			if self.logProtocol.validatePacket(self.fulldata):
				#~ print 'parse ok'
				self.logProtocol.parsePacket(self.fulldata)
				if self.logProtocol.cmd==LogProtocolCmds['SendText']:
					parser=RecordParser(self.logProtocol.packetData)
					text=parser.getVarcharUtf2()
					print 'recv text',text
					#~ l=logs(deviceId=self.logProtocol.deviceId.decode('utf8','ignore').encode('ascii','ignore'),data=text.decode('utf8','ignore').encode('ascii','ignore'),time=int(time.time()))
					#~ l=logs(deviceId=unicode(self.logProtocol.deviceId),data=unicode(text),time=int(time.time()))
					l=logs(deviceId=self.logProtocol.deviceId.decode('utf8','ignore'),data=text.decode('utf8','ignore'),time=int(time.time()))
					l.save()
					currentTime=int(time.time())
					try:
						#~ d=Device.objects.get(deviceId=self.logProtocol.deviceId)
						#~ d=Device.objects.get(deviceId=unicode(self.logProtocol.deviceId))
						d=Device.objects.get(deviceId=self.logProtocol.deviceId.decode('utf8','ignore'))
						#~ d.update(lastActivityTime=currentTime)
						d.lastActivityTime=currentTime
						d.ipAddress=self.transport.client[0]
						d.save()
					except DoesNotExist:
						#~ d=Device(deviceId=self.logProtocol.deviceId,ipAddress=self.transport.client[0],lastActivityTime=currentTime)
						#~ d=Device(deviceId=unicode(self.logProtocol.deviceId),ipAddress=self.transport.client[0],lastActivityTime=currentTime)
						print 'add new deviceId',self.logProtocol.deviceId
						d=Device(deviceId=self.logProtocol.deviceId.decode('utf8','ignore'),ipAddress=self.transport.client[0],lastActivityTime=currentTime)
						d.save()
						
					
					res=self.logProtocol.sendAck()
					self.transport.write(res)
				self.fulldata=''
				self.transport.loseConnection( )
		except:
			print traceback.format_exc()
			pass

class EchoServerFactory(protocol.ServerFactory):
	# protocol  = EchoProtocol
	protocol  = DataProtocol

	def buildProtocol(self, addr):
		print 'Connected',addr
		#~ l=logs(deviceId='server',data='client connected from {}'.format(addr),time=int(time.time()))
		#~ l.save()
		#~ if addr.host == "127.0.0.1":
		if 1:
			return protocol.ServerFactory.buildProtocol(self, addr)
		return None

if __name__ == "__main__":
	port = 5001
	reactor.listenTCP(port, EchoServerFactory( ))
	print 'start serve'
	reactor.run( )
