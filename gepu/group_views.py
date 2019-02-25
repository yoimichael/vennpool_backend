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

# user Django paginator to divide many data into pages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Group, User
from .serializers import GroupSerializer

# Get the type of request
@api_view(['GET', 'POST'])
def group_list(request, group_ids):
    """
    Takes a list of group-id's and return all the group objects that match
    List of user's groups, or create a new group (with user in it).
    """
    # GET request
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        groups = Group.objects.filter(id__in=group_ids.split(','))
        page = request.GET.get('page', 1)
        paginator = Paginator(users, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = GroupSerializer(data,context={'request': request} ,many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data , 'count': paginator.count, 'numpages' : paginator.num_pages, 'nextlink': '/api/group/?page=' + str(nextPage), 'prevlink': '/api/group/?page=' + str(previousPage)})

    # POST request
    elif request.method == 'POST':
        # fetch the data
        serializer = GroupSerializer(data=request.data)
        # save the data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def group_detail(request, id):
    """
    Retrieve, update or delete a group by id/pk.
    """
    # locate the user
    try:
        group = Group.objects.get(id=id)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GroupSerializer(group,context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = GroupSerializer(group, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        # POST request
