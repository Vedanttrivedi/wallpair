from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image


class Ninja(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    cut =  models.IntegerField(default=0)
class Questions(models.Model):
	poller = models.ForeignKey(User,on_delete=models.CASCADE)
	question = models.CharField(max_length=500)
	image1  = models.ImageField(default='index.jpg',upload_to='poll-pics')
	image2 = models.ImageField(default='index1.jpg',upload_to='poll-pics')
	typee = models.CharField(max_length=50,default='general')
	views = models.IntegerField(default=0)
	date_posted=models.DateTimeField(default=timezone.now)
	show = models.IntegerField(default=0)
	kick = models.IntegerField(default=0)
	iscontest = models.IntegerField(default=0)

	def __str__(self):
	    return f'{self.question}\t\t:\t\t{self.poller.username}'
	 
    
    
	    

class Apppolls(models.Model):
	question = models.ForeignKey(Questions,on_delete=models.CASCADE,default=None)
	image1  = models.TextField(default='lol')
	image2 = models.TextField(default='lol')
	channel1= models.TextField(default=None)
	channel2= models.TextField(default=None)
	subs1 = models.BigIntegerField(default=0)
	subs2 = models.BigIntegerField(default=0)
	views1 = models.BigIntegerField(default=0)
	views2 = models.BigIntegerField(default=0)
	likes1 = models.BigIntegerField(default=0)
	likes2 = models.BigIntegerField(default=0)
	plink1 = models.TextField(default=None,null=True)
	plink2 = models.TextField(default=None,null=True)


class Tags(models.Model):
	poll = models.ForeignKey(Questions,on_delete=models.CASCADE)
	users = models.ManyToManyField(User)
class Watch(models.Model):
	poll = models.ForeignKey(Questions,on_delete=models.CASCADE)
	users = models.ManyToManyField(User)




class Reviews(models.Model):
	pid =  models.ForeignKey(Questions,on_delete=models.CASCADE,default=None)
	uid=models.ForeignKey(User,on_delete=models.CASCADE,default=None)
	l1=models.IntegerField(default=0)
	dl1=models.IntegerField(default=0)
	l2=models.IntegerField(default=0)
	dl2=models.IntegerField(default=0)
	date_posted=models.DateTimeField(default=timezone.now)

	def __str__(self):
	    return f'{self.uid.username}\t\t:\t\t{self.pid.question}  '

class likes1(models.Model):
	poll = models.ForeignKey(Questions,on_delete=models.CASCADE)
	users = models.ManyToManyField(User)


	def __str__(self):
	    return f'{self.poll.question}'


class dlikes1(models.Model):
	poll = models.ForeignKey(Questions,on_delete=models.CASCADE)
	users = models.ManyToManyField(User)


	def __str__(self):
	    return f'{self.poll.question}'

class likes2(models.Model):
	poll = models.ForeignKey(Questions,on_delete=models.CASCADE)
	users = models.ManyToManyField(User)

	def __str__(self):
	    return f'{self.poll.question}'


class dlikes2(models.Model):
	poll = models.ForeignKey(Questions,on_delete=models.CASCADE)
	users = models.ManyToManyField(User)


	def __str__(self):
	    return f'{self.poll.question}'

class Comments(models.Model):
	author = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
	question = models.ForeignKey(Questions,on_delete=models.CASCADE,default=None)
	content = models.TextField()
	parent = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE)
	date_posted=models.DateTimeField(default=timezone.now)

	def __str__(self):
	    return f'by :{self.author.username}\t\t :\t\t{self.content} ,on :{self.question.question}'



class YouPoll(models.Model):
    poller = models.ForeignKey(User,on_delete=models.CASCADE)
    question = models.CharField(max_length=500)


def __str__(self):
    return f'{self.question}\t\t:\t\t{self.poller.username}'
    
    
class Collab(models.Model):
	poller = models.ForeignKey(User,on_delete=models.CASCADE)
	question = models.CharField(max_length=500)
	image1  = models.ImageField(default='index.jpg',upload_to='poll-pics')
	image2 = models.ImageField(default='index1.jpg',upload_to='poll-pics')
	date_posted=models.DateTimeField(default=timezone.now)
	other = models.ForeignKey(User,on_delete=models.CASCADE,related_name="other")
	typee= models.IntegerField(default=0)
	
