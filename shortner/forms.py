from django.db import models
from django import forms
from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.models import User

class ShortUrlForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

        widgets = {
            # telling Django your password field in the mode is a password input on the template
            'password': forms.PasswordInput() 
        }

    #making the password hashed by overiding the save() method
    def save(self, commit=True):
        user = super(ShortUrlForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user