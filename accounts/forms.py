from django import forms
from .models import Account, UserProfile
# phone_number
class RegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(
    attrs= {
    'placeholder': 'Enter Password',
    'class': 'form-control'}
    ))

    confirm_password = forms.CharField(widget=forms.PasswordInput(
    attrs= {
    'placeholder': 'Confirm Password',
    'class': 'form-control'}
    ))

    class Meta:
        model = Account
        fields = ['first_name',
                   'last_name',
                   'email',
                   'password',
                   'city_location',
                   'phone_no',
                    ] 

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = "Enter First Name"
        self.fields['last_name'].widget.attrs['placeholder'] = "Enter Last Name"
        self.fields['phone_no'].widget.attrs['placeholder'] = "Enter Phone Number"
        self.fields['email'].widget.attrs['placeholder'] = "Enter Email Address"
        self.fields['city_location'].widget.attrs['placeholder'] = "Enter City Location"
    
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        cnf_password = cleaned_data.get('confirm_password')

        if password != cnf_password:
            raise forms.ValidationError(
                "Password Does Not Match"
            )
    
class UserForm(forms.ModelForm):
    """Form definition for MODELNAME."""

    class Meta:
        """Meta definition for MODELNAMEform."""

        model = Account
        fields = ('first_name', 'last_name', 'phone_no',)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('address_line1', 'address_line2', 'city', 'state', 'country', 'profile_pic',)
    
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        # self.fields['first_name'].widget.attrs['placeholder'] = "Enter First Name"
        # self.fields['last_name'].widget.attrs['placeholder'] = "Enter Last Name"
        # self.fields['phone_no'].widget.attrs['placeholder'] = "Enter Phone Number"
        # self.fields['email'].widget.attrs['placeholder'] = "Enter Email Address"
        # self.fields['city_location'].widget.attrs['placeholder'] = "Enter City Location"