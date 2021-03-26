from django.shortcuts import render, redirect

def index(request):
    return redirect('article:article_list')
    # return render(request, 'index/index.html')

# Create your views here.
