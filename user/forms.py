from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, Select, EmailInput

from home.models import UserProfile
from django import forms

class UserUpdateForm(UserChangeForm):
    class Meta:
        model =User
        fields =('username','email','first_name','last_name')
        widgets ={
            'username'  : TextInput(attrs={'class': 'input','placeholder':'username'}),
            'email'     : EmailInput(attrs={'class': 'input','placeholder':'email'}),
            'first_name': TextInput(attrs={'class': 'input','placeholder':'first_name'}),
            'last_name' : TextInput(attrs={'class': 'input','placeholder':'last_name'}),
        }

CITY = [
    ('Istanbul','Istanbul'),
    ('Ankara', 'Ankara'),
    ('Izmir', 'Izmir'),
]
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model= UserProfile
        fields =('phone','address','city','country','image')
        widgets ={
            'phone'         : TextInput(attrs={'class': 'input','placeholder':'username'}),
            'address'       : TextInput(attrs={'class': 'input','placeholder':'email'}),
            'city'          : Select(attrs={'class': 'input','placeholder':'city'},choices=CITY),
            'country'       : TextInput(attrs={'class': 'input','placeholder':'first_name'}),
            'image'         : TextInput(attrs={'class': 'input','placeholder':'last_name'}),
        }