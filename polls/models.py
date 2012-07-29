# # from django.db import models
# from mongoengine import *

# class Device(Document):
#     deviceId =StringField(max_length=200)
#     ipAddress = StringField(max_length=200)

#     def __unicode__(self):
#     	return 'Device '+self.deviceId

# class LogMsg(Document):
#     deviceId = StringField(max_length=200)
#     data = StringField(max_length=200)
#     time =StringField(max_length=200)

# class logs(Document):
#     deviceId = StringField(max_length=200)
#     data = StringField(max_length=200)
#     # time =StringField(max_length=200)

#     def __unicode__(self):
#     	return 'from {}: {}'.format(self.deviceId,self.data)

