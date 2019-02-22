# -*- coding: utf-8 -*-

'''
Front end of front-back test 
'''

from __future__ import unicode_literals
from django.shortcuts import render

# for index
from django.http import HttpResponse

# ---test RESTful
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# user Django paginator to divide many data into pages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import User
#from .serializers import UserSerializer

# ----- from file serializer
from rest_framework import serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','phone','name', 'car_info', 'email')


# default index page
@api_view(['GET'])
def index_prompt(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# Create your views here.

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

        serializer = UserSerializer()(data,context={'request': request} ,many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data , 'count': paginator.count, 'numpages' : paginator.num_pages, 'nextlink': '/api/gepu/?page=' + str(nextPage), 'prevlink': '/api/gepu/?page=' + str(previousPage)})


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
        serializer = UserSerializer()(user,context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer()(user, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


