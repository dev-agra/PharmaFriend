from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

# Creation of SuperUser
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError("Email Address cannot be Null")
        if not username:
            raise ValueError("Username cannot be Null")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True

        user.save(using=self._db)
        return user

# Creation of User Model
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_no = models.CharField(max_length=50)
    city_location = models.CharField(max_length=100, blank=True)
    consult_pending = models.BooleanField(default=False, blank=True)

    # Required Fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    object = MyAccountManager()
    
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True
    

# To store all relevant data about the user
class UserProfile(models.Model):
    # This onetoonefield is foreignkey but unique, i.e. one profile for one account
    # When forignkey usage we have multiple user profile for 1 person account
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    address_line1 = models.CharField(blank=True, max_length=100)
    address_line2 = models.CharField(blank=True, max_length=100)
    # Inside media folder profile is created
    profile_pic = models.ImageField(blank=True, upload_to='userprofile')
    city = models.CharField(blank=True, max_length=20)
    state = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def get_fulladdress(self):
        return f"{self.address_line1} {self.address_line2}"

    def to_json(self):
        return{
            'user_first_name': self.user.first_name,
            'user_last_name': self.user.last_name,
            'user_email': self.user.email,
            'user_phone_no': self.user.phone_no,
            'address_line1': self.address_line1,
            'address_line2': self.address_line2,
            'city': self.city,
            'state': self.state,
            'country': self.country,
        }
