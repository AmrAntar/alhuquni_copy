from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
# from django.core.validators import validate_email
from django.contrib.auth.forms import PasswordChangeForm
from .models import Comment, ContactUs
from validate_email import validate_email

User = get_user_model()


# User Form ----> its appear to only users
class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].label = False
        self.fields['email'].label = False
        self.fields['password1'].label = False
        self.fields['password2'].label = False

    full_name = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': 'اسم المستخدم'}))
    email = forms.EmailField(max_length=150, widget=forms.EmailInput(attrs={'placeholder': 'الايميل', 'class': 'new-input'}))
    password1 = forms.CharField(max_length=10, widget=forms.PasswordInput(attrs={'placeholder': 'كلمة المرور'}))
    password2 = forms.CharField(max_length=10, widget=forms.PasswordInput(attrs={'placeholder': 'تأكيد كلمة المرور'}))

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email:
            try:
                User.objects.get(email=email)
            except User.DoesNotExist:
                return email
            raise forms.ValidationError("هذا الايميل مستخدم من قبل !")

        if email == "":
            raise ValidationError("يجب ادخال قيمه للحقل !")

        if not validate_email(email):
            raise ValidationError("من فضلك ادخل ايميل صحيح")


# User Form ----> its appear to only users
class LoginForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = False
        self.fields['password'].label = False

    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'الايميل', 'class': 'new-input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'كلمة المرور'}))

    class Meta:
        model = User
        fields = ['email', 'password']

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')

            if email and password:
                self.user_cache = authenticate(username=email, password=password)
                if self.user_cache is None:
                    raise forms.ValidationError("ربما يكون الايميل او كلمة المرور المدخلين خطأ،")

                elif not self.user_cache.is_active:
                    raise forms.ValidationError("This account is inactive.")
            return self.cleaned_data


# User reset email Form ----> its appear to only users
class RequestResetEmailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RequestResetEmailForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['email'].label = False

    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'الايميل', 'class': 'new-input'}))

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # if email:
        #     try:
        #         User.objects.get(email=email)
        #     except User.DoesNotExist:
        #         return email
        #     raise forms.ValidationError("هذا الايميل غير مسجل لدينا !")

        if email == "":
            raise ValidationError("يجب ادخال قيمه للحقل !")

        if not validate_email(email):
            raise ValidationError("من فضلك ادخل ايميل صحيح")


# User reset email Form ----> its appear to only users
class SetNewPasswordForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SetNewPasswordForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = True
        self.fields['password1'].label = False
        self.fields['password2'].required = True
        self.fields['password2'].label = False

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'كلمة المرور الجديده'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'تأكيد كلمة المرور'}))

    class Meta:
        model = User
        fields = ['password1', 'password2']

    def clean_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 == "" or password2 == "":
            raise ValidationError("يجب ادخال قيمه للحقل !")

        if password1 < 8:
            raise ValidationError("يجب ان تكون كلمة المرور 8 احرف فأكثر !")

        if password1 != password2:
            raise ValidationError("كلمات المرور غير متطابقه !")


# Update User Form ----> its appear to only users
class UpdateUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        # self.fields['email'].required = False
        self.fields['country'].required = True
        self.fields['personal_phone'].required = True
        self.fields['age'].required = True
        self.fields['gender'].required = True
        self.fields['personal_img'].required = False
        # self.fields['email'].widget.attrs['disabled'] = 'disabled'
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['full_name'].widget.attrs['readonly'] = True
        # self.fields['full_name'].label = False
        # self.fields['email'].label = False
        # self.fields['country'].label = False
        # self.fields['personal_phone'].label = False
        # self.fields['gender'].label = False

    GENDER_STATUS = (
        ('رجل', 'رجل'),
        ('امرأه', 'امرأه'),
    )

    COUNTRY = (
        ('مصر', 'مصر'),
    )

    AGE = (
        ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'),
        ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31'), ('32', '32'), ('33', '33'), ('34', '34'), ('35', '35'), ('36', '36'), ('37', '37'),
        ('38', '38'), ('39', '39'), ('40', '40'), ('41', '41'), ('42', '42'), ('43', '43'), ('44', '44'), ('45', '45'), ('46', '46'), ('47', '47'),
        ('48', '48'), ('49', '49'), ('50', '50'), ('51', '51'), ('52', '52'), ('53', '53'), ('54', '54'), ('55', '55'), ('56', '56'), ('57', '57'),
        ('58', '58'), ('59', '59'), ('60', '60'), ('61', '61'), ('62', '62'), ('63', '63'), ('64', '64'), ('65', '65'),
    )

    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'اسم المستخدم', 'class': 'new-input-profile'}), label='اسم المستخدم', max_length=30)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'الايميل', 'class': 'new-input-profile'}), label='الايميل')
    personal_phone = forms.CharField(widget=forms.TextInput(attrs={'onkeypress': 'isInputNumber(event)', 'placeholder': 'ادخل رقم الهاتف', 'maxlength': '11', 'class': 'new-input-profile'}), label='رقم الهاتف')
    age = forms.ChoiceField(label='العمر', choices=AGE)
    country = forms.ChoiceField(label='اسم الدوله', choices=COUNTRY)
    gender = forms.ChoiceField(label='النوع', choices=GENDER_STATUS)
    personal_img = forms.ImageField(widget=forms.FileInput, label='صورة البروفايل')

    class Meta:
        model = User
        fields = ['full_name', 'email', 'country', 'age', 'personal_phone', 'gender', 'personal_img']

    # Validate personal_phone
    def clean_personal_phone(self):
        phone = self.cleaned_data.get('personal_phone')
        min_length = 11
        phone_code = ("010", "011", "012",)

        if len(phone) < min_length:
            raise forms.ValidationError('عفوا يجب ان يكون رقم الهاتف مكون من 11 رقم !')

        # Validate if phone number Start with (010, 011, 012)
        if not phone.startswith(phone_code):
            raise forms.ValidationError('عفوا يجب ان يبدأ الرقم ب 010 او 011 او 012 !')

        return phone


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = False
        self.fields['new_password1'].label = False
        self.fields['new_password2'].label = False

    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'ادخل كملة المرور القديمه'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'ادخل كلمة المرور الجديده'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'تأكيد كلمة المرور الجديده'}))


class CommentsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentsForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = False
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['content'].required = True
        self.fields['content'].label = False
        self.fields['content'].widget.attrs['placeholder'] = 'ضع تعليقك هنا ...'
        self.fields['content'].widget.attrs['maxlength'] = '255'

    class Meta:
        model = Comment
        fields = '__all__'
        exclude = ('email', 'approved_comments', 'approved_comments_date')


class ContactUsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactUsForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = False
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['message'].label = False
        self.fields['message'].widget.attrs['maxlength'] = '255'
        self.fields['message'].widget.attrs['placeholder'] = 'ضع رسالتك هنا ...'

    # email = forms.EmailField(max_length=150, widget=forms.EmailInput(attrs={'class': 'contact-input'}))
    # message = forms.CharField(widget=forms.TextInput(attrs={'class': 'contact-input', 'rows': '3'}))

    class Meta:
        model = ContactUs
        fields = ['username', 'message']

    def clean_message(self):
        message = self.cleaned_data.get('message')
        blockSpecialRegex = [";", "/", "]", "-", "?", "/", "+", "ً", "َ", ">", "<", "ٌ", ",",
                             "ُ", ";", ":", "إٌ", "ُ", "‘", "÷", "×", "؛", "ْْآ", "،", "ـ", "’", "]", "[",
                             "}", "{", "=", "؟", "!", "#", "$", "%", "^", "&", "(", ")", "_", "'",
                             "*", "~", "`", "[", '"']

        for char in blockSpecialRegex:
            if str(char) in message:
                raise ValidationError('لا يسمح بأدخال رموز خاصه مثل (#$%.@!)، يقبل حروف وارقام فقط !')

        if not message:
            raise ValidationError('يجب ادخال قيمة صحيحه اولا، لا يسمح بحقل فارغ !')

        return message

