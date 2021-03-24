from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import ArticlePostForm
from .models import ArticlePost
from comment.models import Comment
import markdown

def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    tag = request.GET.get('tag')

    article_list = ArticlePost.objects.all()

    if search:
        # 使用Q对象进行搜搜
        article_list = article_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ''  # 防止search变成None

    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])

    if order == 'total_views':
        article_list = article_list.order_by('-total_views')

    paginator = Paginator(article_list, 2)
    # 通过utl中 ?key=value 来查询key参数的值
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    context = { 'articles': articles, 'order': order, 'search': search, 'tag': tag }
    return render(request, 'article/list.html', context)

@login_required(login_url='/userprofile/login/')
def article_manage(request):
    articles = ArticlePost.objects.all()
    context = { 'articles': articles }
    return render(request, 'article/manage.html', context)

@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect('article:article_manage')
    else:
        return HttpResponse('请使用POST方法')

# 接收url中传递的id参数
def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)
    article.total_views += 1
    article.save(update_fields=['total_views'])

    # 渲染markdown
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
    # 通过convert将正文渲染正html页面
    article.body = md.convert(article.body)

    comments = Comment.objects.filter(article=id)
    # 目录单独拿出来
    context = { 'article': article, 'toc': md.toc, 'comments': comments}
    return render(request, 'article/detail.html', context)

@login_required(login_url='/userprofile/login/')
def article_create(request):
    # 如果用户是POST操作就提交内容
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)  # 先不提交
            new_article.author = User.objects.get(id=1)
            new_article.save()
            # 保存tags的多对多关系
            article_post_form.save_m2m()
            return redirect('article:article_list')
        else:
            return HttpResponse('内容有误，请重新填写')
    # 如果用户是GET操作就显示表单界面
    else:
        article_post_form = ArticlePostForm()
        context = { 'article_post_form': article_post_form }
        return render(request, 'article/create.html', context)

# Create your views here.
