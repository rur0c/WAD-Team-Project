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
    comment = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'md-textarea form-control',
        'placeholder': 'Comment here ...',
        'rows': '2',
        }))    
    TrackID = forms.IntegerField(widget=forms.HiddenInput(),required=False)
    UserID = forms.IntegerField(widget=forms.HiddenInput(),required=False)
    
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



