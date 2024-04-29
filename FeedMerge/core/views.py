from django.shortcuts import render, redirect
from django.http import HttpResponse # to get the request, we need to import this
from .models import Feed, Post
from .parser_instagram import InstagramParser

def index(request):
    return HttpResponse('<h1> Welcome to FeedMerge</h1>')
def base(request):
  return render(request, 'base.html')
def home(request):
    posts = Post.objects.order_by('-post_time')
    feeds = Feed.objects.order_by('-last_update_date')  # Assuming there is a 'feed_time' field
    context = {
        'posts': posts,
        'feeds': feeds,
    }
    if request.method == "POST":
        instagram_user_id = request.POST['instagram_user_id']
        x_user_id = request.POST['x_user_id']
        facebook_user_id = request.POST['facebook_user_id']
        parser = InstagramParser(instagram_user_id)
        parser.start_parse()
        print("parse data done")
        return redirect('/home')    
        
    else:    
        return render(request, 'home.html', context)
