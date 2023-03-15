from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.views import View
import requests
from base64 import b64encode
from spotify_review_project import settings
import json
from spotiview.forms import UserForm,TrackForm,CommentForm
from spotiview.models import UserClass,Track,Comment
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


# Create your views here.

class IndexView(View):
    def get(self,request):
        return render(request,'spotiview/index.html')
    

class AboutView(View):
        def get(self,request):
            return render(request,'spotiview/about.html')
        
class TopSongs(View):
        def get(self,request):
            context_dic = {}
            # top_tracks = Track.objects.all().order_by('-listens')[:7]
            top_tracks = Track.objects.all()
            context_dic["tracks"] = top_tracks
            for track in top_tracks:
                querySet = Comment.objects.all().filter(TrackID = track.TrackID)
                commentCount = querySet.count()
                track.comments = commentCount
            context_dic["tracks"] = top_tracks
            return render(request,'spotiview/topsongs.html',context=context_dic)
        

class SpotifySearch():

    def get_access_token(self):
        """Get access token via client credentials"""
        EncodedClient = b64encode(bytes(f'{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}', 'utf-8'))
        clientAuth = EncodedClient.decode('utf-8')

        payload='grant_type=client_credentials'
        headers = {'Authorization': f'Basic {clientAuth}',
                   'Content-Type': 'application/x-www-form-urlencoded',}

        response = requests.request("POST", settings.SPOTIFY_TOKEN_URL, headers=headers, data=payload)
        return json.loads(response.text)["access_token"]
    

    def URLify(self,input):
        replacement = "%20"
        for i in range(len(input)):
            if(input[i] == ' '):
                input = input.replace(input[i],replacement)
        return input
    

    def api_search_request(self,userInput):
        urlified = self.URLify(userInput)
        SPOTIFY_SEARCH_URL = f"https://api.spotify.com/v1/search?q="+urlified+"&type=track"
        payload={}
        headers = {'Authorization': 'Bearer '+self.get_access_token()}
        response = requests.request("GET", SPOTIFY_SEARCH_URL, headers=headers, data=payload)
        jsonRES = json.loads(response.text)
        Artist = jsonRES["tracks"]["items"][0]["artists"][0]["name"]
        Album = jsonRES["tracks"]["items"][0]["album"]["name"]
        SpotifyID = jsonRES["tracks"]["items"][0]["id"]
        TrackName = jsonRES["tracks"]["items"][0]["name"]
        trackURL = jsonRES["tracks"]["items"][0]["external_urls"]["spotify"]
        previewURL = jsonRES["tracks"]["items"][0]["preview_url"]
        coverImageURL  = jsonRES["tracks"]["items"][0]["album"]["images"][0]["url"]      #640 x 640 image for track cover
        return (SpotifyID,Album,Artist,TrackName,trackURL,previewURL,coverImageURL)
         
         
    
    
class AddTrackView(View):
    def get(self,request):
          form = TrackForm()
          return render(request,'spotiview/add_track.html',{'form':form})
    def post(self,request):
        form = TrackForm(request.POST)
        if form.is_valid():
            try:
                track = form.save(commit=False)
                (SpotifyID,Album,Artist,NewName,trackURL,previewURL,coverImageURL) = SpotifySearch().api_search_request(track.TrackName)
                querySet = Track.objects.get(SpotifyID = SpotifyID)
                return redirect(reverse('spotiview:index'))
            except (ObjectDoesNotExist,Track.DoesNotExist) as error:
                track.likes = 0
                track.listens = 0
                track.dislikes = 0
                track.SpotifyID = SpotifyID
                track.album = Album
                track.artist = Artist
                track.TrackName = NewName
                track.cover_imageURL = coverImageURL
                track.trackURL = trackURL
                track.previewURL = previewURL
                track.save()
                return redirect(reverse('spotiview:index'))

        else:
            print(form.errors)
        return render(request,'spotiview/add_track.html',{'form':form})



class ListenOnSpotify(View):
    def get(self,request):
        trackIdentity = request.GET.get("trackID")
        currentTrack = get_object_or_404(Track,TrackID=trackIdentity)
        if currentTrack != None:
            currentTrack.listens = currentTrack.listens + 1
            currentTrack.save()
            return redirect(currentTrack.trackURL)
        
        return redirect(reverse('spotiview:topsongs'))
    



class LikeTrackView(View):
    #@method_decorator(login_required)
    def get(self,request):
        trackIdentity = request.GET['trackID']
        try:
            currentTrack = get_object_or_404(Track,TrackID=trackIdentity)
        except Track.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        currentTrack.likes = currentTrack.likes + 1
        currentTrack.save()
        return HttpResponse(currentTrack.likes)

    

class DeincrementLikeCount(View):
    #@method_decorator(login_required)
    def get(self,request):
        trackIdentity = request.GET['trackID']
        try:
            currentTrack = get_object_or_404(Track,TrackID=trackIdentity)
        except Track.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        currentTrack.likes = currentTrack.likes - 1
        currentTrack.save()
        return HttpResponse(currentTrack.likes)
    



class DisLikeTrackView(View):
    #@method_decorator(login_required)
    def get(self,request):
        trackIdentity = request.GET['trackID']
        try:
            currentTrack = get_object_or_404(Track,TrackID=trackIdentity)
        except Track.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        currentTrack.dislikes = currentTrack.dislikes + 1
        currentTrack.save()
        return HttpResponse(currentTrack.dislikes)

    

class DeincrementDislikeCount(View):
    #@method_decorator(login_required)
    def get(self,request):
        trackIdentity = request.GET['trackID']
        try:
            currentTrack = get_object_or_404(Track,TrackID=trackIdentity)
        except Track.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        currentTrack.dislikes = currentTrack.dislikes - 1
        currentTrack.save()
        return HttpResponse(currentTrack.dislikes)




          



