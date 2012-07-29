import threading,socket,time,traceback,re

#~ from terminalUtils import *
import sys

sys.path.append('..')
#from utils.dataUtils import *
from utils.logProtocol import *

SpinDelay=0.1

def inRange(value,low,high):
	try:
		if value>=low and value<=high:
			return True
	except:
		#~ print 'wrong parameter'
		pass
	return False
def isIp(value):
	try:
		parts=value.split('.')
		if len(parts)==4:
			for x in parts:
				if not inRange(int(x),0,255):
					return False
			return True
	except:
		#~ print 'wrong parameter'
		pass
	return False
	
def eventSleep(delay,event=None,events=[]):
	i=0
	if event or events:
		while i<delay/SpinDelay:
			if events:
				for e in events:
					if e.isSet():
						return True
			elif event.isSet():
				return True
			time.sleep(SpinDelay)
			i+=1
	return False


class LogClient:
	def __init__(self,serverAddress='82.207.44.110',serverPort=5001,deviceId=None):
		self.originalServerAddress=serverAddress
		self.serverAddress=serverAddress
		self.deviceId=deviceId
		self.sock=None
		self.isConnected=False
		self.socketConnectionTimeout=10
		self.connectTimeout=20
		self.connectErrorDelay=5
		self.eventExit=threading.Event()
		self.error=''
		self.SendRetryCount=5
		self.SendErrorDelay=0.2
		self.SocketSendBuffer=4096
		self.serverPort=serverPort
		self.eventReady=threading.Event()
		self.queue=[]
		self.lock=threading.RLock()
		self.eventReady.set()
	
	def sendText(self,text,inThread=False):
		if not self.deviceId:
			print 'logClient have no deviceId'
			return
		#~ print 'sT',inThread,self.eventReady.isSet(),text,self.queue
		if inThread:
			if not self.eventReady.isSet():
				self.lock.acquire()
				try:
					self.queue+=[text]
				finally:
					self.lock.release()
			else:
				self.eventReady.clear()
				threading.Thread(target=self.sendText,args=(text,False)).start()
			return True
		try:
			logProtocol=LogProtocol()
			logProtocol.deviceId=str(self.deviceId)
			self.lock.acquire()
			try:
				texts=[text]+self.queue
				self.queue=[]
			finally:
				self.lock.release()
			sendedCount=0
			for text in texts:
				res=logProtocol.sendText(text)
				self.sendData(res)
				sendedCount+=1
			return True
		except:
			#~ pass
			print traceback.format_exc()
			self.lock.acquire()
			try:
				self.queue=texts[sendedCount:]
			finally:
				self.lock.release()
			eventSleep(10,events=[self.eventExit])
		finally:
			
			self.disconnect()
			self.eventReady.set()
		#~ print 'end SendText'
	
	def connect(self):
		#~ fileLog.log('connecting to log server'+str([self.serverAddress,self.serverPort,self.connectTimeout]),level=7)
		print 'connecting to log server'+str([self.serverAddress,self.serverPort,self.connectTimeout])
		self.isConnected=False
		if self.serverAddress:
			try:
				self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.sock.settimeout(self.socketConnectionTimeout)
				lastConnectTry=time.time()
				while 1:
					try:
						if self.eventExit.isSet():
							return
						self.isConnected=False

						if not isIp(self.serverAddress):
							try:
								#~ serverAddress=socket.gethostbyname(self.serverAddress)
								serverAddress=None
								res=getExecOutput('nslookup '+self.serverAddress)
								if res:
									for line in res[4:]:
										if 'Address' in line:
											m=re.search('([0-9\.]+)',line)
											if m:
												serverAddress=m.groups()[0]
												if isIp(serverAddress):
													self.serverAddress=serverAddress
													break
								if not serverAddress:
									cantResolve=True
									raise RuntimeError('cant resolve')
							except Exception,e:
								print 'cant resolve domain {} {}'.format(self.serverAddress,e)
								#~ fileLog.log('cant resolve domain {} {}'.format(self.serverAddress,e),level=6)
								if time.time()-lastConnectTry>self.connectTimeout:
									raise RuntimeError('cant connect')
								if eventSleep(3,events=[self.eventExit]):
									continue
						else:
							serverAddress=self.serverAddress
						res=self.sock.connect_ex((serverAddress,
							self.serverPort))
						if res!=0:
							if time.time()-lastConnectTry>self.connectTimeout:
								raise RuntimeError('cant connect')
							if res==11:
								time.sleep(0.2)
							else:
								if eventSleep(1,events=[self.eventExit]):
									break
							continue
						self.isConnected=True
						self.error=None
					except Exception,e:
						self.isConnected=False
						print ".",e,self.serverAddress,self.serverPort,traceback.format_exc()
						if time.time()-lastConnectTry>self.connectTimeout:
							self.serverAddress=self.originalServerAddress
							raise RuntimeError('cant connect')
						if eventSleep(1,events=[self.eventExit]):
							#~ print 'tcpClient.connecttoserver exited'
							break
						continue
					#~ fileLog.log('CONNECTED',level=7)
					break
			except Exception,e:
				#~ self.inputHandler.printError(("can't connect to server",e,traceback.format_exc()))
				print "can't connect to log server",e
				self.isConnected=False
				if eventSleep(self.connectErrorDelay,events=[self.eventExit]):
					pass
					#~ print 'tcpClient.connecttoserver exited'
					#~ break
		return self.isConnected
		
	def disconnect(self):
		self.isConnected=False
		if self.sock:
			try:
				self.sock.shutdown(socket.SHUT_RDWR)
			except:
				pass
		if self.sock:
			try:
				self.sock.close()
			except:
				#~ fileLog.log('self.sock.close()'+traceback.format_exc(),level=6)
				pass
		
	def shutdown(self):
		self.eventExit.set()
		
	def sendData(self,fulldata):
		if not self.isConnected:
			if not self.connect():
				print 'not connected to logserver'
				return None
		if self.isConnected:
			ofs=0
			retry=self.SendRetryCount
			while retry:
				try:
					while ofs!=len(fulldata):
						if self.eventExit.isSet():
							return None
						length=self.sock.send(fulldata[ofs:ofs+self.SocketSendBuffer])
						ofs+=length
						if length>0:
							retry=self.SendRetryCount
						#~ print 'sended',length,'ofs',ofs,'len',len(fulldata)
					return True
				except:
					#~ fileLog.log('cant send packet'
					time.sleep(self.SendErrorDelay)
					retry-=1
					#~ fileLog.log('why bug? '+traceback.format_exc())
		print 'cant send log'
		#~ self.isConnected=False
		return None
		
if __name__ == '__main__':
	logClient=LogClient(serverAddress='127.0.0.1')
	logClient.sendText('hallou')
