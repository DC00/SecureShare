from django.db import models
# TODO: Need to use Reporter instead of SignUp
class Reporter(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    created_at = models.DateTimeField('date published')
    email = models.EmailField()

    def __str__(self):
       return "%s, %s" % (self.last_name, self.first_name)

class Report(models.Model):
    # See https://docs.djangoproject.com/en/1.8/ref/models/fields/ for explanations of model fields
    created_at = models.DateTimeField('date published')
    description = models.TextField()
    full_description = models.TextField()
    # TODO: make Report hold more than 1 file
    uploaded_files = models.FileField(default=None)
    is_private = models.BooleanField(default=True)
    
    # Foreign key for relationship to a Reporter. Many Reports to One Reporter
    reporter_it_belongs_to = models.ForeignKey(Reporter, blank=True, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
       return self.description

# Many Groups to Many Reporters
class Group(models.Model):
    name = models.CharField(max_length=120)
    members = models.ManyToManyField(Reporter, through='Membership')

    def __str__(self):
      return self.name

class Message(models.Model):
    created_at = models.DateTimeField('date published')
    content = models.TextField()
    is_private = models.BooleanField(default=False)
    group_it_belongs_to = models.ForeignKey(Group)

# Intermediate model for the many-to-many relationship between Groups and Reporters
class Membership(models.Model):
    reporter = models.ForeignKey(Reporter)
    group = models.ForeignKey(Group)





