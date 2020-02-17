from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.utils.html import mark_safe


class Meet(models.Model):
    meet_name = models.CharField(max_length=60)
    # provide list of state abbreviations here?
    state = models.CharField(max_length=2)
    start_date = models.DateField(auto_now_add=False)
    end_date = models.DateField(auto_now_add=False)
    meet_url = models.URLField(null=True)
    results_url = models.URLField(null=True)

    def __str__(self):
        return self.meet_name

class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length = 100)
    meet = models.ForeignKey(Meet,on_delete=models.SET_NULL, related_name='boards', null=True)

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()

class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add = True)
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.SET_NULL, null=True)
    starter = models.ForeignKey(User, related_name='topics', on_delete=models.SET_NULL, null=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject

class Post(models.Model):
    message= models.TextField(max_length = 4000)
    topic = models.ForeignKey(Topic, related_name= 'posts', on_delete=models.SET_NULL,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.SET_NULL, null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL)

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

    # def get_message_as_markdown(self):
    #     print("IN get_message_as_markdown",self.message)
    #     return mark_safe(markdown(self.message, safe_mode='escape'))


