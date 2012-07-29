from twisted.internet import stdio, reactor, protocol
from twisted.protocols import basic

import sys
sys.path.append('..')
from utils.dataUtils import *
from utils.logProtocol import *


class DataForwardingProtocol(protocol.Protocol):

	def dataReceived(self, data):
		print 'recv',data

class StdioProxyProtocol(DataForwardingProtocol):
	def connectionMade(self):
		print "Connected to server.  Press ctrl-C to close connection."
		logProtocol=LogProtocol(deviceId=sys.argv[1])
		#~ logProtocol.deviceId='test client'
		#~ res=logProtocol.preparePacket(1,utf8ToCp866(sys.argv[3]))
		res=logProtocol.sendText(sys.argv[2])
		self.transport.write(res)

class StdioProxyFactory(protocol.ClientFactory):
	protocol = StdioProxyProtocol

	def clientConnectionLost(self, transport, reason):
		reactor.stop( )

	def clientConnectionFailed(self, transport, reason):
		print reason.getErrorMessage( )
		reactor.stop( )

if __name__ == '__main__':
	import sys

	if not len(sys.argv) == 3:
		print "Usage: %s host port" % __file__
		sys.exit(1)

	#~ reactor.connectTCP(sys.argv[1], int(sys.argv[2]), StdioProxyFactory( ))
	reactor.connectTCP('127.0.0.1', 5001, StdioProxyFactory( ))
	reactor.run( )
