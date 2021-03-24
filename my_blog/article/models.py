from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager

class ArticlePost(models.Model):
    # 用django内建的User关联作者
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    total_views = models.PositiveIntegerField(default=0)
    tags = TaggableManager(blank=True)

    class Meta:
        # ordering表示排列顺序
        ordering =('-created',)

    def __str__(self):
        return self.title

    # 路由重定向获取文章地址
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])

# Create your models here.
