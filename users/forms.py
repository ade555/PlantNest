from django import forms
from allauth.account.forms import SignupForm, LoginForm
from core.utils import DivErrorList

from .models import User


# form for the user to update their profile
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


# create a custom signup for that overrides the default form by django all auth
class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    phone_number = forms.CharField(max_length=20)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': 'First Name', 'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Last Name', 'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email', 'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password', 'class': 'form-control', 'id': 'password'})
        self.fields['username'].widget.attrs.update({'placeholder': 'Username', 'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'placeholder': 'phone number', 'class': 'form-control', 'type':'tel'})
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['phone_number'].required = True
        self.fields['username'].required = True

        # add a custom error class to display error messages
        self.error_class = DivErrorList

    # save the custom login form with the new fields 
    def save(self, request):
        user = super().save(request)
        if user:
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.save()
        return user

# create a custom login for that overrides the default form by django all auth
class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        # add a custom css class to the fields
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({'placeholder': 'Username', 'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password', 'class': 'form-control', 'id': 'password'})
        self.fields['remember'].widget.attrs.update({ 'class': 'form-check-input'})
        self.error_class = DivErrorList

class UserDeleteForm(forms.Form):
    """
    Simple form that provides a checkbox that signals deletion.
    """
    delete = forms.BooleanField(required=True)