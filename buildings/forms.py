from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from buildings.models import House, Building

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


class HouseForm(forms.Form):
    building_id = forms.CharField(
        max_length=255,
        error_messages={
            'max_length': custom_error_messages['max_length'],
            'required': custom_error_messages['required'],
        }
    )

    number_of_floors = forms.IntegerField(
        error_messages={
            'max_length': custom_error_messages['max_length'],
            'min_length': custom_error_messages['min_length'],
        }
    )

    living_floors = forms.CharField(
        required=False,
        error_messages={
            'max_length': custom_error_messages['max_length'],
        }
    )

    number_of_entrance = forms.IntegerField(
        required=False,
        error_messages={
            'max_length': custom_error_messages['max_length'],
            'min_length': custom_error_messages['min_length'],
        }
    )

    number_of_flat = forms.IntegerField(
        required=False,
        error_messages={
            'max_length': custom_error_messages['max_length'],
            'min_length': custom_error_messages['min_length'],
        }
    )

    street_name = forms.CharField(
        max_length=100,
        error_messages={
            'max_length': custom_error_messages['max_length'],
            'required': custom_error_messages['required']
        }
    )

    number = forms.CharField(
        max_length=255,
        error_messages={
            'max_length': custom_error_messages['max_length'],
            'required': custom_error_messages['required']
        }
    )

    finishing = forms.CharField(
        required=False,
        error_messages={
            'max_length': custom_error_messages['max_length'],
        }
    )

    materials = forms.CharField(
        required=False,
        error_messages={
            'max_length': custom_error_messages['max_length'],
        }
    )

    stage_development = forms.CharField(
        max_length=100,
        required=False,
        error_messages={
            'max_length': custom_error_messages['max_length'],
        }
    )

    start_development = forms.DateField(
        required=False,
        error_messages={
            'format': custom_error_messages['format']
        }
    )

    end_development = forms.DateField(
        required=False,
        error_messages={
            'format': custom_error_messages['format']
        }
    )


# class HouseForm(ModelForm):
#     class Meta:
#         model = House
#
#         fields = [
#             'building_id',
#             'number_of_floors',
#             'living_floors',
#             'number_of_entrance',
#             'number_of_flat',
#             'street_name',
#             'number',
#             'finishing',
#             'materials',
#             'stage_development',
#             'start_development',
#             'end_development'
#         ]
#
#         error_messages = {
#             'number_of_floors': {
#                 'max_length': _(custom_error_messages['max_length']),
#             },
#
#             'living_floors': {
#                 'max_length': _(custom_error_messages['max_length']),
#             },
#
#             'number_of_entrance': {
#                 'max_length': _(custom_error_messages['max_length']),
#             },
#
#             'number_of_flat': {
#                 'max_length': _(custom_error_messages['max_length']),
#             },
#
#             'street_name': {
#                 'max_length': _(custom_error_messages['max_length']),
#                 'required': _(custom_error_messages['required']),
#             },
#
#             'number': {
#                 'max_length': _(custom_error_messages['max_length']),
#                 'required': _(custom_error_messages['required']),
#             },
#
#             'finishing': {
#                 'max_length': _(custom_error_messages['max_length']),
#             },
#
#             'materials': {
#                 'required': _(custom_error_messages['required']),
#                 'max_length': _(custom_error_messages['max_length'])
#             },
#
#             'stage_development': {
#                 'required': _(custom_error_messages['required']),
#                 'max_length': _(custom_error_messages['max_length'])
#             },
#
#             'start_development': {
#                 'format': _(custom_error_messages['format']),
#             },
#
#             'end_development': {
#                 'format': _(custom_error_messages['format']),
#             },
#         }