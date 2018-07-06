from django.forms import ModelForm
from django import forms
from django.utils.translation import gettext_lazy as _

from auth.models import User

custom_error_messages = {
    'max_length': 'Превышен лимит символов',
    'required': 'Поле обязательно для заполнения',
    'unique': 'Запись уже существует',
    'min_length': 'Минимальное кол-во символов 2',
    'format': 'Неверный формат',
}


class CompanyForm(forms.Form):
    company_name = forms.CharField(
        max_length=100,
        error_messages={
            'required': custom_error_messages['required'],
            'max_length': custom_error_messages['max_length']
        }
    )


class UserForm(ModelForm):
    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            'middle_name',
            'email',
            'phone',
            'password',
            'is_agree_with_save_personal_data'
        ]

        error_messages = {
            'first_name': {
                'max_length': _(custom_error_messages['max_length']),
                'required': _(custom_error_messages['required']),
            },

            'last_name': {
                'max_length': _(custom_error_messages['max_length']),
            },

            'middle_name': {
                'max_length': _(custom_error_messages['max_length']),
            },

            'email': {
                'max_length': _(custom_error_messages['max_length']),
                'required': _(custom_error_messages['required']),
                'unique': _(custom_error_messages['unique'])
            },

            'phone': {
                'max_length': _(custom_error_messages['max_length']),
                'required': _(custom_error_messages['required']),
                'unique': _(custom_error_messages['unique'])
            },

            'password': {
                'max_length': _(custom_error_messages['max_length']),
                'required': _(custom_error_messages['required'])
            },

            'is_agree_with_save_personal_data': {
                'required': _(custom_error_messages['required']),
            },
        }
