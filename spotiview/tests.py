from django.test import TestCase
from spotiview.models import Track
from spotiview.models import Comment
# Create your tests here.

#Tests for Models here

#----Track Model test ----#
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




