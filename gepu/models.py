from django.db import models
from uuid import uuid4
from django.utils import timezone

class User(models.Model):
    # let postgres make its own primary key
    uid = models.UUIDField(default=uuid4, editable=False)
    phone = models.CharField(max_length=15,default='')
    name = models.CharField(max_length=20,default='')
    car_info = models.CharField(max_length=25,default='',blank=True)
    email = models.CharField(max_length=25,default='',blank=True)
    photo = models.TextField(default='',blank=True)
    groups = models.ManyToManyField('Group', null=True,blank=True)
    posts = models.ManyToManyField('Post', null=True,blank=True)
    # join_date = models.DateTimeField('date published')
    def __str__(self):
        return self.name


class Post(models.Model):
    #uid = models.UUIDField(default=uuid4, editable=False)
    #eventID = models.ForeignKey('Event', on_delete=models.CASCADE,default=-1)
    eventID = models.CharField(max_length=36,default='')
    # assume the FIRST user created this post
    users = models.ManyToManyField('User',default=-1)
    # indicator whether it's a ride request (True) or drive offer (False)
    isRide = models.BooleanField(default=False)
    # indicator whther it's a ride share post that uses third party apps
    third_Party = models.BooleanField(default=False)
    from_addr = models.TextField(default='')
    # how many available spots (type 0, 2), how many people requests (type 1)
    count = models.IntegerField(default=0)
    time = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.time)

class Event(models.Model):
    #uid = models.UUIDField(default=uuid4, editable=False)
    title = models.CharField(max_length=20,default='')
    to_addr = models.TextField(default='')
    photo = models.TextField(default='', null=True,blank=True)
    info = models.TextField(default='', null=True,blank=True)
    #created = models.ForeignKey('User', on_delete=models.CASCADE, default=0)
    createrID = models.CharField(max_length=36,default='')
    posts = models.ManyToManyField('Post',default=-1,blank=True)
    # counter for claimed rides
    count = models.IntegerField(default=0)
    time = models.DateTimeField(default=timezone.now)
    # cascade: if the group it belongs is deleted, it gets deleted.
    groupID = models.OneToOneField('Group',default=-1,on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Group(models.Model):
    gid = models.UUIDField(default=uuid4, editable=False)
    name = models.CharField(max_length=36,default='')
    admin = models.CharField(max_length=36,default='') # stores admin's uid
    users = models.ManyToManyField('User', null=True,default=-1,blank=True)
    events = models.ManyToManyField('Event', null=True,default=-1,blank=True)
    def __str__(self):
        return self.name

