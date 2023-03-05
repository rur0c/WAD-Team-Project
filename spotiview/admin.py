from django.contrib import admin
from spotiview.models import Comment,Track,UserClass

# Register your models here.

class TrackAdmin(admin.ModelAdmin):
    list_display = ('TrackID','SpotifyID','TrackName','album','artist','likes','dislikes','listens')

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('comment','DateTime')

class UserClassAdmin(admin.ModelAdmin):
    list_display = ('UserID','user')

admin.site.register(Track,TrackAdmin)
admin.site.register(UserClass,UserClassAdmin)
admin.site.register(Comment,CommentsAdmin)