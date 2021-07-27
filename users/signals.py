from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import get_user_model
from django.dispatch import receiver


User = get_user_model()


# to get ip address fro user by session
@receiver(user_logged_in, sender=User)
def login_success(sender, request, user, **kwargs):
    ip = request.META.get("REMOTE_ADDR")
    print("CLIENT IP: ", ip)
    request.session['ip'] = ip
