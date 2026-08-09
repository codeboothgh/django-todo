from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
class LoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        return super().confirm_login_allowed(user)


class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2"
        ]