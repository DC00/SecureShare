from django import forms
from .models import Reporter, Message, Report

class ReporterForm(forms.ModelForm):
    class Meta:
        model = Reporter
        # formats the admin signup form. Corresponds to the SignUp model
        fields = ['first_name','last_name', 'email']

    

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




