from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, update_last_login, Group
from django.contrib.auth.signals import user_logged_in
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView, 
    DeleteView
)
from .models import Post, City, Ad, Market, Comment
from users.models import Profile
import requests
from .forms import CityForm, CommentForm
# Import count obj
from django.db.models import Q, Count

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse

from random import randint

import time

# ADD BS4
from bs4 import BeautifulSoup


# Manually add a like with AJAX (might not work)
def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))

def home(request):
    context = {'posts': Post.objects.all()}
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['ads'] = Ad.objects.all().order_by('?')
        context['ads2'] = Ad.objects.all().order_by('?')
        context['ads3'] = Ad.objects.all().order_by('?')
        context['ads4'] = Ad.objects.all().order_by('?')
        context['trending'] = Post.objects.all().order_by('-blog_views')[0:5]
        context['notifications'] = Post.objects.annotate(ct=Count('likes')).order_by('-ct')[0:2]
        return context

class StoriesListView(ListView):
    model = Post
    template_name = 'blog/stories.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 1

class CuratedListView(ListView):
    model = Post
    template_name = 'blog/curated.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'poster'
    ordering = ['-date_posted']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['3Gen'] = Profile.objects.all().order_by('?')[0:3]
        context['ads'] = Ad.objects.all().order_by('?')
        context['ads2'] = Ad.objects.all().order_by('?')
        context['ads3'] = Ad.objects.all().order_by('?')
        context['ads4'] = Ad.objects.all().order_by('?')
        context['trending'] = Post.objects.all().order_by('-blog_views')[0:5]
        context['poster'] = Post.objects.all().order_by('?')
        return context

def trending(request):
    context = {'posts': Post.objects.all()}
    return render(request, 'blog/curated.html', context)

class TrendingListView(ListView):
    model = Post
    template_name = 'blog/trending.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['ads'] = Ad.objects.all().order_by('?')
        context['ads2'] = Ad.objects.all().order_by('?')
        context['ads3'] = Ad.objects.all().order_by('?')
        context['ads4'] = Ad.objects.all().order_by('?')
        context['trending'] = Post.objects.all().order_by('-blog_views')[0:5]
        context['profiles'] = Profile.objects.all().order_by('-Current_city')[0:5]
        return context



def showComment(request):
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(comments_post_id=post_id)

    return render(request, 'page.html', {'news': news, 'comments': comments, 'head1': head1})

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['publications'] = Publications.objects.all().order_by('?')
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):  
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['recommendations'] = Post.objects.all().order_by('?')[0:5]
        
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context['total_likes'] = total_likes
        context['liked'] = liked

        return context

    def get_object(self):
        obj = super().get_object()
        obj.blog_views += 0.25
        obj.save()
        return obj

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image', 'location', 'Add_post_to_group']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'blog/comment_create.html'
    form_class = CommentForm
    
    def get_success_url(self):
          # if you are passing 'pk' from 'urls' to 'DeleteView' for company
          # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
          pk = self.kwargs['pk']
          return reverse_lazy('post-detail', kwargs={'pk': pk})
    
    def form_valid(self, form):
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        comment = form.save(commit=False)
        comment.author = get_object_or_404(User, username=self.request.user)
        comment.post = stuff
        comment.save()
        return super().form_valid(form)

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    success_url = "/"
    
    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image', 'location', 'Add_post_to_group']

    def form_invalid(self, form):
        print("form is invalid")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostChangelogView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['changelog']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def careers(request):
    return render(request, 'blog/careers.html', {'title': 'Careers'})

def view_careers(request):
    return render(request, 'blog/careers_detail.html', {'title': 'Careers at Product'})

def business(request):
    return render(request, 'blog/business.html', {'title': 'Business'})

def weather(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'
    err_msg = ''
    message = ''
    message_class = ''

    if request.method == "POST":
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()

                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'That city doesn\'t exist. Please enter a valid city, state, or country.'
            else:
                err_msg = 'This city has already been added. Please do a cmd/ctrl+F and type it in.'

        if err_msg:
            message = err_msg
            message_class = "is-danger"
        else:
            message = "City has been publicly added!"
            message_class = "is-success"

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()

        city_weather = {
            'city': city.name,
            'temperature': r["main"]["temp"],
            'description': r["weather"][0]["description"],
            'icon': r["weather"][0]["icon"],
        }
        weather_data.append(city_weather)

    context = {
        'weather_data' : weather_data,
        'form' : form,
        'message' : message,
        'message_class' : message_class,
    }
    return render(request, 'blog/weather.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('blog-weather')

def legal(request):
    return render(request, 'blog/legal.html', {'title': 'Legal'})

def events(request):
    return render(request, 'blog/events.html', {'title': 'Events'})

class NewsListView(ListView):
    model = Post
    template_name = 'blog/news.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        p2 = get_object_or_404(User, username='vlad')
        p3 = get_object_or_404(User, username='Smartcart')
        trending_in_us = Post.objects.filter(Q(author=p2) | Q(author=p3)).order_by('?')[0:2]
        # covid_news = Post.objects.filter(author=c1).order_by('?')[0:10]
        return trending_in_us

def PeopleListView(request):
    p1 = get_object_or_404(User, username='vlad')
    p2 = get_object_or_404(User, username='Smartcart')
    p3 = get_object_or_404(User, username='ana')

    query = request.GET.get('q','')
    #The empty string handles an empty "request"
    if query:
            results = User.objects.filter(Q(username__icontains=query)).order_by('-username')[0:5]
    else:
       results = []

    if request.user.is_authenticated:
        global currentuser
        currentuser = request.user
    else:
        currentuser = None

    context = {
            '3Gen': Profile.objects.all().order_by('?')[0:3], 
            'users': Profile.objects.all().exclude(user=currentuser).order_by('?')[0:5],
            'trending':  Profile.objects.filter(Q(user=p1) | Q(user=p2) | Q(user=p3)),
            'results':results,
            'query':query,
            'profiles': Profile.objects.all().exclude(user=currentuser).order_by('?').order_by('-Current_city')[0:5], 
            'ads': Profile.objects.filter(ad=True).order_by('?')
    }
    return render(request, 'blog/people.html', context)

def HashtagView(request):
    context = {
            'tech': Post.objects.filter(Add_post_to_group='tech').order_by('?')[0:10],
            'travel': Post.objects.filter(Add_post_to_group='travel').order_by('?')[0:10],
    }
    return render(request, 'blog/hashtag.html', context)

# ADS

class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    fields = ['title', 'image', 'content', 'Add_a_link']
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class AdDetailView(DetailView):
    model = Ad

    def get_object(self):
        obj = super().get_object()
        obj.ad_views += 1
        obj.save()
        return obj

class UserAdListView(ListView):
    model = Ad
    template_name = 'blog/user_ads.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'ads'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Ad.objects.filter(author=user).order_by('-date_posted')


class AdUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ad
    fields = ['title', 'image', 'content', 'Add_a_link']
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class AdDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ad
    success_url = '/'
    
    def test_func(self):
        ad = self.get_object()
        if self.request.user == ad.author:
            return True
        return False


# Market

class MarketListView(ListView):
    model = Market
    template_name = 'blog/market.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'listings'
    ordering = ['-date_posted']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['ads'] = Ad.objects.all().order_by('?')
        context['ads2'] = Ad.objects.all().order_by('?')
        context['ads3'] = Ad.objects.all().order_by('?')
        context['ads4'] = Ad.objects.all().order_by('?')
        return context

class UserMarketListView(ListView):
    model = Market
    template_name = 'blog/user_market_posts.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class MarketDetailView(DetailView):
    model = Market
    # def get_object(self):
    #     obj = super().get_object()
    #     obj.blog_views += 1
    #     obj.save()
    #     return obj
    

class MarketCreateView(LoginRequiredMixin, CreateView, ListView):
    model = Market
    fields = ['enter_title', 'enter_price', 'Top_image_of_product', 'Image_2', 'Image_3', 'Image_4', 'Image_5', 'enter_condition', 'Describe_product', 'enter_public_address', 'enter_item_type']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['ads'] = Ad.objects.all().order_by('?')
        return context


class MarketUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Market
    fields = ['enter_title', 'enter_price', 'Top_image_of_product', 'Image_2', 'Image_3', 'Image_4', 'Image_5', 'enter_condition', 'Describe_product', 'enter_public_address', 'enter_item_type']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        market = self.get_object()
        if self.request.user == market.author:
            return True
        return False


class MarketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Market
    success_url = '/'
    
    def test_func(self):
        market = self.get_object()
        if self.request.user == market.author:
            return True
        return False


# Ad tracking statement

def AdTracking(request):
    return render(request, 'blog/adtracking.html', {'title': 'Ad Tracking'})

def Docs(request):
    return render(request, 'blog/docs.html', {'title': 'Documentation'})

def Pricing(request):
    return render(request, 'blog/pricing.html', {'title': 'Pricing'})

def Verification(request):
    return render(request, 'blog/verification.html', {'title': 'Verification'})

def Updates(request):
    return render(request, 'blog/updates.html', {'title': 'Site Updates'})

def Groups(request):
    return render(request, 'blog/groups.html', {'title': 'Groups'})

def VotingCenter(request):
    return render(request, 'blog/voting-center.html', {'title': 'Voting Center'})


# SHADOW - My livestream site for job shadowing

def shadow(request):
    return render(request, 'blog/shadow-home.html', {'title': 'Home'})

# Product Blog - The Blog for me to write

def blog(request):
    return render(request, 'blog/bloghome.html', {'title': 'Blog'})

def AI(request):
    return render(request, 'blog/AI.html', {'title': 'autodriver'})

##################################################
##################################################
# Publications
class PublicationsCreateView(LoginRequiredMixin, CreateView):
    model = Publications
    fields = ['title', 'category', 'PDF']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PublicationsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Publications
    success_url = '/'
    
    def test_func(self):
        pub = self.get_object()
        if self.request.user == pub.author:
            return True
        return False
##################################################
##################################################