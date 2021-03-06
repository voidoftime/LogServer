import traceback

from dataUtils import *

LogProtocolCmds={
	'Ack':0x01,
	'Nack':0x02,
	'Echo':0x03,
	'SendText':0x04,
	'SendFile':0x05,
	'QueryData':0x06,
}
#~ LogProtocolCmds

#~ class 


class LogProtocolException(Exception):
       def __init__(self, value):
           self.value = value
           
       def __str__(self):
           return repr(self.value)

class LogProtocol:
	def __init__(self,deviceId=''):
		self.deviceId=deviceId
		self.cmd=None
		self.packetData=None

	def preparePacket(self,cmd,data=''):
		#~ packer=RecordPacker()
		#~ packer.setVarchar2()
		res=chr(len(utf8ToCp866(self.deviceId)))+utf8ToCp866(self.deviceId)+chr(cmd)+intToCU32(len(data))+data
		length=len(res)
		res=intToCU32(length)+res
		res+=intToCU16(crc16(res))
		return res
	
	def validatePacket(self,data):
		try:
			parser=RecordParser(data)
			#~ packetData=parser.getPacketWithCrc()
			packetData=parser.getPacket4WithCrc()
			#~ if packetData==False:
			return True
		except:
			print 'not full or wrong packet',traceback.format_exc()
			return
	
	def parsePacket(self,data):
		try:
			parser=RecordParser(data)
			packetData=parser.getPacket4WithCrc()
			parser=RecordParser(packetData)
			#~ packetBody=parser.getVarchar2()
			#~ packetCrc=parser.getInt16()
			#~ if parser.getRestOfData():
				#~ return Non
			#~ packetLength=parser.getInt16()
			#~ if packetLength==len(data)-4:
			self.deviceId=parser.getVarcharUtf1()
			self.cmd=parser.getInt8()
			#~ self.packetData=parser.getRestOfData()
			self.packetData=parser.getVarbinary4()
				#~ self.packetData=cp866ToUtf(parser.getRestOfData())
				#~ self.packetData=parser.getVarcharUtf1()
				#~ return (deviceId,cmd,packetData)
			return True
			#~ else:
				#~ print 'wrong length'
				#~ return
		except:
			print 'wrong packet',traceback.format_exc()
			return
		
	#~ def sendPacket(
			
	def sendText(self,text):
		packer=RecordPacker()
		packer.setVarcharUtf2(text)
		res=self.preparePacket(LogProtocolCmds['SendText'],packer.getData())
		return res
	
	def sendAck(self):
		res=self.preparePacket(LogProtocolCmds['Ack'])
		return res
		
		
