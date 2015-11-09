from django.db import models

class Report(models.Model):
    # See https://docs.djangoproject.com/en/1.8/ref/models/fields/ for explanations of model fields
    created_at = models.DateTimeField('date published')
    description = models.TextField()
    full_description = models.TextField()
    uploaded_files = models.FileField()

    def __str__(self):
        return self.description

class SignUp(models.Model):
    email = models.EmailField()
    full_name = models.CharField(max_length=120, blank=False, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.email
