import re

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.forms import TextInput, CheckboxInput, Field
from .models import InfoForPhones
from django.contrib.auth import get_user_model

User = get_user_model()


class DateInput(forms.DateInput):
    input_type = 'date'


class RegisterNewPhone(forms.ModelForm):
    # Make Email Not Required
    def __init__(self, *args, **kwargs):
        super(RegisterNewPhone, self).__init__(*args, **kwargs)
        # self.fields['owner_mail'].required = False
        # self.fields['owner_mail'].widget.attrs['readonly'] = True
        self.fields['owner_name'].widget.attrs['readonly'] = True
        self.fields['communication_number'].widget.attrs['readonly'] = True
        self.fields['communication_number'].required = True
        # self.fields['communication_number'].help_text = 'يجب عليك اولا تحديث بياناتك واضافة رقم الهاتف من خلال حسابك الشخصي'
        self.fields['phone_cover'].help_text = 'ضع صوره واضحه'
        # self.fields['phone_bill'].help_text = 'ضع صوره واضحه'
        # self.fields['phone_bill'].help_text = 'اختيارى'
        # self.fields['phone_bill'].required = False
        self.fields['type_of_phone'].help_text = 'ضع حروف وارقام فقط بحد اكثر 30 حرف ، لا يقبل الرموز'
        self.fields['name_of_state'].help_text = 'ضع حروف وارقام فقط بحد اكثر 30 حرف ، لا يقبل الرموز'
        self.fields['place_of_thift'].help_text = 'ضع حروف وارقام فقط بحد اكثر 50 حرف ، لا يقبل الرموز'
        self.fields['serial_number_of_phone'].help_text = 'ضع ارقام فقط بحد اكثر 15 رقم ، لا يقبل الرموز او المسافات'
        self.fields['Date_of_thift'].help_text = 'ضع تاريخ السرقه'
        self.fields['check_me_out'].help_text = 'يجب التأكيد على اقرار المسؤوليه ، حتى يتم تسجيل البلاغ بنجاح'
        # if self.instance:
        #     # If the instance has no image, they haven't uploaded anything
        #     if not self.instance.phone_bill:
        #         # Alter the field in the form
        #         self.fields['phone_bill'].disabled = True

    owner_name = forms.CharField(label='مقدم البلاغ')
    # owner_mail = forms.EmailField(label='ايميل المبلغ')
    communication_number = forms.CharField(label='رقم هاتفك الحالي')
    type_of_phone = forms.CharField(label='نوع الهاتف المفقود', widget=TextInput())

    # Make IMEI num Only Number By add javaScript Code (Not Chars Or Text), Code Added in Base Html Page
    serial_number_of_phone = forms.CharField(widget=TextInput(attrs={'maxlength': '15'}), label='رقم ال IMEI الخاص بالهاتف المفقود')
    # phone_bill = forms.ImageField(widget=forms.FileInput, label='صورة فاتورة الشراء موضح عليها البيانات')
    phone_cover = forms.ImageField(widget=forms.FileInput, label='صورة علبة الهاتف  موضح عليها رقم الIMEI')
    name_of_state = forms.CharField(widget=TextInput(attrs={'maxlength': '30'}), label='اسم البلد التي تم فقد الهاتف فيها')
    place_of_thift = forms.CharField(widget=TextInput(attrs={'maxlength': '50'}), label='اسم المنطقه التى تم فقد الهاتف بها')
    Date_of_thift = forms.DateField(widget=DateInput, label='تاريخ الفقد')
    check_me_out = forms.BooleanField(required=True, label='اقر بأن جميع البيانات التي تم ادخالها صحيحه ، وتقع على '
                                                           'مسؤليتي الشخصيه، وفي حالة مخالفة ذلك ، اكون قد عرضت نفسي '
                                                           'للمساءله القانونيه بكافة اشكالها، ويحق فى هذه الحاله '
                                                           'لادارة الموقع منفرده، باتخاذ اي اجراء مناسب لها.',
                                      widget=CheckboxInput(attrs={'class': 'check-input'}))

    class Meta:
        model = InfoForPhones
        fields = '__all__'
        exclude = ('slug', 'owner_mail', 'report_id', 'is_published', 'Date_of_register_updated', 'published_date',
                   'is_return', 'is_return_date', 'phone_bill')

    # Validate IMEI Num
    def clean_serial_number_of_phone(self):
        serial_num = self.cleaned_data.get('serial_number_of_phone')
        min_length = 15
        blockSpecialRegex = [";", "/", "]", "-", "?", "/", "+", "ً", "َ", ">", "<", "ٌ", ",",
                             "ُ", ";", ":", "إٌ", "ُ", "‘", "÷", "×", "؛", "ْْآ", "،", "ـ", "’", "]", "[",
                             "}", "{", "=", "؟", "!", "#", "$", "%", "^", "&", "(", ")", "_", "'",
                             "*", "~", "`", "[", '"']

        if len(serial_num) < min_length or len(serial_num) > min_length:
            raise forms.ValidationError('عفوا يجب ادخال قيمة مكونه من 15 رقم !')

        if InfoForPhones.objects.filter(serial_number_of_phone=serial_num).exists():
            raise ValidationError('عفوا هذا ال IMEI ، تم التبليغ عنه من قبل !')

        for char in blockSpecialRegex:
            if str(char) in serial_num:
                raise ValidationError('لا يسمح بأدخال رموز خاصه مثل (#$%.@!)، يقبل ارقام فقط !')

        if bool(re.search('[\D\s]', serial_num)):  # serial_num should not have whitespace or Text
            raise forms.ValidationError("لا تضع مسافات بين الارقام او احرف ، يقبل ارقام فقط !")

        return serial_num

    def clean_type_of_phone(self):
        check = self.cleaned_data['type_of_phone']
        max_length = 30
        blockSpecialRegex = [";", "/", "]", "-", "?", "/", "+", "ً", "َ", ">", "<", "ٌ", ",",
                             "ُ", ";", ":", "إٌ", "ُ", "‘", "÷", "×", "؛", "ْْآ", "،", "ـ", "’", "]", "[",
                             "}", "{", "=", "؟", "!", "#", "$", "%", "^", "&", "(", ")", "_", "'",
                             "*", "~", "`", "[", '"', "@", ",", "."]
        for char in blockSpecialRegex:
            if str(char) in check:
                raise ValidationError('لا يسمح بأدخال رموز خاصه مثل (#$%.@!) !')

        if len(check) > max_length:
            raise forms.ValidationError('عفوا يجب ادخال 30 حرف على الاكثر !')
        return check

    def clean_name_of_state(self):
        check = self.cleaned_data.get('name_of_state')
        max_length = 30
        blockSpecialRegex = [";", "/", "]", "-", "?", "/", "+", "ً", "َ", ">", "<", "ٌ", ",",
                             "ُ", ";", ":", "إٌ", "ُ", "‘", "÷", "×", "؛", "ْْآ", "،", "ـ", "’", "]", "[",
                             "}", "{", "=", "؟", "!", "#", "$", "%", "^", "&", "(", ")", "_", "'",
                             "*", "~", "`", "[", '"', "@", ",", "."]
        for char in blockSpecialRegex:
            if str(char) in check:
                raise ValidationError('لا يسمح بأدخال رموز خاصه مثل (#$%.@!) !')

        if len(check) > max_length:
            raise forms.ValidationError('عفوا يجب ادخال 30 حرف على الاكثر !')
        return check

    def clean_place_of_thift(self):
        check = self.cleaned_data.get('place_of_thift')
        max_length = 50
        blockSpecialRegex = [";", "/", "]", "-", "?", "/", "+", "ً", "َ", ">", "<", "ٌ", ",",
                             "ُ", ";", ":", "إٌ", "ُ", "‘", "÷", "×", "؛", "ْْآ", "،", "ـ", "’", "]", "[",
                             "}", "{", "=", "؟", "!", "#", "$", "%", "^", "&", "(", ")", "_", "'",
                             "*", "~", "`", "[", '"', "@", ",", "."]
        for char in blockSpecialRegex:
            if str(char) in check:
                raise ValidationError('لا يسمح بأدخال رموز خاصه مثل (#$%.@!) !')

        if len(check) > max_length:
            raise forms.ValidationError('عفوا يجب ادخال 50 حرف على الاكثر !')
        return check

    def clean_check_me_out(self):
        check = self.cleaned_data.get('check_me_out')
        if not check:
            raise forms.ValidationError('يجب عليك وضع علامة موافق حتى يتم التسجيل بنجاح !')

        return check


class UpdateReport(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpdateReport, self).__init__(*args, **kwargs)
        self.fields['is_return'].required = False

    type_of_phone = forms.CharField(label='نوع الهاتف المفقود', widget=TextInput(attrs={'maxlength': '20'}))
    name_of_state = forms.CharField(widget=TextInput(attrs={'maxlength': '20'}),label='اسم البلد التي تم فقد الهاتف فيها')
    place_of_thift = forms.CharField(widget=TextInput(attrs={'maxlength': '40'}),label='اسم المنطقه التى تم فقد الهاتف بها')
    is_return = forms.BooleanField(label='هل تم استعاده الهاتف ؟')
    Date_of_thift = forms.DateField(widget=DateInput, label='تاريخ الفقد')

    class Meta:
        model = InfoForPhones
        fields = ['type_of_phone', 'name_of_state',
                  'place_of_thift', 'Date_of_thift', 'is_return']
        exclude = ('phone_cover', 'phone_bill', 'communication_number')

    def save(self, commit=True):
        report = self.instance
        # report.communication_number = self.cleaned_data['communication_number']
        report.type_of_phone = self.cleaned_data['type_of_phone']
        report.name_of_state = self.cleaned_data['name_of_state']
        report.place_of_thift = self.cleaned_data['place_of_thift']
        report.Date_of_thift = self.cleaned_data['Date_of_thift']
        report.is_return = self.cleaned_data['is_return']

        if commit:
            report.save()
        return report

    # Validate Communication Num
    def clean_communication_number(self):
        serial_number = self.cleaned_data.get('communication_number')
        MIN_LINGTH = 11
        vodafone = ("010", "011", "012",)

        if len(serial_number) < MIN_LINGTH:
            raise forms.ValidationError('عفوا يجب ان يكون رقم الهاتف مكون من 11 رقم !')

        # Validate if phone number Start with (010, 011, 012)
        if not serial_number.startswith(vodafone):
            raise forms.ValidationError('عفوا يجب ان يبدأ الرقم ب 010 او 011 او 012 !')
        return serial_number

    def clean_type_of_phone(self):
        check = self.cleaned_data.get('type_of_phone')
        blockSpecialRegex = ['@', '.', '+']
        for char in blockSpecialRegex:
            if str(char) in check:
                raise ValidationError('لا يسمح بأدخال رموز خاصه !')
            return check
