from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.



class UserClass(models.Model):
    UserID = models.IntegerField(unique=True,primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # 1 - 1 relationship between the Django's User model to allow
    # for authentication based access (also gives username,password, etc)
    
    def __str__(self):
        return str(self.UserID) + "ID with username: "  + self.user.username

class Track(models.Model):
    MAX_LENGHT = 200
    TrackID = models.IntegerField(unique=True,primary_key=True)
    SpotifyID = models.CharField(max_length=300)
    TrackName = models.CharField(max_length=MAX_LENGHT)
    album = models.CharField(max_length=MAX_LENGHT)
    artist = models.CharField(max_length=MAX_LENGHT)
    likes = models.IntegerField(default=0,blank=True)
    dislikes = models.IntegerField(default=0,blank=True)
    listens = models.IntegerField(default=0,blank=True)
    cover_imageURL = models.URLField(blank=True)
    trackURL  = models.URLField(blank=True)
    previewURL = models.URLField(blank=True)
    slug = models.SlugField()
    userLikes = models.ManyToManyField(User,related_name="user_likes")
    userDisLikes = models.ManyToManyField(User,related_name="user_dislikes")

    class Meta:
        verbose_name_plural = 'Tracks'

    def __str__(self):
        return self.TrackName + " by "  + self.artist
    
    def save(self,*args,**kwargs):
        self.slug = slugify(self.TrackName)
        super(Track,self).save(*args,**kwargs)

    def get_user_likes(self):
        return "\n".join([user.username for user in self.userLikes.all()])
    
    def get_user_dislikes(self):
        return "\n".join([user.username for user in self.userDisLikes.all()])
    
    
        
    @property
    def commentCount(self):
        querySet = Comment.objects.all().filter(TrackID = self.TrackID)
        commentCount = querySet.count()
        return commentCount





class Comment(models.Model):
    MAX_LENGTH = 200
    TrackID = models.ForeignKey(Track, on_delete=models.CASCADE)
    UserID = models.ForeignKey(UserClass, on_delete=models.CASCADE)
    CommentID = models.IntegerField(unique=True,primary_key=True)
    comment = models.CharField(max_length=MAX_LENGTH)
    DateTime = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.comment + " was published on " + str(self.DateTime)







    

