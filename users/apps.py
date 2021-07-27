from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = "قسم المستخدمين"

    def ready(self):
        import users.signals
