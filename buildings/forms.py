from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from buildings.models import Building

custom_error_messages = {
    'min_length': 'Должно быть больше символов',
    'max_length': 'Превышен лимит символов',
    'required': 'Поле обязательно для заполнения',
    'unique': 'Запись уже существует',
    'format': 'Неверный формат',
    'invalid': 'Неверный формат',
}


class BuildingForm(forms.Form):
        name = forms.CharField(
            max_length=255,
            error_messages={
                'max_length': custom_error_messages['max_length'],
                'required': custom_error_messages['required'],
            }
        )

        company_id = forms.CharField(
            max_length=255,
            error_messages={
                'max_length': custom_error_messages['max_length'],
                'required': custom_error_messages['required'],
            }
        )

        region = forms.CharField(
            max_length=100,
            required=False,
            error_messages={
                'max_length': custom_error_messages['max_length'],
            }
        )

        district = forms.CharField(
            max_length=100,
            required=False,
            error_messages={
                'max_length': custom_error_messages['max_length'],
            }
        )

        city = forms.CharField(
            max_length=50,
            required=False,
            error_messages={
                'max_length': custom_error_messages['max_length'],
            }
        )

        country = forms.CharField(
            max_length=100,
            required=False,
            error_messages={
                'max_length': custom_error_messages['max_length'],
            }
        )

        images = forms.CharField(
            required=False,
            error_messages={
                'max_length': custom_error_messages['max_length'],
            }
        )

        video = forms.CharField(
            required=False,
            error_messages={
                'max_length': custom_error_messages['max_length'],
            }
        )

        coordinates = forms.CharField(
            required=False,
            error_messages={
                'max_length': custom_error_messages['max_length'],
            }
        )

        currency = forms.CharField(
            max_length=50,
            required=False,
            error_messages={
                'max_length': custom_error_messages['max_length'],
            }
        )


# class BuildingForm(ModelForm):
#     class Meta:
#         model = Building
#
#         fields = [
#             'name',
#             'region',
#             'district',
#             'city',
#             'country',
#             'images',
#             'video',
#             'coordinates',
#             'currency',
#         ]
#
#         # exclude = ['company_id', 'company_hash_id']
#
#         error_messages = {
#             'name': {
#                 'max_length': _(custom_error_messages['max_length']),
#                 'required': _(custom_error_messages['required']),
#             },
#
#             'region': {
#                 'max_length': _(custom_error_messages['max_length']),
#             },
#
#             'district': {
#                 'max_length': _(custom_error_messages['max_length']),
#             },
#
#             'city': {
#                 'max_length': _(custom_error_messages['max_length']),
#             },
#
#             'country': {
#                 'max_length': _(custom_error_messages['max_length']),
#             },
#
#             'images': {
#                 'max_length': _(custom_error_messages['max_length']),
#             },
#
#             'video': {
#                 'required': _(custom_error_messages['required']),
#             },
#
#             'coordinates': {
#                 'required': _(custom_error_messages['required']),
#             },
#
#             'currency': {
#                 'required': _(custom_error_messages['required']),
#             },
#         }