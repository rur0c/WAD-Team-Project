from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.utils import timezone

# Create your models here.



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
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Tracks'

    def __str__(self):
        return self.TrackName + " by "  + self.artist
    
    def save(self,*args,**kwargs):
        if self.listens<0:
            self.listens = 0
        elif self.likes<0:
            self.likes = 0
        elif self.dislikes <0:
            self.dislikes =0
        self.slug = slugify(self.TrackName)
        super(Track,self).save(*args,**kwargs)

    @property
    def commentCount(self):
        querySet = Comment.objects.all().filter(TrackID = self.TrackID)
        commentCount = querySet.count()
        return commentCount




class UserClass(models.Model):
    UserID = models.IntegerField(unique=True,primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # 1 - 1 relationship between the Django's User model to allow
    # for authentication based access (also gives username,password, etc)
    userLikes = models.ManyToManyField(Track,related_name="user_likes")
    userDisLikes = models.ManyToManyField(Track,related_name="user_dislikes")
    profile_image = models.ImageField(upload_to='profile_pictures',blank=True)
    
    def __str__(self):
        return self.user.username
    


    def get_user_likes(self):
        return "\n".join([track.TrackName for track in self.userLikes.all()])
    
    def get_user_dislikes(self):
        return "\n".join([track.TrackName for track in self.userDisLikes.all()])
    




class Comment(models.Model):
    MAX_LENGTH = 200
    CommentID = models.IntegerField(unique=True,primary_key=True,auto_created=True)
    TrackID = models.ForeignKey(Track, on_delete=models.CASCADE,auto_created=True)
    UserID = models.ForeignKey(UserClass, on_delete=models.CASCADE)
    comment = models.TextField(max_length=MAX_LENGTH)
    DateTime = models.DateTimeField(default=timezone.now)
    class Meta:
        verbose_name_plural = 'comments'

    def __str__(self):
        return self.comment + " was published on " + str(self.DateTime)
    


def create_concrete_profile(sender,instance,created,**kwargs):
    if created:
        newProfile = UserClass(user=instance)
        newProfile.save()

    
post_save.connect(create_concrete_profile,sender = User)









    

