from django.urls import path
from spotiview import views

app_name = 'spotiview'

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('', views.IndexView.as_view(), name='index'),
    path('about/',views.AboutView.as_view(),name = 'about'),
    path('topsongs/',views.TopSongs.as_view(),name = 'topsongs'),
    path('addTrack/',views.AddTrackView.as_view(),name = 'add_track'),

]
