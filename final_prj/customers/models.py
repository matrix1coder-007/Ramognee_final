from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Permission


# Create your models here.
import uuid
from django.utils import timezone


# A model to inherit the time-stamp details from


class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# A manager for the custom user model


class CustomUserManager(BaseUserManager):

    def create_staff_user(self, email, password=None):

        print('staff user creation')

        if not email:
            raise ValueError("Users must have an email address")

        if not password:
            raise ValueError("Users must have a password")

        staff_user_obj = self.model(
            user_email=self.normalize_email(email)
        )

        staff_user_obj.set_password(password)
        staff_user_obj.save(using=self._db)

        print('staff user created')

        return staff_user_obj

    def create_admin_user(self, email, password=None):

        print('admin user creation')

        if not email:
            raise ValueError("Users must have an email address")

        if not password:
            raise ValueError("Users must have a password")

        admin_user_obj = self.model(
            user_email=self.normalize_email(email)
        )

        admin_user_obj.set_password(password)
        admin_user_obj.admin = True
        admin_user_obj.save(using=self._db)

        print('admin user created')

        return user

    def create_superuser(self, user_email, password=None):

        print('super-user creation')

        if not user_email:
            raise ValueError("Users must have an email address")

        if not password:
            raise ValueError("Users must have a password")

        super_user_obj = self.model(
            user_email=self.normalize_email(user_email)
        )
        super_user_obj.set_password(password)
        super_user_obj.admin = True
        super_user_obj.superuser = True
        super_user_obj.save(using=self._db)

        print('super-user created')

        return super_user_obj

# A model for the custom user


class CustomUserModel(AbstractBaseUser, TimeStampedModel):

    uuid_user = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    fname_user = models.CharField(max_length=200)
    mname_user = models.CharField(max_length=200, null=True, blank=True)
    lname_user = models.CharField(max_length=200)
    user_email = models.EmailField(max_length=500, unique=True)
    is_superuser = models.BooleanField(default=False)
    staff = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    joining_dt_user = models.DateTimeField(default=timezone.now)
    deactivation_dt_user = models.DateField(null=True, blank=True)

    USERNAME_FIELD = 'user_email'

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    # admin console access for staff?
    @property
    def is_staff(self):
        return self.staff

    # admin console access for admin?
    @property
    def is_admin(self):
        return self.admin

    # admin console access for active?
    @property
    def is_active(self):
        return True

    # User's full name?
    def user_fullname(self):

        def non_nullify_names(name):

            if name:
                return name
            return ''

        first_name = non_nullify_names(self.fname_user)
        mid_name = non_nullify_names(self.mname_user)
        last_name = non_nullify_names(self.lname_user)

        if mid_name == '':
            return first_name + ' ' + last_name

        return first_name + ' ' + mid_name + ' ' + last_name

    # User's UUID?

    def user_uuid(self):
        return self.uuid_user

    # User administrative statistics?

    def user_admin_statistics(self):

        return {
            'User e-mail': self.user_email,
            'Joining date': self.joining_dt_user,
            'Is_Active': self.is_active,
            'Is_Superuser': self.is_superuser,
            'Is_Admin': self.admin,
            'Is_Staff': self.staff,
            'Deactivation date': self.deactivation_dt_user if self.is_active else '-'
        }

    # By default return value for a user?

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:

        abstract = False
        db_table = "Custom_Users"
        verbose_name = "Custom_User"
        verbose_name_plural = "Custom_Users"
