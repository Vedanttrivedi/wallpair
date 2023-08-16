from django.urls import path
from . import views
urlpatterns = [
path('',views.PollListView,name='poll-home'),
path('suggestions/',views.suggest,name='suggestions'),
path('letsdo/<pk>',views.letsdo,name="letsgo"),
path('showrepost/<pk>',views.showreposts,name='showrepost'),

path('topcharts/',views.explore,name='poll-explore'),
path('create/',views.PollCreateViewd,name='poll-create'),
path('votes/<int:pk>',views.vote,name='votes'),
path('comments/',views.com,name='com'),
path('user/<int:pk>',views.up,name='userspoll'),
path('pollinfo/<int:pk>/<string>',views.userlikes,name="userlikes"),
path('youtube/',views.ypolls,name='ypolls'),
path('ycreate/',views.YPollCreateView,name='ypoll-create'),
path('mycreate/',views.mypost,name='mypost-create'),
path('kicked/<int:pk>',views.kickpoller,name='kick-poller'),
path('polltagd/<int:pk>/',views.tages,name="poll-tags"),
path('update/<int:pk>',views.update,name='update'),
path('delete/',views.delete,name='delete'),
path('comupdate/<int:pk>',views.comupdate,name='comupdate'),
path('deletecom/',views.delcom,name='deletecom'),
path('votes1/',views.vote1,name='votes'),
#path('topcharts/',views.topcharts,name='topcharts'),
path('repcom/',views.repcom,name='repcom'),
path('likes1/',views.lik1,name='rwepcom'),
path('dlikes1/',views.dlik1,name='rsepcom'),
path('likes2/',views.lik2,name='qrepcom'),
path('dlikes2/',views.dlik2,name='reeepcom'),

path('random/',views.random,name='random'),

path('randomgame/<str:what>',views.randomgame,name='erandom'),
path('memes/',views.memers,name="memers"),
path('neke/<int:pk>',views.neke,name="neke"),

]