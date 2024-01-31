from django.test import TestCase
from .models import LaikaProfileUser, Follow, LaikaComment, Message, Pet, Post
from django.contrib.auth.models import User

class LaikaProfileUserTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', password='12345')
        self.profile = LaikaProfileUser.objects.create(laika_user=self.user)

    def test_profile_creation(self):
        self.assertEqual(self.profile.laika_user, self.user)

    def test_profile_str(self):
        self.assertEqual(str(self.profile), f"{self.user.username}'s Profile")
        
        
class PetTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='petowner', password='12345')
        self.pet = Pet.objects.create(owner=self.user, pet_name='Buddy', species='Dog')

    def test_pet_creation(self):
        self.assertEqual(self.pet.owner, self.user)
        self.assertEqual(self.pet.pet_name, 'Buddy')

    def test_pet_str(self):
        self.assertEqual(str(self.pet), 'Dog: Buddy')
        
        
class PostTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='author', password='12345')
        self.post = Post.objects.create(author=self.user, title='First Post', description='A new post')

    def test_post_creation(self):
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.title, 'First Post')

    def test_post_str(self):
        self.assertEqual(str(self.post), 'First Post: author')
        
        
class LaikaCommentTests(TestCase):

    def setUp(self):
        self.author = User.objects.create(username='author', password='12345')
        self.commenter = User.objects.create(username='commenter', password='12345')
        self.profile = LaikaProfileUser.objects.create(laika_user=self.author)
        self.comment = LaikaComment.objects.create(author=self.commenter, profile=self.profile, content='Nice post!')

    def test_comment_creation(self):
        self.assertEqual(self.comment.author, self.commenter)
        self.assertEqual(self.comment.profile, self.profile)

    def test_comment_str(self):
        self.assertEqual(str(self.comment), 'Comment by commenter on author')
        
        
class FollowTests(TestCase):

    def setUp(self):
        self.follower = User.objects.create(username='follower', password='12345')
        self.followed = User.objects.create(username='followed', password='12345')
        self.follow = Follow.objects.create(follower=self.follower, followed=self.followed)

    def test_follow_creation(self):
        self.assertEqual(self.follow.follower, self.follower)
        self.assertEqual(self.follow.followed, self.followed)

    def test_follow_str(self):
        self.assertEqual(str(self.follow), 'follower follows followed')
        
        
class MessageTests(TestCase):

    def setUp(self):
        self.sender = User.objects.create(username='sender', password='12345')
        self.recipient = User.objects.create(username='recipient', password='12345')
        self.message = Message.objects.create(sender=self.sender, recipient=self.recipient, content='Hello!')

    def test_message_creation(self):
        self.assertEqual(self.message.sender, self.sender)
        self.assertEqual(self.message.recipient, self.recipient)

    def test_message_str(self):
        self.assertEqual(str(self.message), 'Message from sender to recipient')






