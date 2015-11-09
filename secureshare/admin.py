from django.contrib import admin

# importing the SignUp models that we wrote
from .forms import SignUpForm
from .models import SignUp

class SignUpAdmin(admin.ModelAdmin):
    list_display = ["__str__", "timestamp", "updated"]
    form = SignUpForm
    # class Meta:
    #     model = SignUp

# Formats the page at localhost:8000/admin
admin.site.register(SignUp, SignUpAdmin)
