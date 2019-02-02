from django.shortcuts import render
from blog.models import Blogposts

def index(request):
    my_posts = Blogposts.objects.order_by('posttime')
    posts = {'blog_posts':my_posts}
    return render(request,"blog/index.html",context=posts)

