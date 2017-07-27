from django import forms
from django.contrib.auth.models import User

from .models import Member


class MemberRegistrationForm(forms.Form):
    email = forms.EmailField()
    full_name = forms.CharField(max_length=200, label="Your name")
    password = forms.CharField(min_length=8, widget=forms.PasswordInput())
    confirm_password = forms.CharField(min_length=8,
                                       widget=forms.PasswordInput())

    def clean(self):
        """This is how you can manually hook into clean and do this yourself
        without a validator.
        """
        cleaned_data = super(MemberRegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')

        if confirm != password:
            raise forms.ValidationError(
                'Your passwords do not match!'
            )

        email = cleaned_data.get('email')
        user = User.objects.filter(email=email)

        if len(user):
            raise forms.ValidationError(
                'A user with this email already exists!'
            )


# this could also be a ModelForm
class MemberRegistrationModelForm(forms.ModelForm):
    password = forms.CharField(min_length=8, widget=forms.PasswordInput())
    confirm_password = forms.CharField(min_length=8,
                                       widget=forms.PasswordInput())

    class Meta:
        model = Member
        fields = ['email', 'name',]

    def clean(self):
        """This is how you can manually hook into clean and do this yourself
        without a validator.
        """
        cleaned_data = super(MemberRegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')

        if confirm != password:
            raise forms.ValidationError(
                'Your passwords do not match!'
            )
