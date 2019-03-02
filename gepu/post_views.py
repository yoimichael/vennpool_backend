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

# post Django paginator to divide many data into pages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from .serializers import PostSerializer

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
