from django import forms
from .models import Pet, LaikaProfileUser, Post, LaikaComment


class ProfileForm(forms.ModelForm):
    class Meta:
        model = LaikaProfileUser
        fields = ['image']
        

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['pet_name', 'species', 'species_type', 'age', 'sex' , 'weight', 'neutered', 'special_needs' ,'description'] 


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'image']
        
class LaikaCommentForm(forms.ModelForm):
    class Meta:
        model = LaikaComment
        fields = ['content']