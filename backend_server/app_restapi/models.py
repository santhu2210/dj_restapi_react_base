from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserLogin(models.Model):
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField()


class UserProfile(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, blank=True)  
    email = models.CharField(max_length=140, blank=True)  
    telephone = models.CharField(max_length=20, blank=True)  
    

    def __str__(self):
        return 'Profile of user: {}'.format(self.user.username)


# class Room(models.Model):
# 	name = models.CharField(max_length=3000)
# 	description =  models.TextField(null=True, blank=True)
# 	created_at = models.DateTimeField(auto_now_add=True)
# 	created_by = models.ForeignKey(User, related_name='adding_person')	
# 	is_delete = models.BooleanField(default=False)

# 	def __str__(self):
# 		return self.name

# class Booking(models.Model):
# 	title = models.CharField(max_length=3000)
# 	description =  models.TextField(null=True, blank=True)
# 	date = models.DateField()
# 	start = models.TimeField()
# 	end = models.TimeField()
# 	room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='meeting_room')
# 	members = models.ManyToManyField(User,blank=True)
# 	created_at = models.DateTimeField(auto_now_add=True)
# 	created_by = models.ForeignKey(User, related_name='booking_person')	
# 	is_delete = models.BooleanField(default=False)	

# 	def __str__(self):
# 		return self.title


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()