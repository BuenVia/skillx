from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Client, CpdInfo

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['client_name']

class UserCreationFormWithClient(forms.ModelForm):
    # Add a client selection dropdown
    client = forms.ModelChoiceField(queryset=Client.objects.all())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def save(self, commit=True):
        # Save the User first
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # hash the password
        if commit:
            user.save()
            # Create the associated UserProfile
            UserProfile.objects.create(user=user, client=self.cleaned_data['client'])
        return user

class UserEditForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset=Client.objects.all())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def __init__(self, *args, **kwargs):
        user_instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        # Prepopulate client if editing
        if user_instance:
            try:
                self.fields['client'].initial = user_instance.userprofile.client
            except UserProfile.DoesNotExist:
                pass

    def save(self, commit=True):
        user = super().save(commit=commit)
        client = self.cleaned_data['client']

        # Update or create UserProfile
        UserProfile.objects.update_or_create(user=user, defaults={'client': client})

        return user
    
class CpdInfoForm(forms.ModelForm):
    class Meta:
        model = CpdInfo
        fields = [
            "title",
            "provider",
            "type_course",
            "description",
            "date_start",
            "date_complete",
            "duration",
            "grade",
        ]
