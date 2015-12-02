from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
fs = FileSystemStorage(location='/media/uploads')


# TODO: Need to use Reporter instead of SignUp

class Reporter(models.Model):
    user_name = models.CharField(max_length=120, null=True)
    password = models.CharField(max_length=120, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    email = models.EmailField()
    user = models.OneToOneField(User, blank=True, null=True)

    def __str__(self):
       return(self.user_name)
class Group(models.Model):
    name = models.CharField(max_length=120)
    members = models.ManyToManyField(Reporter, through='Membership')

    def __str__(self):
      return self.name


class Report(models.Model):
    # See https://docs.djangoproject.com/en/1.8/ref/models/fields/ for explanations of model fields
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    description = models.TextField()
    full_description = models.TextField()
    # TODO: make Report hold more than 1 file
    uploaded_files = models.FileField(upload_to='', default=None)
    groups_that_can_view = models.ManyToManyField(Group, blank=True, null=True, related_name='groups_to')
    reporters_that_can_view = models.ManyToManyField(Reporter, blank=True, null=True, related_name='reporter_to')
    is_private = models.BooleanField(default=False, blank=True)
    # Foreign key for relationship to a Reporter. Many Reports to One Reporter
    reporter_it_belongs_to = models.ForeignKey(Reporter, blank=True, null=True, on_delete=models.SET_NULL, related_name='belongs_to')
    
    def __str__(self):
       return self.description


class Folder(models.Model):
    name = models.CharField(max_length=120)
    contents = models.ManyToManyField(Report, blank=True, null=True)
    owner = models.ForeignKey(Reporter, blank=True, null=True, on_delete=models.SET_NULL)
    def __str__(self):
       return self.name
 
# Many Groups to Many Reporters   

class Message(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    content = models.TextField(default='defualt Message')
    is_private = models.BooleanField(default=False, blank=True)
    #group_it_belongs_to = models.ForeignKey(Group, default=None)
    send_to = models.ForeignKey(Reporter, blank=True, null=True, on_delete=models.SET_NULL, related_name='send_to')
    sender = models.ForeignKey(Reporter, blank=True, null=True, on_delete=models.SET_NULL, related_name='sender')
    def __str__(self):
      return self.content


# Intermediate model for the many-to-many relationship between Groups and Reporters
class Membership(models.Model):
    reporter = models.ForeignKey(Reporter)
    group = models.ForeignKey(Group)





