from django.db import models
from django.contrib.auth.models import AbstractUser , BaseUserManager, PermissionsMixin

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
# Custom User Model
class CustomUser (AbstractUser , PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    address = street + city + state + postal_code + country
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'street', 'city', 'state', 'postal_code', 'country']

    # Override groups and user_permissions to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customer_user_set',  # Change this line
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customer_user_permissions_set',  # Change this line
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
class SavedAdrress(models.Model):
    user = models.ForeignKey('customer.CustomUser', on_delete=models.CASCADE)
    address = models.CharField()

    def __str__(self):
        return self.address
    