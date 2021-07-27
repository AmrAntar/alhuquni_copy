import os
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import InfoForPhones
from .forms import RegisterNewPhone, UpdateReport
from django.contrib.auth import get_user_model

from django.template.loader import render_to_string
from django.core.mail import EmailMessage

User = get_user_model()
# from django.contrib.auth.models import User


@login_required(login_url='login')
def register_new_phone(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = RegisterNewPhone(request.POST or None, request.FILES or None)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner_mail = request.user
                obj.save()
                form = RegisterNewPhone()
                messages.success(request, 'تم ارسال بلاغك للادارة للمراجعه '
                                          ' فى حالة صحة مطابقة البيانات المدخله سيتم النشر فى فتره اقصاها 48 ساعه')

                return redirect('profile')

        else:
            form = RegisterNewPhone(
                initial={
                    'owner_mail': request.user.email,
                    'owner_name': request.user.full_name,
                    'communication_number': request.user.personal_phone,
                }
            )
        context = {
            'form': form,
        }
        return render(request, 'get_phone/register_new_phone.html', context)


def send_email_success_share(request):
    pass


def report_detail(request, slug):
    report = get_object_or_404(InfoForPhones, slug=slug)
    context = {
        'report': report,
    }
    return render(request, 'get_phone/report_detail.html', context)


def delete_report(request, slug):
    report = get_object_or_404(InfoForPhones, slug=slug)
    report.delete()
    messages.success(request, 'تم حذف البلاغ بنجاح')
    return redirect('profile')


def update_report(request, slug):
    report = get_object_or_404(InfoForPhones, slug=slug)
    if request.method == 'POST':
        form = UpdateReport(request.POST or None, request.FILES or None, instance=report)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            obj = UpdateReport()
            messages.success(request, 'تم تحديث بيانات البلاغ بنجاح')
            return redirect('profile')

    else:
        form = UpdateReport(
            initial={
                'type_of_phone': report.type_of_phone,
                'serial_number_of_phone': report.serial_number_of_phone,
                'name_of_state': report.name_of_state,
                'place_of_thift': report.place_of_thift,
                'Date_of_thift': report.Date_of_thift,
                'is_return': report.is_return,
            }
        )
    context = {
        'form': form,
    }
    return render(request, 'get_phone/update_report.html', context)
