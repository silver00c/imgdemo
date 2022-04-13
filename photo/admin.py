from django.contrib import admin
from photo.models import Category, Photo, Tag

admin.site.register(Photo)
admin.site.register(Category)
admin.site.register(Tag)