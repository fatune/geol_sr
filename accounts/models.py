from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

class Token(models.Model):
    email = models.EmailField()
    uid = models.CharField(max_length=255)


class SrUserManager(BaseUserManager):

    def create_user(self, email):
        SrUser.objects.create(email=email)

    def create_superuser(self, email, password):
        self.create_user(email)

class SrUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(primary_key=True)
    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['email', 'height']

    objects = SrUserManager()

    @property
    def is_staff(self):
        return self.email == 'harry.percival@example.com'

    @property
    def is_active(self):
        return True
