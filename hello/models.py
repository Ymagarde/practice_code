from django.db import models
from django.conf import settings
#from django.contrib.auth.models import User
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

#custem usermanager
class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, password2=None):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, name
         and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


#custom model
class User(AbstractBaseUser):
    email = models.EmailField( verbose_name='email', max_length=255,unique=True,)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



class Profilepik(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True,related_name='customuser') 
    background_image = models.ImageField(upload_to='images/',null = True,blank = True)
    images= models.ImageField(upload_to='images/',null = True,blank =True)
    postby_name = models.CharField(max_length=100)


class Blog(models.Model):
    
    tag_name = models.CharField(max_length=100)
    blog_name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    post_by = models.CharField(max_length=100)
    images= models.ImageField(upload_to='images/',null = True,blank =True)
    