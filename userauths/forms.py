from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm
from django.forms import ImageField, FileInput

from userauths.models import User, Profile


class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Аты-жөніңіз"}))
    username = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Қолданушы атыңыз"}))
    phone = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Ұялы телефон нөмірі"}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={"placeholder": "Email адрес"}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": "Құпия сөз"}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": "Құпия сөзді растаңыз"}))

    class Meta:
        model = User
        fields = ['full_name', 'username', 'email',
                  'phone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "with-border"


class ProfileUpdateForm(forms.ModelForm):
    image = ImageField(widget=FileInput)

    class Meta:
        model = Profile
        fields = [
            'image',
            'full_name',
            'bio',
            'about',
            'phone',
            'gender',
            'country',
            'city',
            'state',
            'address',
            'working_at',
            'instagram',
            'whatsapp',
            'telegram',
        ]
        widgets = {
            'about': forms.Textarea(attrs={'rows': 3}),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, label='Email', widget=forms.EmailInput(
        attrs={'autocomplete': 'email'}))
