from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Feed, Post
from django.contrib import messages
from .parser_instagram import InstagramParser
from .parser_twitter import TwitterParser
from .parser_facebook import FacebookParser
from django.db.models import Q

def index(request):
    return HttpResponse('<h1> Welcome to FeedMerge</h1>')

def base(request):
  return render(request, 'base.html')

def home(request):
    posts = Post.objects.order_by('-post_time')
    feeds = Feed.objects.order_by('-last_update_date')
    # search_query = request.GET.get('search', '')

    context = {
        'posts': posts,
        'feeds': feeds,
        # 'search_query': search_query
    }

    if request.method == "POST":
        instagram_user_id = request.POST.get('instagram_user_id', '').strip()
        x_user_id = request.POST.get('x_user_id', '').strip()
        facebook_user_id = request.POST.get('facebook_user_id', '').strip()

        if not instagram_user_id and not x_user_id and not facebook_user_id:
            messages.warning(request, 'Please fill at least one input field to add feeds.')
            return render(request, 'home.html', context)

        try:
            if instagram_user_id:
                parser1 = InstagramParser(instagram_user_id)
                print("start parsing instagram")
                parser1.start_parse()
                
            if x_user_id:
                parser2 = TwitterParser(x_user_id)
                print("start parsing Twitter")
                parser2.start_parse()

            if facebook_user_id:
                parser3 = FacebookParser(facebook_user_id)
                print("start parsing Facebook")
                parser3.start_parse()
                
            messages.success(request, "Parsing data completed successfully.")
            
        except Exception as e:
            messages.error(request, f"Failed to parse platforms due to: {str(e)}")
            print("Failed to parse platforms")

        return redirect('home')        
        
    else:    
        return render(request, 'home.html', context)