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
from django.utils import timezone
from django.http import HttpResponseRedirect



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
            try:
                currentUser = get_object_or_404(UserClass,user=request.user)
            except TypeError:
                context_dic["tracks"] = top_tracks
                return render(request,'spotiview/topsongs.html',context=context_dic)

            if currentUser != None:
                for track in top_tracks:
                    if (track in currentUser.userLikes.all()):
                        track.liked = True
                    if (track in currentUser.userDisLikes.all()):
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
        currentUser = get_object_or_404(UserClass,user=request.user)
        currentUser.userLikes.add(Track.objects.get(TrackID = trackIdentity))
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
        currentUser = get_object_or_404(UserClass,user=request.user)
        currentUser.userLikes.remove(Track.objects.get(TrackID = trackIdentity))
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
        currentUser = get_object_or_404(UserClass,user=request.user)
        currentUser.userDisLikes.add(Track.objects.get(TrackID = trackIdentity))
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
        currentUser = get_object_or_404(UserClass,user=request.user)
        currentUser.userDisLikes.remove(Track.objects.get(TrackID = trackIdentity))
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



class ChosenSongView(View):
    def post_detail(request, year, month, day, track):
        track = get_object_or_404(Track, slug=track,
                                    status='published',
                                    publish__year=year,
                                    publish__month=month,
                                    publish__day=day)

        # List of active comments for this post
        comments = track.comments.filter(active=True)

        new_comment = None

        if request.method == 'POST':
            # A comment was posted
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                # Create Comment object but don't save to database yet          
                new_comment = comment_form.save(commit=False)
                # Assign the current post to the comment
                new_comment.Track = Track
                # Save the comment to the database
                new_comment.save()
        else:
            comment_form = CommentForm()                   
        return render(request,
                    'spotiview/chosensong.html',
                    {'track': Track,
                    'comments': comments,
                    'new_comment': new_comment,
                    'comment_form': comment_form})


class ShowTrackView(View):
    model = Track
    template_name = "spotiview/chosensongs.html"
    slug_field = "slug"

    form = CommentForm
    @method_decorator(login_required)
    def get(self,request,**kwargs):
        context_dict = {}
        try:
            track_slug = kwargs['track_name_slug']
            track = Track.objects.get(slug = track_slug)
            track_comments = Comment.objects.all().filter(TrackID = track.TrackID)
            track_comments_count = Comment.objects.all().filter(TrackID=track.TrackID).count()
            currentUser = get_object_or_404(UserClass,user=request.user)
            if currentUser != None:
                if (track in currentUser.userLikes.all()):
                    track.liked = True
                if (track in currentUser.userDisLikes.all()):
                    track.disliked = True

            context_dict['track'] = track
            context_dict.update({
            'form': self.form,
            'track_comments': track_comments,
            'track_comments_count': track_comments_count,
        })
        except (Track.DoesNotExist,TypeError):
            context_dict['track'] = None
            return render(request,'spotiview/index.html')
        
        return render(request, 'spotiview/chosensongs.html', context=context_dict)
    @method_decorator(login_required)
    def post(self,request,**kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            try:
                track_slug = kwargs['track_name_slug']
                track = get_object_or_404(Track, slug = track_slug)
                user = get_object_or_404(UserClass, user = request.user)
                form.instance.user = request.user
                form.instance.TrackID = track
                form.instance.UserID = user
                form.save()
            except (Track.DoesNotExist,TypeError):
                return render(request,'spotiview/index.html')
            
            return HttpResponseRedirect(reverse('spotiview:show_track', args=(track_slug,)))



    

