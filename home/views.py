import os
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from .models import UploadFile
from get_phone.models import InfoForPhones
from get_phone.forms import RegisterNewPhone, UpdateReport
from django.contrib.auth import get_user_model


# Create your views here.

User = get_user_model()


def home(request):
    all_phone = InfoForPhones.objects.all()
    users = User.objects.all().count()
    # result = User.objects.filter(Q(user_ip__icontains=ip))

    query = request.GET.get('q')

    if query:
        all_phone = all_phone.filter(
            Q(serial_number_of_phone=query)
        ).distinct()

    context = {
        'query': query,
        'all_phone': all_phone,
        'users': users,
    }
    return render(request, 'home/index.html', context)


def how_it_work(request):
    files = UploadFile.objects.all()
    context = {
        'files': files,
    }
    return render(request, 'home/instructions.html', context)


def privacy(request):
    return render(request, 'home/privacy.html')


# def download(request, path):
#     file_path = os.path.join(settings.MEDIA_ROOT, path)
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as fh:
#             response = HttpResponse(fh.read(), content_type='application/adminupload')
#             response['Content-Disposition'] = 'inline;filename=' + os.path.basename(file_path)
#             return response
#     raise Http404



