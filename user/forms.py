from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'id': "your_name",
        'placeholder': "Your Name",
        "name": "your_name"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Password",
        "id": "your_pass",
        "name": "name"}))


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Password",
                                                                 'id': "pass",
                                                                 'name': 'pass'}))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Repeat your password",
                                                                  'id': "re_pass",
                                                                  'name': 'pass'}))

    terms_service = forms.BooleanField(widget=forms.CheckboxInput(attrs={"name": "agree-term",
                                                                         'id': "agree-term",
                                                                         "class": "agree-term"}))

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': "Username",
                                               'id': "name",
                                               'name': 'name'}),
            # 'first_name': forms.TextInput(attrs={'placeholder': "First name",
            #                                      'id': "name",
            #                                      'name': 'name'}),
            'email': forms.EmailInput(attrs={'placeholder': "Your email",
                                             'id': "email",
                                             'name': 'email'})
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('passwords don\'t match.')
        return cd['password2']


class PasswordResetConfirmForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Password",
                                                                 'id': "pass",
                                                                 'name': 'pass'}))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Repeat your password",
                                                                  'id': "re_pass",
                                                                  'name': 'pass'}))

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('passwords don\'t match.')
        return cd['password2']
