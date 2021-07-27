from django.contrib import admin
from .models import InfoForPhones

# Register your models here.


class InfoPhone(admin.ModelAdmin):
    list_display = ['owner_name', 'report_id', 'owner_mail', 'communication_number', 'type_of_phone',
                    'serial_number_of_phone', 'name_of_state', 'place_of_thift', 'Date_of_thift',
                    'Date_of_register', 'Date_of_register_updated', 'published_date',
                    'is_published', 'is_return']

    list_editable = ['is_published']
    ordering = ('is_published', 'Date_of_register', 'published_date', 'is_return')
    search_fields = ('report_id', 'owner_mail', 'communication_number', 'name_of_state')
    list_filter = ('is_published',  'is_return', 'Date_of_thift', 'name_of_state', 'Date_of_register',
                   'Date_of_register_updated')
    fieldsets = (
        ('المعلومات الشخصيه للشخص المبلغ', {'fields': ('report_id', 'owner_name', 'owner_mail', 'slug', 'communication_number',)}),
        ('معلومات الهاتف المفقود', {'fields': ('type_of_phone', 'serial_number_of_phone', 'phone_cover', 'phone_bill')}),
        ('معلومات الاماكن التى تم فقد الهاتف بها', {'fields': ('name_of_state', 'place_of_thift')}),
        ('الصلاحيات', {'fields': ('is_published', 'check_me_out', 'is_return')}),
    )


admin.site.register(InfoForPhones, InfoPhone)
