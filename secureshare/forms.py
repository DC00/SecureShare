from django import forms
# from .models import Reporter

# class ReporterForm(forms.ModelForm):
#     class Meta:
#         model = SignUp
#         # formats the admin signup form. Corresponds to the SignUp model
#         fields = ['full_name', 'email']

#     # overriding the function clean_email for extra validation
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         email_base, provider = email.split("@")
#         domain, extension = provider.split('.')

#         # if not domain == 'UVA':
#         #     raise forms.ValidationError("Please make sure you use your UVA email")

#         if not extension == "edu":
#             raise forms.ValidationError("Please use a valid .edu email address")
#         return email

#     def clean_full_name(self):
#         full_name = self.cleaned_data.get('full_name')
#         # write validation code here like clean_email

#         return full_name