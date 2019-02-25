from django.db import models
from uuid import uuid4
from django.utils import timezone

class User(models.Model):
    # let postgres make its own primary key
    uid = models.UUIDField(default=uuid4, editable=False)
    phone = models.CharField(max_length=15,blank=False)
    name = models.CharField(max_length=20,blank=False)
    car_info = models.CharField(max_length=25,blank=True)
    email = models.CharField(max_length=25,blank=True)
    photo = models.TextField(blank=True)
    #groups = models.ManyToManyField('Group', blank=True, null=True, related_name='users')
    # posts = models.ManyToManyField('Post', blank=True)
    join_date = models.DateTimeField(default=timezone.now,editable=False)
    def __str__(self):
        return self.name

class Post(models.Model):
    #uid = models.UUIDField(default=uuid4, editable=False)
    # cascade: if the event is deleted, this post will be deleted
    event = models.ForeignKey('Event',on_delete=models.CASCADE, related_name='posts')
    # stores the id who craeted it
    creatorID = models.DecimalField(max_digits=10, decimal_places=0)
    # indicator whether it's a ride request (True) or drive offer (False)
    isRide = models.BooleanField(default=False)
    third_Party = models.BooleanField(default=False)
    from_addr = models.TextField(blank=True)
    seats = models.PositiveIntegerField(default=0)
    time = models.DateTimeField(default=timezone.now)
    users = models.ManyToManyField('User',default=-1, related_name='posts')
    def __str__(self):
        return str(self.time)

class Event(models.Model):
    #uid = models.UUIDField(default=uuid4, editable=False)
    title = models.CharField(max_length=20,default='')
    to_addr = models.TextField(default='')
    photo = models.TextField(default='', null=True,blank=True)
    info = models.TextField(default='', null=True,blank=True)
    #posts = models.ManyToManyField('Post',default=-1,blank=True)
    # counter for claimed rides
    #count = models.IntegerField(default=0)
    time = models.DateTimeField(default=timezone.now)
    # cascade: if the group it belongs is deleted, it gets deleted.
    group = models.ForeignKey('Group',on_delete=models.CASCADE, related_name='events')
    def __str__(self):
        return self.title

class Group(models.Model):
    gid = models.UUIDField(default=uuid4, editable=False)
    name = models.CharField(max_length=36,default='')
    admin = models.CharField(max_length=36,default='') # stores admin's uid
    users = models.ManyToManyField('User', null=True,default=-1,related_name='groups')
    #events = models.ManyToManyField('Event', null=True,default=-1,blank=True)
    def __str__(self):
        return self.name

