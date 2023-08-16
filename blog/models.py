from django.db import models
from django.contrib.auth.models import User
from poll.models import Collab
from django.utils import timezone
from django.urls import reverse
# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	dateposted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User,on_delete=models.CASCADE,default=None)

	def  get_absolute_url(self):
		return reverse('blog-post',kwargs={'pk':self.pk})
		
class Share(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    done = models.ManyToManyField(Collab,related_name="collab")
    pend= models.ManyToManyField(Collab,related_name="pendcol")
    def __str__(self):
        return f'{self.user.username} shares'
    
	
	



class Room(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    caption = models.CharField(max_length=500)
    
