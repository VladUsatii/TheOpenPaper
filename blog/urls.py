from django.urls import path
from .views import (
    PostListView, 
    StoriesListView, 
    CuratedListView, 
    TrendingListView, 
    PostDetailView, 
    PostCreateView,
    PostUpdateView,
    PostDeleteView, 
    PostChangelogView,
    UserPostListView, 
    NewsListView, 
    PeopleListView,
    AdCreateView, 
    AdUpdateView, 
    AdDeleteView, 
    MarketListView, 
    UserMarketListView, 
    MarketDetailView, 
    MarketCreateView, 
    MarketUpdateView,
    MarketDeleteView,
    AdDetailView, 
    UserAdListView,
    LikeView, 
    CommentCreateView, 
    CommentDeleteView,
    PublicationsCreateView,
    PublicationsDeleteView
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('stories/', StoriesListView.as_view(), name='blog-stories'),
    path('curated/', CuratedListView.as_view(), name='blog-curated'),
    path('trending/', TrendingListView.as_view(), name='blog-trending'),
    path('market/', MarketListView.as_view(), name='market-home'), 
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('ad/<str:username>', UserAdListView.as_view(), name='user-ads'),
    path('market/user/<str:username>', UserMarketListView.as_view(), name='user-listings'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('ad/<int:pk>/', AdDetailView.as_view(), name='ad-detail'),
    path('market/<int:pk>/', MarketDetailView.as_view(), name='market-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('ad/new/', AdCreateView.as_view(), name='ad-create'),
    path('market/new/', MarketCreateView.as_view(), name='market-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('ad/<int:pk>/update/', AdUpdateView.as_view(), name='ad-update'),
    path('market/<int:pk>/update/', MarketUpdateView.as_view(), name='market-update'),
    path('post/<int:pk>/changelog', PostChangelogView.as_view(), name='post-changelog'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('ad/<int:pk>/delete/', AdDeleteView.as_view(), name='ad-delete'),
    path('market/<int:pk>/delete/', MarketDeleteView.as_view(), name='market-delete'),
    path('about/', views.about, name='blog-about'),
    path('business/', views.business, name='blog-business'),
    path('careers/', views.careers, name='blog-careers'),
    path('allcareers/', views.view_careers, name='careers-detail'),

    path('weather/', views.weather, name='blog-weather'),
    path('delete/<city_name>/', views.delete_city, name='delete_city'),
    path('legal/', views.legal, name='blog-legal'),
    path('events/', views.events, name='blog-events'),
    path('news/', NewsListView.as_view(), name='blog-news'),
    path('people/', views.PeopleListView, name='blog-people'),
    path('hashtags/', views.HashtagView, name='blog-hashtag'), 
    path('adtracking/', views.AdTracking, name='blog-adtracking'), 
    path('docs/', views.Docs, name='blog-docs'), 
    path('pricing/', views.Pricing, name='blog-pricing'), 
    path('verification/', views.Verification, name='blog-verification'), 
    path('updates/', views.Updates, name='product-updates'), 
    path('groups/', views.Groups, name='blog-groups'), 

    path('voting/', views.VotingCenter, name='voting-center'),

    path('like/<int:pk>', LikeView, name='like-post'), 

    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='add_comment'),
    path('post/<int:pk>/comment/delete/', CommentDeleteView.as_view(), name='comment-delete'),


    path('shadow/', views.shadow, name='shadow-home'),

    path('blog/', views.blog, name='blog-blog'),

    # ai
    path('autodriver/', views.AI, name='blog-AI'),

    # publications
    path('publications/', PublicationsCreateView.as_view(), name='pub-create'),
    path('publications/delete', PublicationsDeleteView.as_view(), name='pub-delete'),
]
