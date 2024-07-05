from django import forms
from django.contrib.auth.models import User
from .models import User_info


class UserInfo(forms.ModelForm):
    class Meta:
        model = User_info
        fields = ('profile_pic','gender','address','phone')
        

class UserFLEname(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email')
