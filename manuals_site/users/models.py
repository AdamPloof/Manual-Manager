from django.db import models
from django.contrib.auth.models import User
from manuals.models import Directory, Manual


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    manual_favorites = models.ManyToManyField(Manual, related_name='+', blank=True)
    directory_favorites = models.ManyToManyField(Directory, related_name='+', blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'
