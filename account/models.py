from __future__ import unicode_literals
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from datetime import datetime#
from tinymce import models as tinymce_models
import uuid
    
@python_2_unicode_compatible
class Employee(models.Model):
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True) #other wanted information
    profilePic = models.ImageField(upload_to="Profile Pictures", blank=True)
    def __str__(self):
        return 'Employee Name: %s %s' % (self.firstName, self.lastName)

@python_2_unicode_compatible
class Post(models.Model):
    when = models.CharField(max_length=200, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    post = models.CharField(max_length=10000)
    subject = models.CharField(max_length=1000)
    postId= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    status = models.CharField(max_length=200, default="Unresolved")
    def __str__(self):
        return 'Posted by %s %s at %s postId: %s' % (self.employee.firstName, self.employee.lastName, self.when, self.postId)

@python_2_unicode_compatible
class Comment(models.Model):
    when = models.CharField(max_length=200)
    comment = models.TextField(null=False, blank=False)
    commentId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    def __str__(self):
        return 'Posted by %s %s at %s' % (self.employee.firstName, self.employee.lastName, self.when)