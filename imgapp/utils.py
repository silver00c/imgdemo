import random
import os
import datetime
from pathlib import Path

from django.conf import settings

def ranstr(num):
    H = 'abcdefghijklmnopqrstuvwxyz0123456789' 
    H0 = 'abcdefghijklmnopqrstuvwxyz' 

    salt = ''

    salt += random.choice(H0) 
    for i in range(num-1): 
        salt += random.choice(H)

    return salt

# 接收并保存图片
def save_img(image, dest_father_dir):
    # 创建存储路径
    img_dir1 = os.path.join(settings.MEDIA_ROOT, dest_father_dir)
    if not os.path.exists(img_dir1):
        os.mkdir(img_dir1)
    img_dir2 = os.path.join(img_dir1, datetime.datetime.now().strftime("%Y"))
    if not os.path.exists(img_dir2):
        os.mkdir(img_dir2)
    img_file = os.path.join(img_dir2, datetime.datetime.now().strftime("%m"))
    if not os.path.exists(img_file):
        os.mkdir(img_file)

    # 防重名
    p = Path(image.name)
    img_pure_name = p.stem + ranstr(5)
    img_extend_name = p.suffix
    img_name = img_pure_name + img_extend_name

    # 存储图片
    destination = open(os.path.join(img_file, img_name), 'wb+')
    for chunk in image.chunks():
        destination.write(chunk)
    destination.close()

    return  img_name

# 获取图片存储地址
def get_img_url(request, img_file, img_name):
    if request.is_secure():
        protocol = 'https'
    else:
        protocol = 'http'
    # 传回给后端ImageField要存储的图片路径
    backend_relative_path = img_file + '/' + datetime.datetime.now().strftime("%Y") + '/' + datetime.datetime.now().strftime("%m") + '/' + img_name
    relative_path = settings.MEDIA_URL + backend_relative_path
    # 前端显示需要的图片路径
    frontend_url = protocol + '://'+ str(request.META['HTTP_HOST']) + relative_path
    return {"url": frontend_url, "backend_path": backend_relative_path}
