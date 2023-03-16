from django import forms
from spotiview.models import Comment,Track, UserClass
from django.contrib.auth.models import User
from datetime import datetime

class TrackForm(forms.ModelForm):
    TrackName = forms.CharField(max_length=Track.MAX_LENGHT,help_text="Enter the name of track/song")
    slug = forms.CharField(widget=forms.HiddenInput(),required=False)
    likes = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    dislikes = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    listens = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    
    class Meta:
        model = Track
        fields = ('TrackName',)

class CommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=Comment.MAX_LENGTH)
    DateTime = forms.DateTimeField(widget=forms.HiddenInput())

    class Meta:
        model = Comment
        fields = ('comment',)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username','password',)


# class UserClassForm(forms.ModelForm):
#     class Meta:
#         model = UserClass
#         fields = ('',)



