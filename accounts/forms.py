from django.forms import Form, ModelForm, CharField, PasswordInput
from django.contrib.auth import get_user_model


class LoginForm(Form):
    username = CharField(max_length=32)
    password = CharField(widget=PasswordInput(), max_length=64)


class RegisterForm(ModelForm):
    password = CharField(widget=PasswordInput(), max_length=64)
    password2 = CharField(widget=PasswordInput(), max_length=64)

    class Meta:
        model = get_user_model()
        fields = "email", "username",
