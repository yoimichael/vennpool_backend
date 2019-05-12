# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render

# REST
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
# REST auth
#from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny # default is IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User as User_auth
from requests import get

#test
from django.core import serializers

# user Django paginator to divide many data into pages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import User, Event, Post, Hash
from .serializers import UserSerializer, EventSerializer, PostSerializer, HashSerializer, PostPublicSerializer
from django.utils import timezone

# for random hash_code
from random import randint

import logging
logger = logging.getLogger("django")

# ----------------------USER----------------------
@api_view(['POST'])
@permission_classes((AllowAny,))
def get_auth_token(request):
    '''
    as user log in
    takes a username, id and fb token, returns gepu's auth token
    '''
    data = request.data
    fb_id = data.get('fb_id') # id here is user's fb_id
    fbtoken = data.get('fbtoken')
    email = data.get('email')
    # verify data
    if fb_id is None or fbtoken is None:
        return Response({'error': 'Invalid Credentials0'},status=status.HTTP_404_NOT_FOUND)

    # verify fbtoken
    response = get('https://graph.facebook.com/me?access_token='+ fbtoken).json()
    if 'id' not in response or response['id'] != fb_id:
        return Response({'error': 'Invalid Credentials1'},status=status.HTTP_404_NOT_FOUND)

    try:
        # find user in auth db
        auth_user = User_auth.objects.get(username=fb_id)
    except (User_auth.DoesNotExist):
        # if user doesn't exist in auth db
        auth_user = User_auth.objects.create_user(username=fb_id, email=email, password=fbtoken)
    # update the token
    auth_user.set_password(fbtoken)
    auth_user.save()
    # get auth token
    db_token, _ = Token.objects.get_or_create(user=auth_user)
    response = {'db_token' : db_token.key}

    try:
        # find user in auth db
        gepu_user = User.objects.get(fb_id=fb_id)
        # update the fbtoken if updated
        if gepu_user.fbtoken != fbtoken:
            gepu_user.fbtoken = fbtoken
            gepu_user.save(update_fields=["fbtoken"])
        response.update({'exist': True, 'user':UserSerializer(gepu_user).data})
    except (User.DoesNotExist):
        response.update({'exist': False})

    return Response(response, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def remove_auth_token(request):
    '''
    as user log out
    delete the session data of the user
    '''
    data = request.data
    id = data.get('fb_id')
    if id == None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # locate the user
    try:
        # get User object that has all user data
        user_auth = User_auth.objects.get(username=id)
        # get the token object that has user token and auth_user object
        # user_token = Token.objects.get(key=data.get('db_token'))
        # confirm user Id and token match
        # if (user_token.user.username != user_auth.username):
        if (request.user.username != user_auth.username):
            return Response(status=status.HTTP_404_NOT_FOUND)
    except (User_auth.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)

    # delete sessions
    # user_token.delete()
    request.user.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def create_user(request):
    # if user doesn't have a fb id (a bu from the complete profile)
    if 'fb_id' not in request.data or not request.data['fb_id']:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # store the user data to db
    serializer = UserSerializer(data=request.data)
    # save the data
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def users_detail(request, id):
    """
    Retrieve, update or delete a user by id/pk.
    """
    if request.method == 'GET':
        try:
            # locate the user
            user = User.objects.get(id=id)
        except (User.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
        serialized_data = serializers.serialize("json",[user],fields=('id','name','car_info','fb_id'))

        # serializer = UserSerializer(user,context={'request': request},fields=('id','name','car_info','fb_id'))
        return Response(serialized_data,status=status.HTTP_200_OK)
    else:
        try:
            # confirm user Id and token match
            user_id = request.data.get('id')
            # locate user
            user = User.objects.get(id=user_id)
            # get the token object that has user token and auth_user object
            # db_token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
            # user_token = Token.objects.get(key=db_token)
            # confirm user Id and token match
            # if (user_token.user.username != str(user.fb_id)):
            if (request.user.username != str(user.fb_id)):
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except (User.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        # udpate user
        if request.method == 'PUT':
            user.car_info = request.data.get('car_info')
            user.phone = request.data.get('phone')
            user.name = request.data.get('name')
            user.save()
            serializer = UserSerializer(user)
            return Response(serializer.data)

        elif request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # POST request?


# ----------------------EVENT----------------------
# import logging
# logger = logging.getLogger("django")
#logger.info("The value of var is %r", fb_eid_time)

@api_view(['POST'])
def event_list(request):
    """
    Take a dictionary of fb_eids to their time
    returns all posts ids associated for that event
    """
    fb_eid_time = request.data
    # limit the size of event_ids
    if (len(fb_eid_time) > 40):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # TODO:: get info about user id = data.get('id') and add user to event (for post protection: check if user belongs to the event)

    # get the query set of given events
    events_qs = Event.objects.filter(fb_eid__in=fb_eid_time.keys())

    # if all events exist, repond with serialized info
    if len(events_qs) == len(fb_eid_time):
        serializer = EventSerializer(events_qs,many=True)
    else:
        # if some events don't exist in db, create them
        event_list = []
        for fb_eid in fb_eid_time:
            new_event = events_qs.get_or_create(
                            fb_eid = fb_eid,
                            time=fb_eid_time[fb_eid])
            event_list.append(new_event)
        serializer = EventSerializer(event_list,many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

# ----------------------POST----------------------
# Get the type of request
@api_view(['POST'])
def create_ride(request):
    '''
    gets the user's db id, fb_eid, and ride_data:
    isRide (bool), third_Party (bool), seats (PositiveSmallIntegerField)
    creates a ride for the event, if the event doesn't exist, create one
    '''
    # get request data
    data = request.data
    fb_eid = data.get('fb_eid')
    id = data.get('id')
    ride_data = data.ride_data

    try:
        # locate user
        user = User.objects.get(id=id)
        # get the token object that has user token and auth_user object
        # user_token = Token.objects.get(key=request.META['Authorization'])
        # confirm user Id and token match
        # if (user_token.user.username != user.fb_id):
        if (request.user.username != str(user.fb_id)):
            return Response(status=status.HTTP_404_NOT_FOUND)
    except (User.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        # locate event
        event = Event.objects.get(fb_eid=fb_eid)
    except (Event.DoesNotExist):
        # create a new event if it doesn't exist
        serializer = EventSerializer(data={'fb_eid':fb_eid})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        event = serializer.save()
        # make the creator a host
        event.hosts.add(user)

    # make user a member
    if user not in event.members:
        event.members.add(user)

    # add ForeignKey to new post
    ride_data['creator'] = users
    ride_data['event'] = event
    # create ride for user
    serializer = PostSerializer(data=ride_data)
    # save the data
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, id):
    """
    Retrieve, update or delete a post by id/pk.
    """
    # locate the post
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post,context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        user_id = request.data.get('id')
        try:
            user = User.objects.get(id = user_id)
        except (User.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        if user in post.users:
            post.users.remove(user)
        else:
            post.users.add(user)

        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        # POST request

@api_view(['POST'])
def post_list(request):
    """
    create new post(s)
    and return them
    """
    try:
        user_id = request.data.get('uid');
        event_id = request.data.get('eid');
        # locate user
        user = User.objects.get(id=user_id)
        # verify the actor is the user id in data
        if (request.user.username != str(user.fb_id)):
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        # locate event
        event = Event.objects.get(id=event_id)
    except (User.DoesNotExist, Event.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)
    # create posts
    posts = []
    logger.info("request.data is %r", request.data)
    for name in ['post1', 'post2']:
        if (name in request.data):
            post = request.data.get(name)
            logger.info("post is %r", post)
            p = Post(from_addr=post['from_addr'],
                    seats=post['seats'],
                    time=post['time'],
                    creator=user,
                    event=event)
            posts.append(p)
            p.save()
    # return the created ones
    serializer = PostPublicSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# ----------------------HASH----------------------
@api_view(['GET'])
def get_event(request, hash,auth_id):
    '''
    given the hash return event if authenticated
    '''
    try:
        hash = Hash.objects.get(hash_code=hash)
    except Hash.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # if hash is not valid
    if (not hash.valid):
        return Response(status=status.HTTP_404_NOT_FOUND)

    # if user is allowed to join
    if (hash.public or auth_id in hash.whitelist):
        serializer = EventSerializer(hash.event,context={'request': request})
        return Response(serializer.data)

def days_valid(num_days = 5):
    return timezone.now() + timezone.timedelta(days=num_days)

@api_view(['GET', 'PUT'])
def get_hash(request, event_id):
    '''
    given an event id return a hash of it (generate one if necessary)
    '''
    # try to find the event first
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    auth_id = request.data.auth_id
    if (auth_id not in event.hosts):
        # if you are not the admin, you can't get the hash
        return Response(status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        hash = event.hash
        if (hash is None or not hash.event is not None):
            # respond that there's not code found
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            # hash found
            serializer = HashSerializer(hash,context={'request': request})
            return Response(serializer.data)

    # assuming
    elif request.method == 'PUT':
        # creating a hash
        new_hash = Hash.objects.filter(event=None).first()
        if new_hash.exists():
            # assign events
            new.hash.event = event
            # assign date
            days = request.data.days
            if (days):
                new.hash.valid_util = days_valid(int(days))
            else:
                new.hash.valid_util = days_valid(int(days))
            # assign whitelist and public
            public = bool(request.data.public)
            new.hash.public = public
            if (public):
                new.hash.whitelist = []
            else:
                new.hash.whitelist = request.data.whitelist
        else:
            # when all hashes are not available create a new hash that is not pure numbers
            print("Creating non-number cache.")
            new_hash = "".join([char(randint(3,126)) for i in range(4)])
            if (Hash.objects.filter(hash_code=new_hash).exists()):
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = HashSerializer(data=request.data, hash=new_hash,event=event)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def get_event(request, hash_code):
    '''
    given an event id return a hash of it (generate one if necessary)
    '''
    # try to find the event first
    try:
        hash = Hash.objects.get(hash_code=hash_code)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # locate event
    event = hash.event
    if (event is None):
        return Response(status=status.HTTP_404_NOT_FOUND)

    # confirm user authentication
    auth_id = request.data.auth_id
    if (auth_id not in event.hosts and auth_id not in hash.whitelist):
        # if you are not the admin, you can't get the hash
        return Response(status=status.HTTP_403_FORBIDDEN)

    if (hash is None or not hash.event is not None):
        # respond that there's not code found
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # respond with the event data
    serializer = EventSerializer(event,context={'request': request})
    return Response(serializer.data)


# unused functions
# # Get the type of request
# @api_view(['GET', 'POST'])
# def users_list(request):
#     """
#     List users, or create a new user.
#     """
#     # GET request
#     if request.method == 'GET':
#         data = []
#         nextPage = 1
#         previousPage = 1
#         users = User.objects.all()
#         page = request.GET.get('page', 1)
#         paginator = Paginator(users, 10)
#         try:
#             data = paginator.page(page)
#         except PageNotAnInteger:
#             data = paginator.page(1)
#         except EmptyPage:
#             data = paginator.page(paginator.num_pages)
#
#         serializer = UserSerializer(data,context={'request': request} ,many=True)
#         if data.has_next():
#             nextPage = data.next_page_number()
#         if data.has_previous():
#             previousPage = data.previous_page_number()
#
#         return Response({'data': serializer.data , 'count': paginator.count, 'numpages' : paginator.num_pages, 'nextlink': '/api/user/?page=' + str(nextPage), 'prevlink': '/api/user/?page=' + str(previousPage)})
#
#     # POST request
#     elif request.method == 'POST':
#         # fetch the data
#         serializer = UserSerializer(data=request.data)
#         # save the data
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def event_detail(request, id):
#     """
#     Retrieve, update or delete a event by id/pk.
#     """
#     # locate the event
#     try:
#         event = Event.objects.get(id=id)
#     except Event.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = EventSerializer(event,context={'request': request})
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = EventSerializer(event, data=request.data,context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         event.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#         # POST request
