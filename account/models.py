from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

#Admin Acount Manager
class AdminAccountManager(BaseUserManager):
    def create_user(self, email, username, contact, group, password=None):
        if not email:
            raise ValueError('Invalid')

        email = self.normalize_email(email)
        admin = self.model( email = email, username = username, contact = contact, group = group )
        admin.set_password(password)
        admin.save()

        return admin


#Admin Model
class AdminAccounts(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    contact = models.CharField(max_length=12)
    group = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AdminAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'contact', 'group']

    def __str__(self):
        return self.username
    