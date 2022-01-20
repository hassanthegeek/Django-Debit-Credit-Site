from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms.fields import CharField


class UserRegisterationForm(UserCreationForm):
    email = forms.EmailField(max_length=50)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.PasswordInput()

    def clean_email(self):
        print('i am clean email.')
        print(self.cleaned_data)
        e = self.cleaned_data.get('email')
        return e

    def clean_password(self):
        print('i am clean password')
        print(self.cleaned_data)
        p = self.cleaned_data.get('password')
        return p


class AnagramForm(forms.Form):
    first = forms.CharField(max_length=50)
    second = forms.CharField(max_length=50)

    def clean_first(self):
        print('i am first clean')
        print(self.cleaned_data)
        return self.cleaned_data.get('first')

    def clean_second(self):
        print('i am second clean')
        print(self.cleaned_data)
        second = self.cleaned_data.get('second')
        if 'second' == second.lower():
            raise forms.ValidationError('You cannot copy us.')
        return self.cleaned_data.get('second')

    def clean(self):
        print('I am clean')
        print(self.cleaned_data)
        first = self.cleaned_data.get('first')
        second = self.cleaned_data.get('second')
        if first == second:
            raise forms.ValidationError('You are making us fool.')

        return super().clean()
