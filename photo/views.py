
from importlib.machinery import DEBUG_BYTECODE_SUFFIXES
from django.http import HttpResponse
from django.shortcuts import render
from photo.models import Photo,Category,Tag

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

import os
from django.http import HttpResponse, Http404, FileResponse

from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from photo.permissions import IsAdminUserOrReadOnly

from photo.serializers import ImageSerializer,TagSerializer

from django.views.decorators.csrf import csrf_exempt

from photo.serializers import PhotoModelSerializer,CategorySerializer,PhotoSerializer,CategoryDetailSerializer

from rest_framework import viewsets
from rest_framework.permissions import BasePermission,IsAdminUser
from rest_framework.views import APIView

from django.http import Http404
from rest_framework import generics,filters
from django_filters.rest_framework import DjangoFilterBackend

def home(request):
    photos = Photo.objects.all()
    context = {'photo':photos}

    # 处理登入登出的POST请求
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user     = authenticate(request, username=username, password=password)
        # 登入
        if user is not None and user.is_superuser:
            login(request, user)
        # 登出
        isLogout  = request.POST.get('isLogout')
        if isLogout == 'True':
            logout(request)

    return render(request,'photo\list.html',context)

@api_view(['GET','POST'])
def upload(request):
    if request.method == 'POST':
        images=request.FILES.get('image')
        photo = Photo(image=images)
        photo.save()
        serializer = ImageSerializer(photo)
        return JsonResponse(serializer.data, safe=False)
    else:
        return Http404

@api_view(['GET', 'POST'])
def processimg(request):
        images = request.FILES.getlist('images')
        for i in images:
            print(i)
            photo = Photo(image=i)
            print("-----\n")
            print(photo)
            print("-----\n")
        #print(photo)
        #images = request.GET.get('images')
        #print(images)
        #(filepath, images) = os.path.split(images)
        # print('----------\n'+images)
        #photo = Photo(image=images)
        #photo.image = images
        # print("-------\n")
        # print(photo.image)
        # print("--")
        # print(photo.created)
            serializer = ImageSerializer(photo)
            return JsonResponse(serializer.data, safe=False)
        #photo.save()
        #return render(request,'base.html')
        response = HttpResponse("not here")
        return response
        

def download(request):
    file_path = request.POST.get('file_path')
    ext = os.path.basename(file_path).split('.')[-1].lower()
    # cannot be used to download py, db and sqlite3 files.
    if ext not in ['py', 'db',  'sqlite3']:
        response = FileResponse(open(file_path, 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response
    else:
        raise Http404


class IsAdminUser(BasePermission):
    message='请先登录'
    def has_permission(self, request, view):
        # 仅管理员可进行其他操作
        return True
        return request.user.is_superuser

class PhotoViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author__username']
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsAdminUser]
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
class CategoryViewSet(viewsets.ModelViewSet):
    """分类视图集"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = None
    def get_serializer_class(self):
        if self.action == 'list':
            return CategorySerializer
        else:
            return CategoryDetailSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = None
