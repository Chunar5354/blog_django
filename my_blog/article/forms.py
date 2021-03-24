from django import forms
from .models import ArticlePost

class ArticlePostForm(forms.ModelForm):
    class Meta:
        # 数据模型来自于ArticlePost
        model = ArticlePost
        # 表单包含两个字段
        fields = ('title', 'body', 'tags')
