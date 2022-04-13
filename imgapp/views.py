import logging

from django_filters.rest_framework.backends import DjangoFilterBackend
from django.http import Http404

from rest_framework import mixins, filters, viewsets
from rest_framework import status as rest_status
from rest_framework.decorators import action
#from rest_framework.response import Response
from requests import Response
from rest_framework import exceptions as rest_framework_exceptions

from . import utils
from . import models, serializers

logger = logging.getLogger(__name__)

# 新闻
class NewsViewSet(viewsets.GenericViewSet):
    """
    新闻
      获取新闻列表，输入参数解释：
      status: 按新闻审核状态筛选
      category: 按新闻分类筛选
      search: 按关键词搜索
        搜索字段包括：('title', 'content')
      ordering: 按字段排序（默认为-update_time）
        可选列表为：('-update_time', )
        默认为正序，如需逆序，在前面加中横杠，例如'-update_time'
    """
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_fields = ('status', 'category')
    search_fields = ('title', 'content')
    ordering_fields = ('id', 'update_time')
    ordering = ('-update_time', )

    def get_queryset(self):
        return models.News.objects.all()

    def get_serializer_class(self):
        if self.action == 'img_upload':
            return serializers.NewsImgUploadSerializer

    @action(detail=False, methods=['post'], url_path="img_upload")
    def img_upload(self, request, pk=None):
        """
        上传新闻图片
        :param request: img 图片路径
        :return:
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            image = serializer.validated_data['img']
            img_file = "news_img" # 图片存储的文件夹

            img_name = utils.save_img(image, img_file)
            img_url = utils.get_img_url(request, img_file, img_name)
            
            return Response(status=rest_status.HTTP_201_CREATED, data=img_url)
        # 未知错误，报服务器内部错误
        except Exception as error:
            logger.error('图片上传失败，错误: %s' % (error))
            return Response(status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR, data={"detail": "服务器内部错误"})

