from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    """Model manager for UserProfile model"""
    def create_user(self, email, name, password=None):
        """Creates a new UserProfile"""
        if not email:
            raise ValueError("Users must have an email address.")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    types = (
        ('Customer', 'Customer'),
        ('Service provider', 'Service provider')
    )
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100, choices=types, default='Customer')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of user"""
        return self.name


class Service(models.Model):
    provider = models.ForeignKey(UserProfile, on_delete=models.CASCADE, limit_choices_to={'type': 'Service provider'})
    service = models.CharField(max_length=250)
    cost = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.service


class ServiceRequest(models.Model):
    customer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, limit_choices_to={'type': 'Customer'})
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status_t = [
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
        ("Completed", "Completed")
    ]
    status = models.CharField(max_length=15, choices=status_t, default='Pending')

    def __str__(self):
        return self.customer.name


class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    s_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE,
                                  limit_choices_to={'status__in': ['Accepted', 'Completed']})
    timestamp = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    def __str__(self):
        return self.comment
