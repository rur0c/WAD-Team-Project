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
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User



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


            for track in top_tracks:
                if (request.user in track.userLikes.all()):
                    track.liked = True
                if (request.user in track.userDisLikes.all()):
                    track.disliked = True

            context_dic["tracks"] = top_tracks
            context_dic["user"] = request.user

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
    @method_decorator(login_required)
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
        currentTrack.userLikes.add(request.user)
        return HttpResponse(currentTrack.likes)

    

class DeincrementLikeCount(View):
    @method_decorator(login_required)
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
        currentTrack.userLikes.remove(request.user)
        return HttpResponse(currentTrack.likes)
    



class DisLikeTrackView(View):
    @method_decorator(login_required)
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
        currentTrack.userDisLikes.add(request.user)
        return HttpResponse(currentTrack.dislikes)

    

class DeincrementDislikeCount(View):
    @method_decorator(login_required)
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
        currentTrack.userDisLikes.remove(request.user)
        return HttpResponse(currentTrack.dislikes)




          

class RestrictedView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'spotiview/restricted.html')
    
class LoginView(View):
    def get(self,request):
        return render(request,'registration/login.html')
    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = UserClass.objects.get(username=username)
            if user.password == password:
                request.session['user_id'] = user.UserID
                return redirect(reverse('spotiview:index'))
            else:
                return redirect(reverse('register:login'))
        except (ObjectDoesNotExist,UserClass.DoesNotExist) as error:
            return redirect(reverse('register:login'))
    

class LogoutView(View):
    def get(self,request):
        try:
            del request.session['user_id']
        except KeyError:
            pass
        return redirect(reverse('spotiview:index'))
    

class RegisterView(View):
    def get(self,request):
        register_form = UserForm()
        return render(request,'registration/register.html',{'register_form':register_form})
    def post(self,request):
        register_form = UserForm(request.POST)
        if register_form.is_valid():
            try:
                user = register_form.save(commit=False)
                user.save()
                return redirect(reverse('register:login'))
            except (ObjectDoesNotExist,UserClass.DoesNotExist) as error:
                return redirect(reverse('register:login'))
        else:
            print(register_form.errors)
        return render(request,'registration/register.html',{'register_form':register_form})



