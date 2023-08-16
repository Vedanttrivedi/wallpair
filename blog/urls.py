from django.urls import path
from . import views
urlpatterns = [
    path('', views.PostListView.as_view(),name='blog-home'),
    path('user/<str:username>/',views.UserPostListView.as_view(),name='blogers'),
    path('post/<int:pk>',views.PostDetailView.as_view(),name='blog-post'),
    path('post/new/',views.PostCreateView.as_view(),name='new-post'),
    path('post/<int:pk>/update',views.PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete',views.PostDeleteView.as_view(),name='post-delete'),
    path('post/new/blog-home',views.timepass,name='abcd'),
    path('about/',views.about,name='blog-about'),
    path('myroute/',views.myroute,name='mys'),
   
]