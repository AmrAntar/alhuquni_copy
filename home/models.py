from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


User = get_user_model()


# def get_download_file_filepath(instance, filename):
#     file_path = 'Downloaded_file/{title}'.format(
#         title=str(instance.title), filename=filename
#     )
#     return file_path


class UploadFile(models.Model):
    title = models.CharField(max_length=100, verbose_name='اسم الملف')
    file = models.FileField(upload_to='files/', verbose_name='الملف')
    created = models.DateTimeField(auto_now_add=True, verbose_name='وقت انشاء الملف')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-title', )
        verbose_name = "الملفات التى يطلب من المستخدمين تحميلها"
        verbose_name_plural = "الملفات التى يطلب من المستخدمين تحميلها"


