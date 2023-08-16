from django.urls import path
from . import views
urlpatterns = [
    path('',views.create,name="createcontest"),
    path('all/',views.allcontest,name="all the contest"),
    path('contest/<int:pk>',views.newcontest,name="onecontest"),
    path('joincontest/<int:pk>',views.joincontest,name="joincontest"),
    path('members/<int:pk>',views.members,name="membercontest"),
    path('removefromcontest/<conpk>/<pk>',views.removeFromContest,name="removeFromcontest")
    
]