from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=35)

    def __str__(self):
        return self.name

class Song(models.Model):
    title = models.CharField(max_length=67)
    description = models.TextField(max_length=428)
    image=models.ImageField(upload_to='images/')
    song=models.FileField(upload_to='musics/')
    added_date=models.DateTimeField(auto_now_add=True)
    cat=models.ForeignKey(Category,on_delete=models.CASCADE)


    def __str__(self):
        return self.title


class Listen_Later(models.Model):
    music_id = models.CharField(max_length=1638)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    added_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.music_id