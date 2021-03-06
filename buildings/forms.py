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
            'required': custom_error_messages['required'],
            'max_length': custom_error_messages['max_length'],
            'min_length': custom_error_messages['min_length'],
        }
    )

    living_floors = forms.CharField(
        error_messages={
            'required': custom_error_messages['required'],
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
        error_messages={
            'required': custom_error_messages['required'],
            'format': custom_error_messages['format'],
            'invalid': custom_error_messages['invalid']
        }
    )

    end_development = forms.DateField(
        error_messages={
            'required': custom_error_messages['required'],
            'format': custom_error_messages['format'],
            'invalid': custom_error_messages['invalid']
        }
    )


class FlatSchemaForm(forms.Form):
    house_id = forms.CharField(
        max_length=255,
        error_messages={
            'required': custom_error_messages['required']
        }
    )

    type = forms.CharField(
        max_length=255,
        error_messages={
            'required': custom_error_messages['required'],
            'max_length': custom_error_messages['max_length']
        }
    )

    number_of_balcony = forms.IntegerField(
        error_messages={
            'required': custom_error_messages['required'],
        }
    )

    number_of_loggia = forms.IntegerField(
        error_messages={
            'format': custom_error_messages['format']
        }
    )

    number_of_rooms = forms.IntegerField(
        error_messages={
            'required': custom_error_messages['required'],
            'format': custom_error_messages['format']
        }
    )

    area = forms.DecimalField(
        error_messages={
            'required': custom_error_messages['required'],
            'format': custom_error_messages['format'],
            'invalid': custom_error_messages['invalid']
        }
    )

    price = forms.DecimalField(
        error_messages={
            'required': custom_error_messages['required'],
            'format': custom_error_messages['format'],
            'invalid': 'Введите целое число'
        }
    )


class FloorTypeForm(forms.Form):
    house_id = forms.CharField(
        max_length=255,
        error_messages={
            'required': custom_error_messages['required'],
            'max_length': custom_error_messages['max_length']
        }
    )

    number = forms.IntegerField(
        error_messages={
            'required': custom_error_messages['required'],
            'format': custom_error_messages['format']
        }
    )

    clone_floors = forms.CharField(
        required=False,
        max_length=255,
        error_messages={
            'required': custom_error_messages['required'],
            'max_length': custom_error_messages['max_length']
        }
    )

    number_of_flats = forms.IntegerField(
        error_messages={
            'required': custom_error_messages['required'],
            'format': custom_error_messages['format']
        }
    )


class FlatTypeForm(forms.Form):
    house_id = forms.CharField(
        max_length=255,
        error_messages={
            'required': custom_error_messages['required'],
            'max_length': custom_error_messages['max_length']
        }
    )

    floor_type_id = forms.CharField(
        max_length=255,
        error_messages={
            'required': custom_error_messages['required'],
            'max_length': custom_error_messages['max_length']
        }
    )

    flat_schema_id = forms.CharField(
        max_length=255,
        error_messages={
            'required': custom_error_messages['required'],
            'max_length': custom_error_messages['max_length']
        }
    )

    entrance = forms.IntegerField(
        error_messages={
            'required': custom_error_messages['required'],
            'max_length': custom_error_messages['max_length']
        }
    )

    number = forms.IntegerField(
        error_messages={
            'required': custom_error_messages['required'],
            'max_length': custom_error_messages['max_length']
        }
    )

    coordinates = forms.CharField(
        max_length=255,
        required=False,
        error_messages={
            'max_length': custom_error_messages['max_length']
        }
    )

    windows = forms.CharField(
        max_length=255,
        required=False,
        error_messages={
            'max_length': custom_error_messages['max_length']
        }
    )


class FlatForm(forms.Form):
    # house_id = forms.CharField(
    #     max_length=255,
    #     error_messages={
    #         'required': custom_error_messages['required'],
    #         'max_length': custom_error_messages['max_length']
    #     }
    # )
    #
    # flat_schema_id = forms.CharField(
    #     max_length=255,
    #     error_messages={
    #         'required': custom_error_messages['required'],
    #         'max_length': custom_error_messages['max_length']
    #     }
    # )
    #
    # flat_type_id = forms.CharField(
    #     max_length=255,
    #     error_messages={
    #         'required': custom_error_messages['required'],
    #         'max_length': custom_error_messages['max_length']
    #     }
    # )
    #
    # floor = forms.IntegerField(
    #     error_messages={
    #         'required': custom_error_messages['required'],
    #         'max_length': custom_error_messages['max_length']
    #     }
    # )
    #
    # entrance = forms.IntegerField(
    #     error_messages={
    #         'required': custom_error_messages['required'],
    #         'max_length': custom_error_messages['max_length']
    #     }
    # )
    #
    # number = forms.IntegerField(
    #     error_messages={
    #         'required': custom_error_messages['required'],
    #         'max_length': custom_error_messages['max_length']
    #     }
    # )
    #
    # windows = forms.CharField(
    #     max_length=255,
    #     required=False,
    #     error_messages={
    #         'max_length': custom_error_messages['max_length']
    #     }
    # )

    status = forms.IntegerField(
        error_messages={
            'required': custom_error_messages['required'],
            'max_length': custom_error_messages['max_length'],
        }
    )

    price = forms.DecimalField(
        error_messages={
            'required': custom_error_messages['required'],
            'max_length': custom_error_messages['max_length'],
        }
    )

    area = forms.DecimalField(
        error_messages={
            'required': custom_error_messages['required'],
            'max_length': custom_error_messages['max_length'],
        }
    )