from django.db import models
from django.contrib.auth.models import User
from poll.models import Questions,Collab
from PIL import Image
# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	image = models.ImageField(default="profile_pics/user.png",upload_to='profile_pics')
	bio = models.TextField(default='hey there i am using this blog site')
	link = models.TextField(null=True)
	typee  = models.IntegerField(default=0,null=True)
	following = models.ManyToManyField(User,related_name="follow")
	pref = models.IntegerField(default=0)
	pending = models.ManyToManyField(User,related_name="pending")
	clone = models.IntegerField(default=0)
	mysave = models.ManyToManyField(Questions,related_name="mysaved")
	#share = models.ManyToManyField(Collab,related_name="shar")
	#look = models.ManyToManyField(Collab,related_name="mysa")
	
    




	follwers = models.ManyToManyField(User,related_name="follwe")
	def __str__(self):
		return f'{self.user.username} Profile'
	def save(self,*args, **kwargs):
	    super().save(*args, **kwargs)
	    img = Image.open(self.image.path)
	    if img.height > 300 or img.width > 300:
	        #new_img = (300, 300)
	        #img.thumbnail(new_img)
	        img.save(self.image.path,format="JPEG",quality=50)



    
    

        
            
            
            

	
	
	
	    


