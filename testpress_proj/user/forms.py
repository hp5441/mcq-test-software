from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


class SignUpForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ['email', 'name', 'school', 'password1', 'password2']


class SignInForm(AuthenticationForm):

    class Meta:
        model = get_user_model()
        fields = ['email', 'password']
