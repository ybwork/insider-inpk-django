import re

from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from auth.models import User

user_model = User

custom_error_messages = {
    'min_length': 'Должно быть больше символов',
    'max_length': 'Превышен лимит символов',
    'required': 'Поле обязательно для заполнения',
    'unique': 'Запись уже существует',
    'format': 'Неверный формат',
    'invalid': 'Неверный формат',
}


class CompanyForm(forms.Form):
    company_name = forms.CharField(
        max_length=100,
        error_messages={
            'required': custom_error_messages['required'],
            'max_length': custom_error_messages['max_length']
        }
    )


def is_unique_email(value):
    try:
        user = user_model.objects.get(email=value)

        if user.email:
            raise ValidationError(custom_error_messages['unique'])
    except ObjectDoesNotExist:
        pass


def is_unique_phone(value):
    try:
        user = user_model.objects.get(phone=value)

        if user.phone:
            raise ValidationError(custom_error_messages['unique'])
    except ObjectDoesNotExist:
        pass


class RegisterForm(forms.Form):
    company_name = forms.CharField(
        max_length=100,
        error_messages={
            'required': custom_error_messages['required'],
            'max_length': custom_error_messages['max_length']
        }
    )

    first_name = forms.CharField(
        max_length=100,
        error_messages={
            'required': custom_error_messages['required'],
            'max_length': custom_error_messages['max_length']
        }
    )

    last_name = forms.CharField(
        max_length=100,
        error_messages={
            'max_length': custom_error_messages['max_length']
        }
    )

    middle_name = forms.CharField(
        max_length=100,
        error_messages={
            'max_length': custom_error_messages['max_length']
        }
    )

    email = forms.EmailField(
        validators=[is_unique_email],
        max_length=255,
        error_messages={
            'required': custom_error_messages['required'],
            'max_length': custom_error_messages['max_length'],
            'unique': custom_error_messages['unique'],
            'invalid': custom_error_messages['invalid']
        }
    )

    phone = forms.CharField(
        validators=[is_unique_phone],
        max_length=50,
        error_messages={
            'required': custom_error_messages['required'],
            'max_length': custom_error_messages['max_length'],
            'unique': custom_error_messages['unique'],
        }
    )

    password = forms.CharField(
        max_length=255,
        error_messages={
            'required': custom_error_messages['required'],
            'max_length': custom_error_messages['max_length']
        }
    )

    is_agree_with_save_personal_data = forms.BooleanField(
        error_messages={
            'required': 'Подтвердите обработку персональных данных',
        }
    )


class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=255,
        error_messages={
            'required': custom_error_messages['required'],
            'invalid': custom_error_messages['invalid'],
            'max_length': custom_error_messages['max_length']
        }
    )

    password = forms.CharField(
        max_length=255,
        error_messages={
            'required': custom_error_messages['required'],
            'max_length': custom_error_messages['max_length'],
        }
    )


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        min_length=6,
        max_length=255,
        error_messages={
            'required': custom_error_messages['required'],
            'min_length': custom_error_messages['min_length'],
            'max_length': custom_error_messages['max_length'],
        }
    )

    password_confirmation = forms.CharField(
        min_length=6,
        max_length=255,
        error_messages={
            'required': custom_error_messages['required'],
            'min_length': custom_error_messages['min_length'],
            'max_length': custom_error_messages['max_length'],
        }
    )

# class UserForm(ModelForm):
#     class Meta:
#         model = User
#
#         fields = [
#             'first_name',
#             'last_name',
#             'middle_name',
#             'email',
#             'phone',
#             'password',
#             'is_agree_with_save_personal_data'
#         ]
#
#         error_messages = {
#             'first_name': {
#                 'max_length': _(custom_error_messages['max_length']),
#                 'required': _(custom_error_messages['required']),
#             },
#
#             'last_name': {
#                 'max_length': _(custom_error_messages['max_length']),
#             },
#
#             'middle_name': {
#                 'max_length': _(custom_error_messages['max_length']),
#             },
#
#             'email': {
#                 'max_length': _(custom_error_messages['max_length']),
#                 'required': _(custom_error_messages['required']),
#                 'unique': _(custom_error_messages['unique'])
#             },
#
#             'phone': {
#                 'max_length': _(custom_error_messages['max_length']),
#                 'required': _(custom_error_messages['required']),
#                 'unique': _(custom_error_messages['unique'])
#             },
#
#             'password': {
#                 'max_length': _(custom_error_messages['max_length']),
#                 'required': _(custom_error_messages['required'])
#             },
#
#             'is_agree_with_save_personal_data': {
#                 'required': _(custom_error_messages['required']),
#             },
#         }
