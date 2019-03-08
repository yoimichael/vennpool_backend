# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render

# REST
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# user Django paginator to divide many data into pages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import User, Event, Post, Hash
from .serializers import UserSerializer, EventSerializer, PostSerializer, HashSerializer
from django.utils import timezone

# for random hash_code
from random import randint

# ----------------------USER----------------------
# Get the type of request
@api_view(['GET', 'POST'])
def users_list(request):
    """
    List users, or create a new user.
    """
    # GET request
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        users = User.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(users, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = UserSerializer(data,context={'request': request} ,many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data , 'count': paginator.count, 'numpages' : paginator.num_pages, 'nextlink': '/api/user/?page=' + str(nextPage), 'prevlink': '/api/user/?page=' + str(previousPage)})

    # POST request
    elif request.method == 'POST':
        # fetch the data
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
    # locate the user
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user,context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        # POST request


# ----------------------EVENT----------------------

@api_view(['GET', 'POST'])
def event_list(request, event_ids):
    """
    List events, or create a new event.
    """
    # GET request
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        events = Event.objects.filter(id__in=event_ids.split(','))
        page = request.GET.get('page', 1)
        paginator = Paginator(events, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = EventSerializer(data,context={'request': request} ,many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data , 'count': paginator.count, 'numpages' : paginator.num_pages, 'nextlink': '/api/event/?page=' + str(nextPage), 'prevlink': '/api/event/?page=' + str(previousPage)})

    # POST request
    elif request.method == 'POST':
        # fetch the data
        serializer = EventSerializer(data=request.data)
        # save the data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def event_detail(request, id):
    """
    Retrieve, update or delete a event by id/pk.
    """
    # locate the event
    try:
        event = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EventSerializer(event,context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EventSerializer(event, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        # POST request

# ----------------------POST----------------------

# Get the type of request
@api_view(['GET', 'POST'])
def post_list(request, post_ids):
    """
    List posts, or create a new post.
    """
    # GET request
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        posts = Post.objects.filter(id__in=post_ids.split(','))
        page = request.GET.get('page', 1)
        paginator = Paginator(posts, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = PostSerializer(data,context={'request': request} ,many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data , 'count': paginator.count, 'numpages' : paginator.num_pages, 'nextlink': '/api/post/?page=' + str(nextPage), 'prevlink': '/api/post/?page=' + str(previousPage)})

    # POST request
    elif request.method == 'POST':
        # fetch the data
        serializer = PostSerializer(data=request.data)
        # save the data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
        serializer = PostSerializer(post, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        # POST request

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
