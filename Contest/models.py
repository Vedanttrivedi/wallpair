from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from poll.models import Questions

# Register your models here.
class Contest(models.Model):
	author = models.ForeignKey(User,on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	date = models.DateTimeField(default=timezone.now)
	members = models.ManyToManyField(User,related_name="members")
	posts = models.ManyToManyField(Questions,related_name="posts")
	second = models.BooleanField(default=False)
	final = models.BooleanField(default=False)
	over = models.BooleanField(default=False)
	canjoin = models.BooleanField(default=True)
	notification = models.CharField(max_length=200,default=None)
	