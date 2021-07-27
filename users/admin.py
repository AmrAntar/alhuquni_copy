from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .forms import UserAdminCreationForm, UserAdminChangeForm
from django.contrib.auth import get_user_model
from .models import Comment, ContactUs
User = get_user_model()


class UsersAdmin(BaseUserAdmin):
    # form = UserAdminChangeForm
    # add_form = UserAdminCreationForm

    list_display = ['full_name', 'email', 'country', 'age', 'personal_phone', 'gender', 'date_joined', 'is_admin',
                    'last_login', 'is_active']
    list_editable = ['is_active']
    search_fields = ('full_name', 'email', 'age', 'gender')
    readonly_fields = ('id', 'date_joined', 'last_login')
    list_filter = ('is_admin', 'is_staff', 'is_superuser', 'register_from_desktop', 'register_from_mobile')
    fieldsets = (
        (None, {'fields': ('password',)}),
        ('المعلومات الشخصيه', {'fields': ('full_name', 'email', 'country', 'age', 'personal_phone', 'gender',
                                          'personal_img', 'user_ip', 'register_from_mobile', 'register_from_desktop')}),
        ('الصلاحيات', {'fields': ('is_admin', 'is_staff', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    ordering = ('email',)
    filter_horizontal = ()


class AdminComments(BaseUserAdmin):
    list_display = ['username', 'email', 'approved_comments', 'created_at', 'approved_comments_date']
    list_display_links = ['username', 'email']
    list_editable = ['approved_comments']
    search_fields = ('username', 'email')
    readonly_fields = ('created_at',)
    list_filter = ('approved_comments',)
    fieldsets = (
        ('المعلومات الشخصيه', {'fields': ('username', 'email', 'content', 'created_at')}),
        ('الصلاحيات', {'fields': ('approved_comments',)}),
    )
    ordering = ('approved_comments',)
    filter_horizontal = ()


class AdminContactUs(BaseUserAdmin):
    list_display = ['username', 'email', 'created_at']
    search_fields = ('username', 'email')
    readonly_fields = ('created_at',)
    list_filter = ('created_at',)
    fieldsets = (
        ('المعلومات الشخصيه', {'fields': ('username', 'email', 'message', 'created_at')}),
    )
    ordering = ('created_at',)
    filter_horizontal = ()


admin.site.register(User, UsersAdmin)
admin.site.register(Comment, AdminComments)
admin.site.register(ContactUs, AdminContactUs)
admin.site.unregister(Group)


admin.site.site_header = 'ادراة موقع الحقوني'
admin.site.index_title = 'ادارة الموقع'                 # default: "Site administration"
admin.site.site_title = 'ادارة موقع الحقوني'            # default: "Django site admin"
