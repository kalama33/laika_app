from django.contrib import admin
from .models import LaikaProfileUser, Pet, Post, LaikaComment, Follow

admin.site.register(LaikaProfileUser)
admin.site.register(Pet)
admin.site.register(Post)
admin.site.register(LaikaComment)
admin.site.register(Follow)