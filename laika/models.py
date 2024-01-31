from django.db import models
from django.contrib.auth.models import User

class LaikaProfileUser(models.Model):
    """
    LaikaProfileUser model represents a user profile in the Laika app.
    It extends the built-in User model with additional fields.
    """
    # One-to-one relationship with the User model. Each user can only have one LaikaProfileUser.
    laika_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="lpu")

    # Image field for storing user profile images. It uses 'laika_img/' as the upload directory.
    # The 'default' parameter specifies a default image if none is uploaded.
    image = models.ImageField(upload_to='laika_img/', default='laika_img/laika_logo_400.png', null=True, blank=True)

    # String representation of the model.
    def __str__(self):
        return f"{self.laika_user.username}'s Profile"

class Pet(models.Model):
    """
    Pet model represents a pet owned by a user in the Laika app.
    """
    # ForeignKey relationship to User. A user can have multiple pets.
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # CharFields for storing pet's name and species. Defaults are provided.
    pet_name = models.CharField(max_length=20, default="None")
    species = models.CharField(max_length=20, default="None")
    species_type = models.CharField(max_length=20, null=True, blank=True, default="None")
    
    #Additional fields for age, sex, weight, neutered status and spacial needs.
    age = models.IntegerField(null=True, blank=True)
    sex = models.CharField(max_length=10, choices=[('Female', 'Female'),('Male', 'Male'), ('Other', 'Other')], default='None')
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    neutered = models.BooleanField(default=False)
    special_needs = models.TextField(null=True, blank=True,default='None')
    
    # TextField for the description of the pet. It's optional.
    description = models.TextField(null=True, blank=True, default="None")

    # String representation of the model.
    def __str__(self):
        return f"{self.species}: {self.pet_name}"

class Post(models.Model):
    """
    Post model represents a post created by a user in the Laika app.
    """
    # ForeignKey relationship to User. A user can create multiple posts.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="laika_author")

    # Image field for storing post images with a default image specified.
    image = models.ImageField(upload_to='laika_img/', default='laika_img/laika_logo_400.png', null=True, blank=True)

    # CharField for the title of the post and TextField for its description.
    title = models.CharField(max_length=100)
    description = models.TextField()

    # Auto-generated fields for the dates when the post is created and last updated.
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    # Meta class to specify ordering of the posts - newest first.
    class Meta:
        ordering = ['-updated_at']

    # String representation of the model.
    def __str__(self):
        return f'{self.title}: {self.author.username}'


class LaikaComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(LaikaProfileUser, on_delete=models.CASCADE, related_name='laika_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.profile.laika_user.username}'
    

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name = "following", on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name = "followers", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"
    
    
class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender.username} to {self.recipient.username}'
