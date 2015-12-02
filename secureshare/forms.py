from django import forms
from .models import Reporter, Message, Report, Group, Folder

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

class ReportForm(forms.Form):
    description = forms.CharField(label='description:')
    full_description = forms.CharField(label='full_description:')
    is_private = forms.BooleanField(label='make_private:')
    uploaded_files = forms.FileField(label='Attached Files:')
    Reporter_choices = [[x.id, x.user_name] for x in Reporter.objects.all()]
    Select_Users= forms.MultipleChoiceField(label='Select Users', choices=Reporter_choices, widget=forms.CheckboxSelectMultiple(), required=False)
    Group_choices = [[y.id, y.name] for y in Group.objects.all()]
    Select_Groups= forms.MultipleChoiceField(label='Select Groups', choices=Group_choices, widget=forms.CheckboxSelectMultiple(), required=False)

class ReportForm2(forms.ModelForm):
    class Meta:
        model = Report
        # formats the message form. Corresponds to the SignUp model
        fields = ['description','full_description','is_private', 'uploaded_files','groups_that_can_view','reporters_that_can_view']   

class GroupForm(forms.Form):
    name = forms.CharField(label='Group Name:')
    Reporter_choices = [[x.id, x.user_name] for x in Reporter.objects.all()]
    Select_Users= forms.MultipleChoiceField(choices=Reporter_choices, widget=forms.CheckboxSelectMultiple(), required=False)

class FolderForm(forms.Form):
    name = forms.CharField(label='Folder Name:')
    Report_choices = [[x.id, x.description] for x in Report.objects.all()]
    Select_Reports= forms.MultipleChoiceField(choices=Report_choices, widget=forms.CheckboxSelectMultiple(), required=False)

class FolderForm2(forms.ModelForm):
    class Meta:
        model = Folder
        # formats the message form. Corresponds to the SignUp model
        fields = ['name']


    # description = forms.CharField(label='Group Name:')
    # full_description = forms.CharField(label='Group Name:')
    # uploaded_files = forms.FileField(label='Attached Files:')
    # Reporter_choices = [[x.id, x.user_name] for x in Reporter.objects.all()]
    # Select_Users= forms.MultipleChoiceField(label='Select Users', choices=Reporter_choices, widget=forms.CheckboxSelectMultiple(), required=False)
    # Group_choices = [[y.id, y.user_name] for y in Group.objects.all()]
    # Select_Groups= forms.MultipleChoiceField(label='Select Groups', choices=Reporter_choices, widget=forms.CheckboxSelectMultiple(), required=False)