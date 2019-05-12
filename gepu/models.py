from django.db import models
from uuid import uuid4
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

class User(models.Model):
    '''
    backward relations: posts, your_posts, events, your_events
    '''
    # default id: Serial for user
    car_info = models.CharField(max_length=25,blank=True)
    phone = models.CharField(max_length=15,blank=True)

    # fb API may provide
    fb_id = models.BigIntegerField(null=True, blank=True)
    fbtoken = models.TextField(blank=True)
    messenger_id = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=35,blank=False)
    email = models.CharField(max_length=25,blank=True)
    photo = models.TextField(blank=True)

    # nice to have
    join_date = models.DateTimeField(default=timezone.now,editable=False)

    def __str__(self):
        return self.name

class Post(models.Model):
    # default id: Serial for post
    isRide = models.BooleanField(default=False)
    third_Party = models.BooleanField(default=False)
    from_addr = models.TextField(blank=True)
    to_addr = models.TextField(blank=True)
    seats = models.PositiveSmallIntegerField(default=0,blank=True)
    event = models.ForeignKey('Event',on_delete=models.CASCADE, related_name='posts')
    creator = models.ForeignKey('User',on_delete=models.CASCADE,related_name="your_posts")
    time = models.DateTimeField(default=timezone.now,blank=True)
    users = models.ManyToManyField('User',default=-1, related_name='posts', blank=True)

    def __str__(self):
        return str(self.creator.name) + str(self.from_addr)

class Event(models.Model):
    '''
    backward relations: posts, hash
    '''
    # default id: Serial for event
    fb_eid = models.BigIntegerField(default=-1)
    members = models.ManyToManyField('User',default=-1, related_name='events')
    hosts = models.ManyToManyField('User',default=-1, related_name='your_events')

    # fb API may provide
    info = models.TextField(default='', null=True,blank=True)
    # photo = models.TextField(default='', null=True,blank=True)
    # title = models.CharField(max_length=20,default='')
    # to_addr = models.TextField(default='')
    time = models.DateTimeField(default=timezone.now)
    # what's shown as string (e.f.admin application, object)
    def __str__(self):
        return str(self.fb_eid)
    def __int__(self):
        return self.fb_eid

def five_days_valid():
    '''
    return five days from now()
    '''
    return timezone.now() + timezone.timedelta(days=5)

class Hash(models.Model):
    hash_code = models.CharField(primary_key = True, max_length=4,default='BEEF')
    public = models.BooleanField(default=True,blank=False)
    whitelist = ArrayField(models.BigIntegerField(null=True, blank=True), null=True, blank=True)
    #valid = models.BooleanField(default=False,blank=False)
    valid_util = models.DateTimeField(default=five_days_valid)
    event = models.ForeignKey('Event',on_delete=models.SET_NULL, related_name='hash',null=True, default=None, blank=True)

    def __str__(self):
        return self.hash_code
