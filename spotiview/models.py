from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.

class Track(models.Model):
    MAX_LENGHT = 200
    TrackID = models.IntegerField(unique=True,primary_key=True)
    SpotifyID = models.CharField(unique=True,max_length=300)
    TrackName = models.CharField(max_length=MAX_LENGHT)
    album = models.CharField(max_length=MAX_LENGHT)
    artist = models.CharField(max_length=MAX_LENGHT)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    listens = models.IntegerField(default=0)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = 'Tracks'

    def __str__(self):
        return self.TrackName + " by "  + self.artist
    
    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(Track,self).save(*args,**kwargs)
    


class UserClass(models.Model):
    UserID = models.IntegerField(unique=True,primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # 1 - 1 relationship between the Django's User model to allow
    # for authentication based access (also gives username,password, etc)
    
    def __str__(self):
        return self.UserID + "ID with username: "  + self.user.username



class Comment(models.Model):
    TrackID = models.ForeignKey(Track, on_delete=models.CASCADE)
    UserID = models.ForeignKey(UserClass, on_delete=models.CASCADE)
    CommentID = models.IntegerField(unique=True,primary_key=True)
    comment = models.CharField(max_length=200)
    DateTime = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.comment + " was published on " + self.DateTime







    

