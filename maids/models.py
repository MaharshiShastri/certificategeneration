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
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('SuperUser  must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('SuperUser  must have is_superuser=True')
    
# Custom User Model
class CustomUser (AbstractUser , PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    current_money = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    average_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # Override groups and user_permissions to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='maids_user_set',  # Change this line
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='maids_user_permissions_set',  # Change this line
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
class MaidRequirements(models.Model):
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.TextField()

    def __str__(self):
        return f"Maid Requirement - {self.description[:20]}"