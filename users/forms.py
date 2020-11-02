from django import forms
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib.auth import get_user_model
from django.utils.translation import gettext, gettext_lazy as _
#from ckeditor.widgets import CKEditorWidget


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    phone = PhoneNumberField(required=True, label='',
                            widget=forms.NumberInput(attrs={'placeholder': 'Phone: +234 8035873345'}))
    birth_date = forms.DateField(label='', widget=forms.DateInput(attrs={'placeholder': 'DOB: YYYY-MM-DD '}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password Confirmation'}))

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'phone', 'birth_date','phone', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class MyPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(MyPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))


class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(MyPasswordChangeForm, self).__init__(*args, **kwargs)

    old_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Old Password'}))
    new_password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}))
    new_password2 = forms.CharField(label='',
                                    widget=forms.PasswordInput(attrs={'placeholder': 'New Password Confirmation'}))


class ContactForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

    name = forms.CharField(max_length=50, label='', widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    user_email = forms.EmailField(max_length=50, label='', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    comment = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Comment'}))


class SubscriberForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SubscriberForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(max_length=50, label='', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))


class NewsletterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(NewsletterForm, self).__init__(*args, **kwargs)

    subject = forms.CharField(max_length=150, label='', widget=forms.TextInput(attrs={'placeholder': 'Subject'}))
    content = forms.FileField(label='', widget=forms.FileInput(attrs={'placeholder': 'Content'}))


class UserUpdaetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserUpdaetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    phone = PhoneNumberField(required=True, label='',
                            widget=forms.NumberInput(attrs={'placeholder': 'Phone: +234 8035873345'}))

    class Meta:
        model = get_user_model()
        fields = ['email', 'phone', 'first_name', 'last_name']
