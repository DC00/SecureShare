from django.contrib import admin

# importing the SignUp models that we wrote
from .models import Reporter, Report, Message, Group, Membership, Folder

admin.site.register(Report)
admin.site.register(Reporter)
admin.site.register(Message)
admin.site.register(Group)
admin.site.register(Membership)
admin.site.register(Folder)