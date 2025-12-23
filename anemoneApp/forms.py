# anemoneApp/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class EmailAuthForm(AuthenticationForm):
    # This class inherits all the logic but allows us to customize.
    # We rename 'username' to 'email' in the template context.
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 🌟 Change the label for the username field to 'Email'
        self.fields['username'].label = 'Email' 
        
        # We assume the user is logging in with their email,
        # but the underlying field name must remain 'username' 
        # for the built-in view to work correctly.

class CustomSignupForm(forms.ModelForm):
    # 🌟 Fields must match your HTML 'name' attributes
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        # Only take 'username' and 'email' from the form for the User model
        fields = ('username', 'email') 

    # 🔑 Custom validation method
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # 1. Check if passwords match
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        # 2. You would add more password strength/validation here if needed
        # ...
        
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

from .models import Profile
from phonenumber_field.widgets import PhoneNumberPrefixWidget, RegionalPhoneNumberWidget
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field import formfields

class ProfileUpdateForm(forms.ModelForm):
    # Use the SplitPhoneNumberField so the PhoneNumberPrefixWidget (a MultiWidget)
    # is paired with the matching MultiValueField which will compress the
    # separate prefix and number into a single PhoneNumber object.
    phone_number = formfields.SplitPhoneNumberField(
        required=False,
        widget=PhoneNumberPrefixWidget(
            widgets=(formfields.PrefixChoiceField().widget, RegionalPhoneNumberWidget())
        ),
    )

    class Meta:
        model = Profile
        fields = ['image', 'phone_number', 'birthday']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'image': forms.FileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email'] 
        
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text=""