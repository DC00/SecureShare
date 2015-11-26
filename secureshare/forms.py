from django import forms
from .models import Reporter, Message, Report

class ReporterForm(forms.ModelForm):
    class Meta:
        model = Reporter
        # formats the admin signup form. Corresponds to the SignUp model
        fields = ['user_name', 'password', 'email']

class ReporterForm2(forms.ModelForm):
    class Meta:
        model = Reporter
        # formats the admin signup form. Corresponds to the SignUp model
        fields = ['user_name', 'password']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        # formats the message form. Corresponds to the SignUp model
        fields = ['send_to','content', 'is_private']

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        # formats the message form. Corresponds to the SignUp model
        fields = ['description', 'full_description']




