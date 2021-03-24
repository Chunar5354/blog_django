from django.db import models
from django.contrib.auth.models import User
from article.models import ArticlePost

class Comment(models.Model):
    # 指定外键，on_delete的作用是当article删除时comment也随之删除
    article = models.ForeignKey(
        ArticlePost,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return self.body[:20]

# Create your models here.
