from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager

from .common import ROLES


class CustomUserMenager(BaseUserManager):
    def create_user(self, username, email, password=None, user_role=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have an password')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        if user_role:
            user.role = user_role
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.role = 4
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    email = models.EmailField(max_length=255, unique=True)
    phone = models.PositiveIntegerField(unique=False, null=True, blank=True)

    is_active = models.BooleanField(_("Is active User"), default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    role = models.PositiveBigIntegerField(
        _("User role"), choices=ROLES, default=1)

    join_date = models.DateTimeField(
        _("User Join Date"),
        auto_now_add=True
    )
    last_login = models.DateTimeField(
        _("Last loggin Date"),
        auto_now_add=True
    )
    objects = CustomUserMenager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}' if self.first_name or self.last_name else f'{self.username}'

    def __str__(self) -> str:
        return str(self.full_name)
