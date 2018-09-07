from __future__ import unicode_literals
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from datetime import datetime#
    
@python_2_unicode_compatible
class User(models.Model):
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True) #other wanted information
    profilePic = models.ImageField(upload_to="clients", null=True, blank=True)
    def __str__(self):
        return 'Client Name: %s %s' % (self.firstName, self.lastName)

@python_2_unicode_compatible
class Post(models.Model):
    when = datetime.now
    post = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return 'Posted by %s %s at %s' % (self.user.firstName, self.user.lastName, self.when)

@python_2_unicode_compatible
class Comment(models.Model):
    when = datetime.now
    comment = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return 'Posted by %s %s at %s' % (self.user.firstName, self.user.lastName, self.when)