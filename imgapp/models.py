from django.db import models
from django.utils.timezone import now

# 新闻
class News(models.Model):
    """ 
    新闻
    """ 
    img = models.ImageField('展示图片', upload_to="news_img/%Y/%m/", max_length=256, blank=True)
    created = models.DateTimeField(default=now)
    
    def __str__(self):
        return self.image.name
    
    class Meta:
        ordering = ('-created',)
        verbose_name = '新闻'
        verbose_name_plural = '新闻'