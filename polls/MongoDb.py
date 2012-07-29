from pymongo import Connection
from pymongo.errors import ConnectionFailure
import sys

class MongoDb:
	def __init__(self,host="localhost",port=27017,dbName='logdb'):
		self.host=host
		self.port=port
		self.dbName=dbName
		self.c=None
		self.db=None
		self.connected=False

		self.connect()

	def connect(self):
		self.connected=False
		try:
			self.c = Connection(host=self.host, port=self.port)
			print "Connected successfully"
		except ConnectionFailure, e:
			sys.stderr.write("Could not connect to MongoDB: %s" % e)
			return

		self.db = self.c[self.dbName]
		self.connected=True
		return True

	def insert(self,table,data):
		if not self.connected:
			if not self.connect():
				return None

		return self.db[table].insert(data,safe=True)

	# def select
