from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):
    profile_picture = forms.ImageField(required=False)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.profile_picture = self.cleaned_data.get('profile_picture')
        user.save()
        return user