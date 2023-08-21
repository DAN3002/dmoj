from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

class OnlyEmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
            return user
        except User.DoesNotExist:
            return None 
            