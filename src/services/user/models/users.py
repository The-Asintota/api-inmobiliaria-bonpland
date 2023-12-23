from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, UserManager
)
from django.db import models
from .user_manager import UserCustomManager
import uuid


class Users(AbstractBaseUser, PermissionsMixin):
    """
    User model that extends from Django's AbstractBaseUser and PermissionsMixin.
    
    This model represents a user in the system.

    Attributes:
    - id (UUIDField) : The primary key for the user. (Automatically generated)
    - dni (CharField) : The user's DNI. Can be null.
    - full_name (CharField) : The user's full name. Can be null.
    - email (EmailField) : The user's email. Must be unique and not null.
    - phone_number (CharField) : The user's phone number. Can be null.
    - password (CharField) : The user's password. Not null.
    - is_staff (BooleanField) : Flag indicating if the user is a staff member.
    - is_superuser (BooleanField) : Flag indicating if the user is a superuser.
    - is_active (BooleanField) : Flag indicating if the user is active.
    - date_joined (DateTimeField) : The date and time the user joined. (Automatically set when the user is created)
    """

    id = models.UUIDField(
        db_column='id',
        default=uuid.uuid4,
        primary_key=True
    )
    dni = models.CharField(
        db_column='dni',
        max_length=8,
        unique=True,
        null=True,
        blank=True
    )
    full_name = models.CharField(
        db_column='full_name',
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )
    email = models.EmailField(
        db_column='email',
        max_length=100,
        unique=True,
        null=False,
        blank=False
    )
    phone_number = models.CharField(
        db_column='phone_number',
        max_length=16,
        unique=True,
        null=True,
        blank=True
    )
    password = models.CharField(
        db_column='password',
        max_length=128,
        null=False,
        blank=False
    )
    is_staff = models.BooleanField(
        db_column='is_staff',
        default=False,
        serialize=False
    )
    is_superuser = models.BooleanField(
        db_column="is_superuser",
        default=False,
        serialize=False
    )
    is_active = models.BooleanField(
        db_column='is_active',
        default=False
    )
    date_joined = models.DateTimeField(
        db_column='date_joined',
        auto_now_add=True,
        serialize=False
    )

    objects: UserCustomManager = UserCustomManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        db_table = 'user'
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.email
