from django.contrib import admin
from spotiview.models import Comment,Track,UserClass

# Register your models here.

class TrackAdmin(admin.ModelAdmin):
    list_display = ('TrackID','SpotifyID','TrackName','album','artist','likes','dislikes','listens')

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('comment','DateTime')

admin.site.register(Track,TrackAdmin)
admin.site.register(Comment,CommentsAdmin)
admin.site.register(UserClass)
