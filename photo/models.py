from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Tag(models.Model):
    """文章标签"""
    text = models.CharField(max_length=30)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.text

class Category(models.Model):
    """图片分类"""
    title = models.CharField(max_length=100)
    created = models.DateTimeField(default=now)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

class Photo(models.Model):
    author = models.ForeignKey(
        User, 
        null=True,
        on_delete=models.CASCADE, 
        related_name='photos'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='articles'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='photos'
    )
    image = models.ImageField(upload_to='photo/')#%Y%m%d/
    created = models.DateTimeField(default=now)
    

    def __str__(self):
        return self.image.name
    
    class Meta:
        ordering = ('-created',)
