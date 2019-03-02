# -*- coding: utf-8 -*-

'''
Front end of front-back test
'''

from __future__ import unicode_literals
from django.shortcuts import render

# REST
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# event Django paginator to divide many data into pages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Event
from .serializers import EventSerializer

# Get the type of request
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
