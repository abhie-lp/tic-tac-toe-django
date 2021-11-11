from django.forms import ModelForm, CharField, PasswordInput
from django.contrib.auth import get_user_model


class RegisterForm(ModelForm):
    password = CharField(widget=PasswordInput(), max_length=64)
    password2 = CharField(widget=PasswordInput(), max_length=64)

    class Meta:
        model = get_user_model()
        fields = "email", "username",
