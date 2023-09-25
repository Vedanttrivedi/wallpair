"""root URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from users import views as users_views
from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.conf import  settings
from django.conf.urls.static import static
from blog import views as dviews
from poll import views as pviews

urlpatterns = [
    path('con/',include('Contest.urls')),
    path('nooneadmin/', admin.site.urls),
    path('team/',dviews.team,name="team"),
    path('send/',users_views.send,name="sends"),
    path('recieved/',users_views.recieved,name="recieved"),
    path('tandc/',dviews.tandc,name="tandc"),
    path('settings/',users_views.settings,name="settings"),
    path('collab/',users_views.collab,name="collab"),
    path('acceptcollab/<id>',users_views.acceptcollab,name="acceptcollab"),
    path('removecollab/<id>',users_views.removecollab,name="scollab"),

    path('mycollab/',users_views.showcollab,name="mycollab"),
    path('nice/',pviews.pcollabs,name="pcollab"),
    path('find/',users_views.see,name="find"),
    path('showsave/',users_views.showsave,name="showsave"),
    path('repost/<pk>', pviews.repost,name="repost"),
    path('savepost/<pk>',users_views.savepost,name="savepost"),

    path('unsavepost/<pk>',users_views.unsavepost,name="unsavepost"),
    path('following/<username>',users_views.followinguser,name="following"),
    path('follwer/<username>',users_views.follwersuser,name="follower"),

    path('profilep/',users_views.updateuser,name="updateuser"),

    path('account/',users_views.updateaccount,name="updateaccount"),
    path('addme/<username>',users_views.addme,name="addme"),

    path('removeme/<username>',users_views.removeme,name="removeme"),

    path('removeme1/<username>',users_views.removeme1,name="removeme1"),

    path('follow/<pk>',users_views.follow,name="follow"),
    path('requestuser/',users_views.requestusers,name="requestusers"),
    path('catuser/<slug:typee>/<slug:username>',users_views.catuser,name='catuser'),
    path('categorie/<string>',pviews.cat,name='catp'),
    path('categorie1/<string>',pviews.cate,name='cate'),
    path('activate/<uidb64>/<token>',users_views.Verify.as_view(),name="activate"),
    path('polltaged/<int:pk>/',users_views.usertags,name="polltags"),
    path('user/<int:pk>',users_views.info,name='uinfo'),
    path('userlinks/',users_views.userlinks,name='userlinks'),
    path('userlinks1/',users_views.userlinks1,name='hello1'),
    path('search/',users_views.search,name='search'),
    path('about/',dviews.about,name='blog-about'),
    path('register/',users_views.signup,name='users_register'),
    path('profile/',users_views.profile,name='profile'),
    path('',include('poll.urls')),
    #path('bpost/',include('blog.urls')),
    path('login/',users_views.check,name='login'),
    #path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
      path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

