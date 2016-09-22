from __future__ import unicode_literals

from django.db import models
from ..login_register.models import User

class Message(models.Model):
    message = models.CharField(max_length=255)
    user_to = models.ForeignKey(User, related_name='user_to')
    user_from = models.ForeignKey(User, related_name='user_from')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'messages'

class Comment(models.Model):
    comment = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    message = models.ForeignKey(Message)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'comments'
