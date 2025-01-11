from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)  # Get the user by email
            if user.check_password(password):    # Check the password
                return user
        except User.DoesNotExist:
            return None
        return None
