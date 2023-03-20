from django.urls import path
from spotiview import views

app_name = 'spotiview'

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('', views.IndexView.as_view(), name='index'),
    path('about/',views.AboutView.as_view(),name = 'about'),
    path('topsongs/',views.TopSongs.as_view(),name = 'topsongs'),
    path('addTrack/',views.AddTrackView.as_view(),name = 'add_track'),
    path('listenOnSpotify/',views.ListenOnSpotify.as_view(),name='listenOnSpotify'),
    path('like_track/', views.LikeTrackView.as_view(), name='like_track'),
    path('unlike_track/', views.DeincrementLikeCount.as_view(), name='unlike_track'),
    path('dislike_track/', views.DisLikeTrackView.as_view(), name='dislike_track'),
    path('undislike_track/', views.DeincrementDislikeCount.as_view(), name='undislike_track'),
    path('restricted/', views.RestrictedView.as_view(), name='restricted'),
    path('chosensong/', views.ChosenSongView.as_view(), name ='chosensong'),

]
