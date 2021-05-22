from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from userapp.utils import *
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name='profile',on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/',blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()
        if self.profile_pic:
            image = Image.open(self.profile_pic.path)
            image = make_square(image)
            image.save(self.profile_pic.path)

class Post(models.Model):
    user = models.ForeignKey(User,related_name='posts',on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=300,blank=True,null=True)
    picture = models.ImageField(upload_to='pics/')
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

    # rounding only for profile pictures is enough
    # def save(self, *args, **kwargs):
    #     super().save()
    #     if self.picture:
    #         image = Image.open(self.picture.path)
    #         image = make_square(image)
    #         image.save(self.picture.path)

class Comment(models.Model):
    post = models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='comments',on_delete=models.CASCADE)
    text = models.CharField(max_length=256)
    time_commented = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text