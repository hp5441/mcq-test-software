from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('valid email id was not inserted')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        if not email:
            raise ValueError('valid email id not entered')
        school, created = School.objects.get_or_create(name="PSBB")
        user = self.model(email=self.normalize_email(email), school=school)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_teacher(self, email, password, **extra_fields):
        if not email:
            raise ValueError('valid email id not entered')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.is_teacher = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class School(models.Model):

    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    """user model for both students and teachers with customised fields from django's base user model"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self) -> str:
        return self.email
