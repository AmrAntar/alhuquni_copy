import os
import sys

from django.conf import settings
from django.core.mail import EmailMessage
from django.db import models
from django.template.loader import render_to_string

from .utils import unique_report_id_generator
from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver
from django.utils.text import slugify
from .validators import validate_file_extension

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from django.contrib.auth import get_user_model

# Create your models here.


User = get_user_model()


def get_phone_cover_filepath(instance, filename):
    file_path = 'phone_cover/{owner_mail}-{report_id}-{filename}'.format(
        owner_mail=str(instance.owner_mail), report_id=str(instance.report_id), filename=filename
    )
    return file_path


class InfoForPhones(models.Model):
    report_id = models.CharField(max_length=30, verbose_name='رقم البلاغ')
    owner_name = models.CharField(max_length=50, verbose_name='مقدم البلاغ')
    slug = models.SlugField(unique=True, blank=True)
    owner_mail = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='الايميل')
    communication_number = models.CharField(max_length=15, verbose_name='رقم الهاتف الحالى للتواصل')
    type_of_phone = models.CharField(max_length=30, verbose_name='نوع الهاتف')
    phone_cover = models.ImageField(upload_to=get_phone_cover_filepath, verbose_name='صورة علبة الهاتف', blank=True,
                                    null=True, validators=[validate_file_extension])
    serial_number_of_phone = models.CharField(max_length=15, verbose_name='رقم ال IMEI')
    phone_bill = models.ImageField(upload_to=get_phone_cover_filepath, verbose_name='صورة من فاتورة الشراء', blank=True,
                                   null=True, validators=[validate_file_extension])
    name_of_state = models.CharField(max_length=30, verbose_name='اسم البلد التى تمت فيها السرقه')
    place_of_thift = models.CharField(max_length=50, verbose_name='مكان السرقه')
    Date_of_thift = models.DateField(verbose_name='تاريخ السرقه')
    Date_of_register = models.DateTimeField(auto_now_add=True, verbose_name='وقت تسجيل البلاغ')
    Date_of_register_updated = models.DateTimeField(auto_now=True, verbose_name='وقت تحديث البلاغ')
    is_published = models.BooleanField(default=False, verbose_name='السماح بنشر البلاغ')
    published_date = models.DateTimeField(auto_now_add=True, verbose_name='وقت الموافقه على البلاغ')
    is_return = models.BooleanField(default=False, verbose_name='تمت عودة الهاتف')
    is_return_date = models.DateTimeField(auto_now=True, verbose_name='تاريخ عودة الهاتف')
    check_me_out = models.BooleanField(default=True, verbose_name='تعهد بصحة البيانات')

    def __str__(self):
        return str(self.owner_mail)

    class Meta:
        ordering = ('-Date_of_register',)
        verbose_name = "بلاغات المستخدمين"
        verbose_name_plural = "بلاغات المستخدمين"

    # save custom size Image and convert it to jpg
    # def save(self, *args, **kwargs):
    #     imageTemproary = Image.open(self.phone_cover)
    #     outputIoStream = BytesIO()
    #     imageTemproaryResized = imageTemproary.resize((400, 300))
    #     imageTemproaryResized.save(outputIoStream, format='PNG', quality=100)
    #     outputIoStream.seek(0)
    #     self.phone_cover = InMemoryUploadedFile(outputIoStream, 'ImageField',
    #                                             "%s.png" % self.phone_cover.name.split('.')[0],
    #                                             'image/png', sys.getsizeof(outputIoStream), None)
    #
    #     imageTemproary = Image.open(self.phone_bill)
    #     outputIoStream = BytesIO()
    #     imageTemproaryResized = imageTemproary.resize((400, 300))
    #     imageTemproaryResized.save(outputIoStream, format='PNG', quality=100)
    #     outputIoStream.seek(0)
    #     self.phone_bill = InMemoryUploadedFile(outputIoStream, 'ImageField',
    #                                            "%s.png" % self.phone_bill.name.split('.')[0],
    #                                            'image/png', sys.getsizeof(outputIoStream), None)
    #
    #     super(InfoForPhones, self).save(*args, **kwargs)


@receiver(post_delete, sender=InfoForPhones)
def send_message_on_delete(sender, instance, **kwargs):
    user = instance.owner_name
    email = instance.owner_mail
    imei = instance.serial_number_of_phone
    email_subject = "للاسف تم رفض البلاغ"
    email_body = render_to_string('get_phone/message_when_delete.html',
                                  {
                                      'user': user,
                                      'imei': imei,
                                  }
                                  )
    email_message = EmailMessage(
        email_subject,
        email_body,
        settings.EMAIL_HOST_USER,
        [email],
    )
    email_message.send(fail_silently=False)


def pre_save_phone_info(sender, instance, *args, **kwargs):
    if not instance.slug:
        # instance.slug = slugify(instance.owner_name + "-" + instance.serial_number_of_phone)
        instance.slug = arabic_slugify(instance.owner_name + "-" + instance.serial_number_of_phone)

    if not instance.report_id:
        instance.report_id = unique_report_id_generator(instance)

    if instance.phone_cover:
        imageTemproary = Image.open(instance.phone_cover)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((400, 300))
        imageTemproaryResized.save(outputIoStream, format='PNG', quality=100)
        outputIoStream.seek(0)
        instance.phone_cover = InMemoryUploadedFile(outputIoStream, 'ImageField',
                                                "%s.png" % instance.phone_cover.name.split('.')[0],
                                                'image/png', sys.getsizeof(outputIoStream), None)

    if instance.phone_bill:
        imageTemproary = Image.open(instance.phone_bill)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((400, 300))
        imageTemproaryResized.save(outputIoStream, format='PNG', quality=100)
        outputIoStream.seek(0)
        instance.phone_bill = InMemoryUploadedFile(outputIoStream, 'ImageField',
                                                "%s.png" % instance.phone_bill.name.split('.')[0],
                                                'image/png', sys.getsizeof(outputIoStream), None)


pre_save.connect(pre_save_phone_info, sender=InfoForPhones)


@receiver(post_save, sender=InfoForPhones)
def send_user_data_when_created_by_admin(sender, instance, **kwargs):
    user = instance.owner_name
    email = instance.owner_mail
    imei = instance.serial_number_of_phone
    repo_id = instance.report_id
    Date_of_register = instance.Date_of_register
    if instance.is_published:
        email_subject = "تمت الموافقه على نشر بلاغك"
        email_body = render_to_string('get_phone/share_info_success.html',
                                      {
                                          'user': user,
                                          'imei': imei,
                                          'repo_id': repo_id,
                                          'Date_of_register': Date_of_register
                                      }
                                      )
        email_message = EmailMessage(
            email_subject,
            email_body,
            settings.EMAIL_HOST_USER,
            [email],
        )
        email_message.send(fail_silently=False)


def arabic_slugify(str):
    str = str.replace(" ", "-")
    str = str.replace(",", "-")
    str = str.replace("(", "-")
    str = str.replace(")", "")
    str = str.replace("؟", "")
    return str
