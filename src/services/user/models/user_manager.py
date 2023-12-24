from django.contrib.auth.models import UserManager, AbstractUser
from uuid import UUID


class UserCustomManager(UserManager):
    """
    Custom user manager where email is the unique identifiers for authentication
    instead of usernames.
    """

    def _create_user(self,
        pk: UUID = None,
        dni: str = None,
        full_name: str = None,
        email: str = None,
        phone_number: str = None,
        password: str = None,
        **extra_fields
    ) -> AbstractUser:
        user: AbstractUser = self.model(
            pk=pk,
            dni=dni,
            full_name=full_name,
            email=self.normalize_email(email),
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,
        pk: UUID = None,
        dni: str = None,
        full_name: str = None,
        email: str = None,
        phone_number: str = None,
        password: str = None,
        **extra_fields
    ) -> AbstractUser:
        """
        Create and save a User with the given email and password.

        Args:
        - pk (UUID, optional): User's unique identifier. Defaults to None.
        - dni (str, optional): User's DNI. Defaults to None.
        - full_name (str, optional): User's full name. Defaults to None.
        - email (str, optional): User's email. Defaults to None.
        - phone_number (str, optional): User's phone number. Defaults to None.
        - password (str, optional): User's password. Defaults to None.
        - **extra_fields: Additional fields to set on the user.

        Returns:
            User: The created user instance.
        """

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        return self._create_user(
            pk=pk,
            dni=dni,
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            password=password,
            **extra_fields
        )

    def create_superuser(self,
        pk: UUID = None,
        dni: str = None,
        full_name: str = None,
        email: str = None,
        phone_number: str = None,
        password: str = None,
        **extra_fields
    ) -> AbstractUser:
        """
        Create and save a SuperUser with the given email and password.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        elif extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        elif extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")
        return self._create_user(
            pk=pk,
            dni=dni,
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            password=password,
            **extra_fields
        )
