from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class PlayerManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The username is required for user creation.')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class School(models.Model):
    name = models.CharField(max_length=255, unique=True)
    NBonLivraison = models.CharField(max_length=255, null=True)
    capacity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class DeviceType(models.Model):
    Device = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.Device

class Brands(models.Model):
    Brand = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.Brand

class Stock(models.Model):
    IN = 'IN'
    OUT = 'OUT'

    STATUSCHOICES = [
        (IN, 'IN'),
        (OUT, 'OUT')
    ]

    SerialNumber = models.CharField(max_length=255, unique=True)
    DeviceType = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    HostName = models.CharField(max_length=255, null=True)
    Brand = models.ForeignKey(Brands, on_delete=models.CASCADE)
    Date = models.DateField(auto_now_add=True)
    Model = models.CharField(max_length=255)
    Config = models.CharField(max_length=255)
    DeviceStatus = models.CharField(max_length=3, choices=STATUSCHOICES, default=IN)
    Capacity = models.IntegerField(default=0)

    Garantie = models.BooleanField(default=False)
    Dotation = models.BooleanField(default=False)
    MiseEnRebute = models.BooleanField(default=False)

    NumeroArrivage = models.BooleanField(default=False)
    Retour = models.BooleanField(default=False)

    def __str__(self):
        return self.SerialNumber

class StocksPerSchool(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='devices')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, default="admin")

    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = PlayerManager()

    def __str__(self):
        return self.username
