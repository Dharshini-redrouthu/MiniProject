from django.contrib import admin
from .models import Story, StoryComment, StoryRating

admin.site.register(Story)
admin.site.register(StoryComment)
admin.site.register(StoryRating)
