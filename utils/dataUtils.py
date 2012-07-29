#coding=utf8

import time,traceback,datetime

class RecordPacker:
	def __init__(self):
		self.data=''
		self.errors=0
	def setBool(self,value):
		try:
			self.data+=chr(int(bool(value)))
		except:
			self.errors+=1
			self.data+=chr(0)
	def setInt8(self,value):
		try:
			self.data+=chr(value)
		except:
			self.errors+=1
			self.data+=chr(0)
	def setInt16(self,value):
		try:
			self.data+=chr(int(value) & 255)+chr((int(value)>>8) & 255)
		except:
			self.errors+=1
			self.data+=chr(0)*2
		#~ self.data+=intToCU16(value)
	def setInt32(self,value):
		res=''
		try:
			for x in range(4):
				res+=chr((int(value)>>(x*8)) & 255)
			self.data+=res
		except:
			self.errors+=1
			self.data+=chr(0)*4
			#~ raise RuntimeError('fucka')
		#~ self.data+=intToCU32(value)
	def setVarchar1(self,rawValue,maxLength=254):
		try:
			value=str(rawValue)
			if len(value)>maxLength:
				length=maxLength
			else:
				length=len(value)
			self.data+=chr(length)+value[0:length]
		except:
			self.errors+=1
			self.data+=chr(0)
	def setVarchar2(self,rawValue,maxLength=65534):
		try:
			value=str(rawValue)
			if len(value)>maxLength:
				length=maxLength
			else:
				length=len(value)
			self.data+=intToCU16(length)+value[0:length]
		except:
			self.errors+=1
			self.data+=chr(0)+chr(0)
	def setVarcharUtf1(self,value,maxLength=254):
		self.setVarchar1(str(value).decode('utf8','ignore').encode('cp866','ignore'),maxLength)
	def setVarcharUtf2(self,value,maxLength=65534):
		self.setVarchar2(str(value).decode('utf8','ignore').encode('cp866','ignore'),maxLength)
	def setGUID(self,value):
		try:
			if len(value)!=16:
				#~ raise RuntimeError('bad GUID')
				self.data+=chr(0)*16
				self.errors+=1
			else:
				self.data+=value[0:16]
		except:
			self.errors+=1
			self.data+=chr(0)*16
	def getData(self):
		res=self.data
		self.data=''
		return res
	

class RecordParser:
	def __init__(self,data=''):
		self.ofs=0
		self.data=data
	def getBool(self):
		self.ofs+=1
		#~ print ord(self.data[self.ofs-1:self.ofs]),self.ofs-1
		return bool(ord(self.data[self.ofs-1:self.ofs]))
	def getInt8(self):
		self.ofs+=1
		return ord(self.data[self.ofs-1:self.ofs])
	def getInt32(self):
		self.ofs+=4
		return arrayToU32(self.data[self.ofs-4:self.ofs])
	def getInt16(self):
		self.ofs+=2
		return arrayToU16(self.data[self.ofs-2:self.ofs])
	def getGUID(self):
		self.ofs+=16
		#~ print len(self.data[self.ofs-16:self.ofs]),[self.data[self.ofs-16:self.ofs]]
		return self.data[self.ofs-16:self.ofs]
	def getVarchar1(self):
		dataLength=ord(self.data[self.ofs])
		self.ofs+=dataLength+1
		#~ print 'vc',dataLength,self.data[self.ofs-dataLength:self.ofs]
		return self.data[self.ofs-dataLength:self.ofs]
	def getVarchar2(self):
		dataLength=arrayToU16(self.data[self.ofs:self.ofs+2])
		#~ print 'dataLength',dataLength
		self.ofs+=dataLength+2
		return self.data[self.ofs-dataLength:self.ofs]
	def getVarcharUtf1(self):
		dataLength=ord(self.data[self.ofs])
		self.ofs+=dataLength+1
		#~ print 'vc',dataLength,self.data[self.ofs-dataLength:self.ofs]
		return self.data[self.ofs-dataLength:self.ofs].decode('cp866','ignore').encode('utf8','ignore')
	def getVarcharUtf2(self):
		dataLength=arrayToU16(self.data[self.ofs:self.ofs+2])
		self.ofs+=dataLength+2
		return self.data[self.ofs-dataLength:self.ofs].decode('cp866','ignore').encode('utf8','ignore')
	def getVarbinary4(self):
		dataLength=arrayToU32(self.data[self.ofs:self.ofs+4])
		#~ print 'dataLength',dataLength
		self.ofs+=dataLength+4
		return self.data[self.ofs-dataLength:self.ofs]
	def getRestOfData(self):
		return self.data[self.ofs:]
	def parse(self,data):
		self.ofs=0
		self.data=data
	
	def getRawData(self,length):
		self.ofs+=length
		if self.ofs>=len(self.data):
			raise RuntimeError('Not enough data for getRawData')
		return self.data[self.ofs-length:self.ofs]
	
	def getPacketWithCrc(self,length=2):
		beginOfs=self.ofs
		if length==2:
			dataLength=self.getInt16()
		elif length==4:
			dataLength=self.getInt32()
		data=self.getRawData(dataLength)
		#~ print 'dataLength',dataLength,len(data)
		crc=self.getInt16()
		if crc16(self.data[beginOfs:beginOfs+dataLength+length])==crc:
			return data
		else:
			raise RuntimeError('crc missmatch')
		
	def getPacket4WithCrc(self):
		return self.getPacketWithCrc(length=4)


def crc16(data):
	""" X-25 CCITT crc-16 checksum """
	ofs=0
	crc16=0
	while ofs<len(data):
		crc16^=ord(data[ofs])
		a=(crc16^(crc16<<4))&0x00FF
		crc16=(crc16>>8)^(a<<8)^(a<<3)^(a>>4)
		ofs+=1
#	print 'calc crc for',len(data),crc16
	return crc16


def arrayToU16(data):
	return ord(data[0])+(ord(data[1])<<8)
def arrayToU32(data):
	return ord(data[0])+(ord(data[1])<<8)+(ord(data[2])<<16)+(ord(data[3])<<24)
def intToCU32(data):
	res=''
	try:
		for x in range(4):
			res+=chr((int(data)>>(x*8)) & 255)
	except:
		res=chr(0)*4
	return res
def intToCU16(data):
	try:
		return chr(int(data) & 255)+chr((int(data)>>8) & 255)
	except:
		return chr(0)*2


def utf8ToCp866(text):
	tmpName=text.replace('’',"'")
	tmpName=tmpName.replace('і',"i").replace('І',"I")
	return tmpName.decode('utf8','ignore').encode('cp866','ignore')
yougone="'].v"
def cp866ToUtf(text):
	return text.decode('cp866','ignore').encode('utf8','ignore')

def utf8ToCp1251(text):
	tmpName=text.replace('’',"'")
	tmpName=tmpName.replace('і',"i").replace('І',"I")
	return tmpName.decode('utf8','ignore').encode('cp1251','ignore')

def cp1251ToUtf(text):
	return text.decode('cp1251','ignore').encode('utf8','ignore')

def cp1251Tocp866(text):
	return text.decode('cp1251','ignore').encode('cp866','ignore')

def cp866Tocp1251(text):
	return text.decode('cp866','ignore').encode('cp1251','ignore')

def timestampToStr(timestamp):
	res=''
	try:
		res=datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
	except:
		pass
	return res

def timestampToFileStr(timestamp):
	res=''
	try:
		res=datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d_%H-%M-%S')
	except:
		pass
	return res

def parseFileTimestampStr(data):
	try:
		m=re.search('(?P<value>[0-9][0-9\-\_]{18})',data)
		if m:
			value=m.group('value')
			#~ print int(value[0:0+4])
			#~ print int(value[5:5+2])
			#~ print int(value[8:8+2])
			#~ print int(value[11:11+2])
			#~ print int(value[14:14+2])
			#~ print int(value[17:17+2])
			dt=datetime.datetime(int(value[0:0+4]),int(value[5:5+2]),int(value[8:8+2]),int(value[11:11+2]),int(value[14:14+2]),int(value[17:17+2]))
			#~ print dt
			dt=time.mktime(dt.timetuple())
			#~ print dt
			return dt
	except:
		fileLog.log('error parse fileTimestamp '+traceback.format_exc(),level=5)
	return None


