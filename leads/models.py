from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

#below is my own custom User model
#remember to insert AUTH_USER_MODEL = 'leads.User' in settings.py file
class User(AbstractUser):
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User , on_delete = models.CASCADE)

    def __str__(self):
        return self.user.username


class Lead(models.Model):

    SOURCE_CHOICES = (
        ('Youtube','Youtube'),
        ('LinkedIn','LinkedIn'),
        ('Google','Google'),
    )

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    organization = models.ForeignKey(UserProfile,on_delete=models.CASCADE) 
    agent = models.ForeignKey("Agent",null=True,blank=True,on_delete=models.SET_NULL)
    category = models.ForeignKey("Category",related_name="leads",null=True,blank=True,on_delete=models.SET_NULL)
    description = models.TextField(null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    #profile_picture = models.ImageField(null=True, blank=True, upload_to="profile_pictures/")
    source = models.CharField(choices=SOURCE_CHOICES,max_length=100)
    special_files=models.FileField(blank=True,null=True) 
    
    
      
    def __str__(self):
        return self.first_name+" "+self.last_name


class Agent(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)  
    organization = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.email


class Category(models.Model):
    name = models.CharField(max_length = 30) #for example : New,Contacted,Converted,Unconverted
    organization = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    def __str__(self):
        return self.name


#this function is used to call the post_save signal in order to automatically create 
# a UserProfile object with the same user after the user is created in Users table
def post_user_created_signal(sender, instance,created,**kwargs):
    print(instance,created)
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_created_signal,sender=User)