from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Post, LaikaProfileUser, Pet, LaikaComment, Follow, User, Message
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from dj_proj.mixins import AuthorOrStaffRequiredMixin
from .custom_form import ProfileForm, PetForm, LaikaCommentForm


class AboutView(View):
    def get(self, request):
        return render(request, 'laika/about.html')
    

# Decorator to ensure that the user is logged in to access the view
@method_decorator(login_required, name='dispatch')
class PostListView(ListView):
    # List view for displaying posts
    model = Post
    template_name = 'laika/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Custom queryset to implement search functionality
        queryset = super().get_queryset()
        search_words = self.request.GET.get("search_words")
        search_field = self.request.GET.get("search_field")
        search_date = self.request.GET.get("search_date")

        # Filter by title or description based on user input
        if search_words:
            if search_field == "title":
                queryset = queryset.filter(title__icontains=search_words)
            elif search_field == "description":
                queryset = queryset.filter(description__icontains=search_words)

        # Filter by date if provided
        if search_date:
            queryset = queryset.filter(created_at__gte=search_date)

        return queryset


@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    # View for creating a new post
    model = Post
    fields = ['title', 'description', 'image']
    template_name = 'laika/post_create.html'
    success_url = reverse_lazy('laika-post-list')

    def form_valid(self, form):
        # Assign the current user as the author of the post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        # Handle file upload
        form = self.get_form()
        if "add_image" in request.FILES:
            form.files['image'] = request.FILES["add_image"]
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@method_decorator(login_required, name='dispatch')
class PostDetailView(DetailView):
    # Detailed view for a specific post
    model = Post
    template_name = "laika/post_detail.html"
    context_object_name = "post"


@method_decorator(login_required, name='dispatch')
class PostUpdateView(AuthorOrStaffRequiredMixin, UpdateView):
    # View for updating an existing post
    model = Post
    fields = ['title', 'description', 'image']
    template_name = "laika/post_update.html"

    def get_success_url(self):
        # Redirect to the post detail view after updating
        return reverse_lazy('laika-post-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        # Handle image update or removal
        if form.cleaned_data.get("remove_image", False):
            if form.instance.image:
                form.instance.image.delete()
            form.instance.image = None
        elif "replace_image" in self.request.FILES:
            form.instance.image = self.request.FILES["replace_image"]
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class PostDeleteView(AuthorOrStaffRequiredMixin, DeleteView):
    # View for deleting a post
    model = Post
    template_name = "laika/post_delete.html"
    success_url = reverse_lazy('laika-post-list')


@method_decorator(login_required, name = 'dispatch')
class LaikaProfileView(View):
    template_name = "laika/profile.html"
            
    def get(self, request):
        try:
            profile = LaikaProfileUser.objects.get(laika_user=request.user)
            pet = Pet.objects.get(owner=request.user)
            
            profile_form = ProfileForm(instance=profile)
            pet_form = PetForm(instance=pet)
        except (LaikaProfileUser.DoesNotExist, Pet.DoesNotExist):
            profile_form = ProfileForm()
            pet_form = PetForm()    
        
        return render(request, self.template_name, {"profile_form": profile_form, "pet_form": pet_form})
    
    def post(self, request):
        profile, create = LaikaProfileUser.objects.get_or_create(laika_user=request.user)
        pet, create = Pet.objects.get_or_create(owner=request.user)
        
        profile_form = ProfileForm(request.POST, request.FILES, instance = profile)
        pet_form = PetForm(request.POST, instance = pet)
        
        if profile_form.is_valid() and pet_form.is_valid():
            profile_form.save()
            pet_form.save()
            
            return redirect("laika-profile")  
        
        return render(request, self.template_name, {"profile_form": profile_form, "pet_form": pet_form})            

  
@method_decorator(login_required, name='dispatch')
class LaikaProfileListView(ListView):
    """ View for listing user profiles. """
    model = LaikaProfileUser
    template_name = 'laika/profile_list.html'
    context_object_name = 'profiles'


@method_decorator(login_required, name='dispatch')
class LaikaProfileDetailView(DetailView):
    model = LaikaProfileUser
    template_name = 'laika/profile_detail.html'
    context_object_name = 'profile'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object().laika_user  # Current user profile
        
        # Numbers of followers
        followers_count = Follow.objects.filter(followed=profile_user).count()
        context['followers_count'] = followers_count

        if self.request.user != profile_user:
            is_following = Follow.objects.filter(follower=self.request.user, followed=profile_user).exists()
            context['show_follow_button'] = not is_following
            context['show_unfollow_button'] = is_following

        context['comment_form'] = LaikaCommentForm()
        context['comments'] = LaikaComment.objects.filter(profile=self.get_object())
        return context
    
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Needed to obtain the current profile
        comment_form = LaikaCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.profile = self.object
            comment.save()
            return redirect('laika-profile-detail', pk=self.object.pk)
        else:
            # Render page with form mistakes
            return self.render_to_response(self.get_context_data(comment_form=comment_form))


@method_decorator(login_required, name='dispatch')
class LaikaProfileCreateView(CreateView):
    """ View for creating a new user profile. """
    model = LaikaProfileUser
    fields = ['image']
    template_name = 'laika/profile_create.html'
    success_url = reverse_lazy('laika-profile-list')

   
@method_decorator(login_required, name='dispatch')
class LaikaProfileUpdateView(UpdateView):
    """ View for updating a user profile. """
    model = LaikaProfileUser
    fields = ['image', 'pet_name', 'species', 'species_type', 'description']
    template_name = 'laika/profile_edit.html'

    def get_success_url(self):
        return reverse_lazy('profile-detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user


@method_decorator(login_required, name='dispatch')
class LaikaProfileDeleteView(DeleteView):
    """ View for deleting a user profile. """
    model = LaikaProfileUser
    template_name = 'laika/profile_delete.html'
    success_url = reverse_lazy('profile-list')

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user


class FollowUserView(View):
    @method_decorator(login_required)
    def get(self, request, user_id):
        user_to_follow = get_object_or_404(User, pk=user_id)
        Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
        return redirect('laika-profile-detail', pk=user_to_follow.lpu.id)


class UnfollowUserView(View):
    @method_decorator(login_required)
    def get(self, request, user_id):
        user_to_unfollow = get_object_or_404(User, pk=user_id)
        Follow.objects.filter(follower=request.user, followed=user_to_unfollow).delete()
        return redirect('laika-profile-detail', pk=user_to_unfollow.lpu.id)


class SendMessageView(CreateView):
    model = Message
    fields = ['content']  
    template_name = 'laika/send_message.html'

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.recipient = get_object_or_404(User, pk=self.kwargs['user_id'])
        return super().form_valid(form)

    def get_success_url(self):
        recipient_profile = get_object_or_404(LaikaProfileUser, laika_user=self.object.recipient)
        return reverse_lazy('laika-profile-detail', kwargs={'pk': recipient_profile.pk})


class InboxView(ListView):
    model = Message
    template_name = 'laika/inbox.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects.filter(recipient=self.request.user).order_by('-sent_at')















           
            
            
            
            