from django.http import Http404

from django.shortcuts import render
from django.http import HttpResponse
from dataclasses import dataclass
from .data import CATEGORIES, POSTS



def index(request):
    return HttpResponse("<h1>Привет из Django 6.1!</h1>")

def post_list(request):
    posts = [post for post in POSTS if post['is_published']]
    context = {
        "posts": posts,
        "categories": CATEGORIES,
        "page_title": "Межпространственный блог"
    }
    return render(request, "blog/post_list.html", context)

def post_detail(reguest, post_id):
    for post in POSTS:
        if post['id'] == post_id:
            context = {"post": post, "categories": CATEGORIES, "page_title": post['title']}
            return render(reguest, "blog/post_detail.html", context)
        raise Http404(404, f"Пост с id={post_id} не найден")
    
