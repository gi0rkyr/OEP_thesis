from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from main.models import Container, Containers_id

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class ContainerForm(ModelForm):
    class Meta:
        model = Container
        fields = ['student', 'name', 'container_id', 'pages']

        container_id = forms.ModelMultipleChoiceField(
        queryset=Containers_id.objects.all(),
        widget=forms.CheckboxSelectMultiple
        )