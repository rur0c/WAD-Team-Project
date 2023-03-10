from django.urls import path
from spotiview import views

app_name = 'spotiview'

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('', views.IndexView.as_view(), name='index'),
    path('about/',views.AboutView.as_view(),name = 'about'),
    path('topsongs/',views.TopSongs.as_view(),name = 'topsongs'),
    path('addTrack/',views.AddTrackView.as_view(),name = 'add_track'),
    path('login/',views.LoginView.as_view(),name = 'login'),
    path('logout/',views.LogoutView.as_view(),name = 'logout'),
    path('register/',views.RegisterView.as_view(),name = 'register'),
]
