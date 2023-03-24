from django.test import TestCase, SimpleTestCase, Client
from django.shortcuts import get_object_or_404
from spotiview.models import Track,UserClass,Comment
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from spotiview.forms import TrackForm, UserForm, CommentForm,UserClassForm
from spotiview.views import IndexView, AboutView, TopSongs,SpotifySearch,AddTrackView,ListenOnSpotify,LikeTrackView,DeincrementLikeCount,DisLikeTrackView,DeincrementDislikeCount,LoginView,LogoutView,RegisterView,ShowTrackView,ProfileView
# Create your tests here.

#Tests For Urls Here
class TestUrls(SimpleTestCase):
    def test_index_url_resolves(self):
        url = reverse('spotiview:index')
        self.assertEquals(resolve(url).func.view_class,IndexView)

    def test_about_url_resolves(self):
        url = reverse('spotiview:about')
        self.assertEquals(resolve(url).func.view_class,AboutView)

    def test_topsongs_url_resolves(self):
        url = reverse('spotiview:topsongs')
        self.assertEquals(resolve(url).func.view_class,TopSongs)

    def test_add_track_url_resolves(self):
        url = reverse('spotiview:add_track')
        self.assertEquals(resolve(url).func.view_class, AddTrackView)

    def test_chosen_song_url_resolves(self):
        url = reverse('spotiview:show_track', args= ['some-slug'])
        self.assertEquals(resolve(url).func.view_class, ShowTrackView)

    def test_listen_on_spotify_url_resolves(self):
        url = reverse('spotiview:listenOnSpotify')
        self.assertEquals(resolve(url).func.view_class, ListenOnSpotify)

    def test_like_track_url_resolves(self):
        url = reverse('spotiview:like_track')
        self.assertEquals(resolve(url).func.view_class, LikeTrackView)

    def test_unlike_track_url_resolves(self):
        url = reverse('spotiview:unlike_track')
        self.assertEquals(resolve(url).func.view_class, DeincrementLikeCount)
    
    def test_dislike_track_url_resolves(self):
        url = reverse('spotiview:dislike_track')
        self.assertEquals(resolve(url).func.view_class,DisLikeTrackView)

    def test_unslike_track_url_resolves(self):
        url = reverse('spotiview:undislike_track')
        self.assertEquals(resolve(url).func.view_class, DeincrementDislikeCount)

    def test_unslike_track_url_resolves(self):
        url = reverse('spotiview:profile', args=['some_user'])
        self.assertEquals(resolve(url).func.view_class, ProfileView)


#Tests For Views Here

#----Index View Test ----#
class IndexViewTests(TestCase):
    def test_index_view_GET(self):
        response = self.client.get(reverse('spotiview:index'))
        #Checking the response return code, and what page contains
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Spotiview is a web application")
        self.assertTemplateUsed(response,'spotiview/index.html')
        
#----About View Test----#
class AboutViewTests(TestCase):
    def test_about_view_GET(self):
        response = self.client.get(reverse('spotiview:about'))
        #Checking the response return code, and what page contains
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "About Our Application")
        self.assertTemplateUsed(response,'spotiview/about.html')

#----View Tests----#
class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('spotiview:topsongs')
        self.url_add = reverse('spotiview:add_track')
        self.url_show_track = reverse('spotiview:show_track', args=['some-slug'])
        self.url_like_track = reverse('spotiview:like_track')
        self.track1 = Track.objects.create(
            TrackID = 1,
            TrackName = "some_track",
            likes=0,
            dislikes=0,
            listens=0,
            artist="some_artist",
            album = "some_album"
        )
#TopSongs View Test
    def test_topsongs_GET(self):
        response = self.client.get(self.url)

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'spotiview/topsongs.html')
#AddTrack View Tests
    def test_add_track_GET(self):
        response = self.client.get(self.url_add)

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'spotiview/add_track.html')

    def test_add_track_POST(self):
        response = self.client.post(self.url_add,args = [self.track1])

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'spotiview/add_track.html')
#LikeTrack View Test
    def test_like_track_GET(self):
        response = self.client.get(self.url_like_track,{
            'trackID' : 1,
            'likes' :0
        })

        self.assertEquals(response.status_code,302)
        #self.assertEquals(self.track1.likes,1)

#ShowTrack View Test
    def test_show_track_GET(self):
        response = self.client.get(self.url_show_track)
        
        self.assertEquals(response.status_code, 302)
    def test_show_track_POST(self):
        pass

#Tests For Models Here

#----Track Model Test ----#
class TrackMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        track = Track(TrackID=1, listens=-1, likes=0)
        track.save()
        self.assertEqual((track.listens >= 0), True)

    def test_ensure_likes_are_positive(self):
        track = Track(TrackID=1, listens=0, likes=-1)
        track.save()
        self.assertEqual((track.likes >= 0), True)

    def test_ensure_dislikes_are_positive(self):
        track = Track(TrackID=1, listens=0, dislikes=-1)
        track.save()
        self.assertEqual((track.dislikes >= 0), True)

    def test_slug_line_creation(self):
        track = Track(TrackName='Random Track String')
        track.save()
        self.assertEqual(track.slug, 'random-track-string')
    
    def test_comment_count_works(self):
        track = Track(TrackID = 1,
                      likes = 0,
                      listens = 0,
                      dislikes = 0,
                     )
        track.save()
        user = User()
        user.save()
        userN = UserClass(UserID=1,user = user)
        userN.save()
        comment = Comment(CommentID = 1,TrackID = track,UserID = userN, comment = "some comment here")
        comment.save()
        self.assertEqual(track.commentCount,1)
        

#----Comment Model Test----#
class CommentMethodTest(TestCase):
    def test_ensure_comment_exist(self):
        track = Track(TrackID = 1,
                      likes = 0,
                      listens = 0,
                      dislikes = 0,
                     )
        track.save()
        user = User()
        user.save()
        userN = UserClass(UserID=1,user = user)
        userN.save()
        comment = Comment(TrackID = track, UserID = userN,CommentID = 1,comment = "some comment here")
        comment.save()
        self.assertEqual((comment.comment),"some comment here")
    

#Tests For Forms Here
class TestForms(TestCase):
#----TrackForm Tests----#
    def test_track_form_with_valid_data(self):
        form = TrackForm(data = {
            'TrackName' : "some_track",
            'likes' : 0,
            'listens' : 0,
            'dislikes':0
        })

        self.assertTrue(form.is_valid())

    def test_track_form_with_no_data(self):
        form = TrackForm(data = {})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)
#----CommentForm Tests----#
    def test_comment_form_with_valid_data(self):
        form = CommentForm(data = {
            'comment' : "some comment",
            'TrackID' : 1,
            'UserID' : 1
            })
            
        self.assertTrue(form.is_valid())

    def test_comment_form_fills_userId_trackId_automatically(self):
        form = CommentForm(data = {
            'comment':"some comment"
        })

        self.assertTrue(form.is_valid())

    def test_comment_form_with_no_data(self):
        form = CommentForm(data = {})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
#----UserForm Tests----#
    def test_user_form_with_valid_data(self):
        form = UserForm(data = {
            'username' : "some_user",
            'password' : "my_password1"
        })
        self.assertTrue(form.is_valid())

    def test_user_form_with_no_data(self):
        form = UserForm(data = {})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),2)
#----UserClassForm Tests----#
    def test_user_class_form_with_valid_data(self):
        form = UserClassForm(data = {
            'profile_image' : "some_image.jpg"
        })
        self.assertTrue(form.is_valid())

    def test_user_class_form_not_require_image(self):
        form = UserClassForm(data = {})

        self.assertTrue(form.is_valid())


        
    
