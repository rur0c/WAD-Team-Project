from django.contrib import admin
from spotiview.models import Comment,Track,UserClass

# Register your models here.

class TrackAdmin(admin.ModelAdmin):
    list_display = ('TrackID','SpotifyID','TrackName','album','artist','cover_imageURL','trackURL','previewURL','likes','dislikes','listens',)


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('comment','DateTime')

class UserClassAdmin(admin.ModelAdmin):
    list_display=('user','get_user_likes','get_user_dislikes')



admin.site.register(Track,TrackAdmin)
admin.site.register(Comment,CommentsAdmin)
admin.site.register(UserClass,UserClassAdmin)
