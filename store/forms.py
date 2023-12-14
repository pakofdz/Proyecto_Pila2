from django.contrib.auth.forms import UserCreationForm
from  django.contrib.auth.models import User
from django import forms

class Registrar_usuario_email(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields['username'].label = 'Usuario'