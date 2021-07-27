import os
import sys

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from get_phone.validators import validate_file_extension

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your models here.
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver


class MyCustomManager(BaseUserManager):
    def create_user(self, full_name, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        if not full_name:
            raise ValueError('Users must have username')

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, full_name, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            full_name=full_name,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def get_profile_image_filepath(instance, filename):
    file_path = 'users_profile_img/{email}-{filename}'.format(
        email=str(instance.email), filename=filename
    )
    return file_path


class User(AbstractBaseUser):
    GENDER_STATUS = (
        ('رجل', 'رجل'),
        ('امرأه', 'امرأه'),
    )

    COUNTRY = (
        ('مصر', 'مصر'),
    )

    AGE = (
        ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'),
        ('26', '26'), ('27', '27'),
        ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31'), ('32', '32'), ('33', '33'), ('34', '34'), ('35', '35'),
        ('36', '36'), ('37', '37'),
        ('38', '38'), ('39', '39'), ('40', '40'), ('41', '41'), ('42', '42'), ('43', '43'), ('44', '44'), ('45', '45'),
        ('46', '46'), ('47', '47'),
        ('48', '48'), ('49', '49'), ('50', '50'), ('51', '51'), ('52', '52'), ('53', '53'), ('54', '54'), ('55', '55'),
        ('56', '56'), ('57', '57'),
        ('58', '58'), ('59', '59'), ('60', '60'), ('61', '61'), ('62', '62'), ('63', '63'), ('64', '64'), ('65', '65'),
    )
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,11}$', message='يجب ان يكون الهاتف بالشكل الاتى +99999999999')

    full_name = models.CharField(max_length=30, verbose_name='اسم المستخدم')
    email = models.EmailField(max_length=150, unique=True, verbose_name='الايميل')
    country = models.CharField(max_length=50, verbose_name='اسم الدوله', choices=COUNTRY)
    age = models.CharField(max_length=2, verbose_name='العمر', choices=AGE, null=True, blank=True, default='18')
    otp = models.CharField(max_length=8, null=True, blank=True)
    personal_phone = models.CharField(max_length=15, validators=[phone_regex], verbose_name='الهاتف الشخصي')
    gender = models.CharField(max_length=10, choices=GENDER_STATUS, verbose_name='النوع')
    personal_img = models.ImageField(upload_to=get_profile_image_filepath, null=True, blank=True,
                                     verbose_name='الصوره الشخصيه', validators=[validate_file_extension])
    user_ip = models.CharField(max_length=50, verbose_name='رقم ال ip  الخاص بالمستخدم', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ التسجيل الاساسي')
    last_login = models.DateTimeField(auto_now=True, verbose_name='تاريخ اخر تسجيل')
    register_from_mobile = models.CharField(max_length=100, verbose_name='التسجيل من الهاتف', blank=True, null=True)
    register_from_desktop = models.CharField(max_length=100, verbose_name='التسجيل من الكمبيوتر', blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyCustomManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email

    class Meta:
        ordering = ('-last_login',)
        verbose_name = "المستخدمين"
        verbose_name_plural = "المستخدمين"

    def has_perm(self, perm, obj=None):
        # return self.is_admin
        return True

    def has_module_perms(self, app_label):
        return True

    # def get_full_name(self):
    #     # The user is identified by their email address
    #     return self.email
    #
    # def get_short_name(self):
    #     # The user is identified by their email address
    #     return self.email

    # save custom size Image and convert it to jpg
    # def save(self, *args, **kwargs):
    #     imageTemproary = Image.open(self.personal_img)
    #     outputIoStream = BytesIO()
    #     imageTemproaryResized = imageTemproary.resize((300, 300))
    #     imageTemproaryResized.save(outputIoStream, format='PNG', quality=100)
    #     outputIoStream.seek(0)
    #     self.personal_img = InMemoryUploadedFile(outputIoStream, 'ImageField',
    #                                              "%s.png" % self.personal_img.name.split('.')[0],
    #                                              'image/png', sys.getsizeof(outputIoStream), None)
    #     super(User, self).save(*args, **kwargs)


def pre_save_user_info(sender, instance, *args, **kwargs):
    if instance.personal_img:
        imageTemproary = Image.open(instance.personal_img)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((300, 300))
        imageTemproaryResized.save(outputIoStream, format='PNG', quality=100)
        outputIoStream.seek(0)
        instance.personal_img = InMemoryUploadedFile(outputIoStream, 'ImageField',
                                                     "%s.png" % instance.personal_img.name.split('.')[0],
                                                     'image/png', sys.getsizeof(outputIoStream), None)


pre_save.connect(pre_save_user_info, sender=User)


# @receiver(post_delete, sender=User)
# def auto_delete_file_on_delete(sender, instance, **kwargs):
#     # instance.personal_img.delete(False)
#     """
#         Deletes file from filesystem
#         when corresponding `User` object is deleted.
#     """
#     if instance.personal_img:
#         if os.path.isfile(instance.personal_img.path):
#             os.remove(instance.personal_img.path)
#
#
# @receiver(pre_save, sender=User)
# def auto_delete_file_on_change(sender, instance, **kwargs):
#     """
#     Deletes old file from filesystem
#     when corresponding `User` object is updated
#     with new file.
#     """
#     if not instance.pk:
#         return False
#
#     try:
#         personal_img = User.objects.get(pk=instance.pk).personal_img
#     except User.DoesNotExist:
#         return False
#
#     new_one = instance.personal_img
#     if not personal_img == new_one:
#         try:
#             if os.path.isfile(personal_img.path):
#                 os.remove(personal_img.path)
#         except:
#             return False


class Comment(models.Model):
    username = models.CharField(max_length=30, verbose_name='الاسم')
    email = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='الايميل')
    content = models.TextField(max_length=255, verbose_name='محتوى التعليق')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='وقت انشاء التعليق')
    approved_comments = models.BooleanField(default=False, verbose_name='الموافقه على التعليق')
    approved_comments_date = models.DateTimeField(auto_now_add=True, verbose_name='وقت الموافقه على التعليق')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('-created_at',)
        verbose_name = "تعليقات المستخدمين"
        verbose_name_plural = "تعليقات المستخدمين"


class ContactUs(models.Model):
    username = models.CharField(max_length=30, verbose_name='الاسم')
    email = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='الايميل')
    message = models.TextField(max_length=255, verbose_name='محتوى الرساله')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='وقت انشاء الرساله')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "رسائل قسم تواصل معنا"
        verbose_name_plural = "رسائل قسم تواصل معنا"
