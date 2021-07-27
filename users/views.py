from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
# from django.core.validators import validate_email
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from validate_email import validate_email

from .forms import SignUpForm, LoginForm, UpdateUserForm, SetNewPasswordForm, ChangePasswordForm, CommentsForm, ContactUsForm
from django.contrib.auth import update_session_auth_hash

from get_phone.models import InfoForPhones
from django.contrib.auth import get_user_model
# from django.views.decorators.cache import never_cache
from .models import Comment
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.contrib.auth.views import PasswordChangeView, PasswordResetDoneView

# # Create your views here.

User = get_user_model()


def get_user_ip(request):
    try:
        address = request.META.get('HTTP_X_FORWARDED_FOR')
        if address:
            ip = address.split(",")[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
    except:
        ip = ""
    return ip


def sign_up_page(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SignUpForm(request.POST or None)
            if form.is_valid():
                user = form.save(commit=False)
                email = request.POST.get('email')
                user.is_active = False
                # user.user_ip = get_user_ip(request)  # to store ip address for users
                user.user_ip = request.session.get('ip',
                                                   get_user_ip(request))  # to store ip address for users by session
                user.register_from_mobile = request.POST['mobile']
                user.register_from_desktop = request.POST['desktop']
                user.save()
                messages.success(request, 'تم ارسال رابط تفعيل حسابك على الايميل ، برجاء مراجعة ايميلك')

                current_site = get_current_site(request)
                email_subject = 'تفعيل الحساب الخاص بك'
                email_body = render_to_string('users/email_body_message.html',
                                              {
                                                  'user': user,
                                                  'domain': current_site.domain,
                                                  'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                                  'token': account_activation_token.make_token(user)
                                              }
                                              )
                email_message = EmailMessage(
                    email_subject,
                    email_body,
                    settings.EMAIL_HOST_USER,
                    [email],
                )
                email_message.send(fail_silently=False)
                return redirect('sign_up')
        else:
            form = SignUpForm()
        context = {
            'form': form,
        }
        return render(request, 'users/sign_up.html', context)
    else:
        return redirect('home')


# to verify user account by email ----> user
def verification_email(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # messages.success(request, 'تم تفعيل الحساب بنجاح')
        return redirect('login')
    # else:
    #     messages.error(request, 'عملية تسجيل غير صحيحه.. اعد التسجيل مره اخرى !')
    #     return redirect('signup')

    messages.error(request, 'هذا الرابط فقد صلاحيته، ولا يجوز استخدامه مرتين')
    return render(request, 'users/activation_failed.html', status=401)


def login_page(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request.POST or None)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        messages.success(request, 'تم تسجيل الدخول بنجاح')
                        return redirect('profile')
                    else:
                        return HttpResponseRedirect('in active account')

        else:
            form = LoginForm()
        context = {
            'form': form,
        }
        return render(request, 'users/login.html', context)
    else:
        return redirect('home')


def profile_page(request):
    if request.user.is_authenticated:
        personal_info = request.user
        all_data = InfoForPhones.objects.filter(owner_mail=request.user)
        context = {
            'all_data': all_data,
            'personal_info': personal_info,
        }
        return render(request, 'users/profile.html', context)
    else:
        return redirect('home')


def users_update_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UpdateUserForm(request.POST, request.FILES or None, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'تم تحديث بياناتك بنجاح')
                return redirect('profile')
        else:
            form = UpdateUserForm(
                initial={
                    'email': request.user.email,
                    'full_name': request.user.full_name,
                    'country': request.user.country,
                    'personal_phone': request.user.personal_phone,
                    'gender': request.user.gender,
                    'personal_img': request.user.personal_img,
                }
            )
        context = {
            'form': form,
        }
        return render(request, 'users/users_update_info.html', context)

    else:
        return redirect('home')


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')

    else:
        return redirect('home')


# to reset user password ----> user
def request_reset_email(request):
    if request.method == 'POST':
        data = request.POST
        email = request.POST['email']
        if not validate_email(email):
            messages.error(request, 'ضع ايميل صحيح !')
            return redirect('request_reset_email')

        user = User.objects.filter(email=email)
        if user.exists():
            current_site = get_current_site(request)
            email_subject = 'استعادة كلمة المرور'
            email_body = render_to_string('users/reset_user_password.html',
                                          {
                                              'domain': current_site.domain,
                                              'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                                              'token': PasswordResetTokenGenerator().make_token(user[0])
                                          }
                                          )
            email_message = EmailMessage(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [email],
            )
            email_message.send(fail_silently=False)
            messages.success(request, 'تم ارسال رابط استعادة كلمة المرور لهذا الايميل')
            return redirect('request_reset_email')

        else:
            messages.error(request, 'هذا الحساب غير مسجل لدينا، او ربما يكون قد تم تعطيله او حزفه')
            return redirect('request_reset_email')
    else:
        data = request.POST
    context = {
        'data': data,
    }
    return render(request, 'users/request_reset_email.html', context)


# to reset user password ----> user
def set_new_password(request, uidb64, token):
    if request.method == "GET":
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.error(request, 'عفوا الرابط فقط صلاحيته..اعد العمليه من جديد')
                return redirect('request_reset_email')

        except DjangoUnicodeDecodeError as e:
            messages.error(request, 'حدث خطأ اثناء الاستعاده .. برجاء اعادة المحاوله')
            return redirect('set_new_password')

    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password1')
            try:
                uid = force_text(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
                if not PasswordResetTokenGenerator().check_token(user, token):
                    messages.error(request, 'عفوا الرابط فقط صلاحيته..اعد العمليه من جديد')
                    return redirect('request_reset_email')

                user.set_password(password)
                user.save()
                messages.success(request, 'تم تغيرر كلمة المرور بنجاح .. الان يمكنك الدخول مجددا')
                return redirect('login')

            except DjangoUnicodeDecodeError as e:
                messages.error(request, 'حدث خطأ اثناء الاستعاده .. برجاء اعادة المحاوله')
                return redirect('set_new_password')

    else:
        form = SetNewPasswordForm()
    context = {
        'uidb64': uidb64,
        'token': token,
        'form': form,
    }
    return render(request, 'users/set_new_password.html', context)


def change_password(request):
    if not request.user.is_authenticated:
        return redirect('login')

    else:
        if request.method == 'POST':
            form = ChangePasswordForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'تم تغيير كلمة المرور بنجاح')
                return redirect('profile')
            else:
                messages.error(request, 'حدث خطا .. من فضلك اعد المحاوله')
        else:
            form = ChangePasswordForm(request.user)
        context = {
            'form': form,
        }
        return render(request, 'users/change_password.html', context)


def users_comments(request):
    # comments = Comment.objects.filter(approved_comments=True).order_by('-created_at')[:3]
    comments = Comment.objects.filter(approved_comments=True)
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            form = CommentsForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                # content = request.POST.get('content')
                # comment = Comment.objects.create(content=content, email=request.user)
                comment.email = request.user
                comment.save()
                messages.success(request, 'تم ارسال رسالتك بنجاح، وتتنظر موافقه الاداره للنشر')
                return redirect('users_comments')

        else:
            form = CommentsForm(
                initial={
                    'username': request.user.full_name,
                }
            )
        context = {
            'form': form,
            'comments': comments,
        }
        return render(request, 'users/users_comments.html', context)


def contact_us(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ContactUsForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.email = request.user
                comment.save()
                messages.success(request, 'تم ارسال رسالتك بنجاح، فريق عمل الموقع يتمنى لكم يوما سعيدا')
                return redirect('contact_us')

        else:
            form = ContactUsForm(
                initial={
                    'username': request.user.full_name,
                }
            )

        context = {
            'form': form,
        }
        return render(request, 'users/contact_us.html', context)
    else:
        return redirect('login')