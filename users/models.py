from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from base.models import Base


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, username, password, email, is_staff, is_active,*args,
                     **extra_fields):
        """
        Creates and saves a User with the given username and password.
        """

        user = self.model(username=username, email=email, is_staff=is_staff, is_active=is_active,
                          **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password, email=None, **extra_fields):
        return self._create_user(username, password, email, False, False, **extra_fields)

    def create_superuser(self, username, password, email=None, **extra_fields):
        extra_fields.update({
            'gender': 1,
            'birth_date': timezone.now(),
            'birth_place': 'Tehran',
            'address': 'Tehran',
            'is_superuser': True
        })
        return self._create_user(username, password, email, True, True, **extra_fields)


class User(Base, AbstractBaseUser,PermissionsMixin):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    objects = UserManager()
    username = models.CharField(_('user name'), max_length=255, unique=True,db_index=True)
    first_name = models.CharField(_('first name'), max_length=40,null=True, blank=True)
    last_name = models.CharField(_('last name'), max_length=80,null=True, blank=True)
    email = models.EmailField(_('email address'), max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text='Designates whether this user should be treated as active. '
                                              'Unselect this instead of deleting accounts.')

    gender = models.SmallIntegerField(_('Gender'), choices=[(1, 'Male'), (2, 'Female')], default=1, blank=False)
    birth_date = models.DateField(_('Birth Date'), null=True)
    birth_place = models.CharField(_('Birth Place'), null=True, max_length=100)
    last_certificate = models.CharField(_('last certificate'), null=True, max_length=300)
    address = models.TextField(_('Address'), null=True,blank=True)
    mobile_number = models.CharField(_('cell phone'), max_length=20,null=True, blank=True)
    USERNAME_FIELD = 'username'

    def get_full_name(self):
        return (u'%s %s' % (self.first_name, self.last_name)).strip()

    def get_short_name(self):
        return self.first_name
