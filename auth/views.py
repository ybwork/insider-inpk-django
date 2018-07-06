from django.contrib.auth.hashers import check_password
from django.core import serializers
from django.db import transaction
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.generic.base import View
from auth.forms import CompanyForm, UserForm
from auth.models import Company, User
from insider.services import Deserialization

deserialization = Deserialization()
user_model = User
company_model = Company


def create(model, data):
    return model.manager.create(data)


def get(model, **condition):
    return model.manager.get(**condition)


def all(model):
    return model.manager.all()


def update(model, old_data, new_data):
    return model.manager.update(old_data, new_data)


def delete(model, **condition):
    return model.manager.get(**condition).delete()


def json_decode(data):
    return deserialization.json_decode(data)


def json_encode_queryset(data):
    return serializers.serialize('json', data)


def generate_json_response(data={}, status=200):
    response = JsonResponse(data=data, status=status, safe=False)
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['POST'])
def register(request):
    data = json_decode(request.body)

    company_form = CompanyForm(data)
    user_form = UserForm(data)

    if company_form.is_valid() and user_form.is_valid():
        with transaction.atomic():
            created_company = create(model=company_model, data=company_form.cleaned_data)

            user_form.cleaned_data['company'] = created_company
            user_form.cleaned_data['company_hash_id'] = created_company.hash_id
            user_form.cleaned_data['is_admin'] = True

            created_user = create(model=user_model, data=user_form.cleaned_data)

            """ Здесь должна быть отправка письма на почту для подтверждения аккаунта """

        return generate_json_response(data={**model_to_dict(created_company), **model_to_dict(created_user)}, status=200)

    return generate_json_response(data={**company_form.errors, **user_form.errors}, status=400)


@require_http_methods(['POST'])
def login(request):
    data = json_decode(request.body)

    user = get_user_with_company(email=data['email'])

    if is_user_exists(user) and is_valid_password(data['password'], user.password):
        return generate_json_response(data=model_to_dict(user), status=200)

    return generate_json_response(data={'message': 'Логин или пароль не верны'}, status=400)


def get_user_with_company(**condition):
    return user_model.manager.select_related().filter(**condition).first()


def is_user_exists(user):
    if user:
        return True

    return False


def is_valid_password(password, encoded):
    if check_password(password, encoded):
        return True

    return False


@require_http_methods(['POST'])
def logout(request):
    data = json_decode(request.body)

    update_api_key_user(data['api_key'])

    return generate_json_response(status=200)


def update_api_key_user(api_key):
    return user_model.manager.update_api_key(api_key)


class User(View):
    def get(self, request):
        users = all(user_model)

        return generate_json_response(data=json_encode_queryset(users))

    def post(self, request):
        data = json_decode(request.body)

        user_form = UserForm(data)

        if user_form.is_valid():
            company = get(model=company_model, hash_id=data['company_id'])

            user_form.cleaned_data['company'] = company
            user_form.cleaned_data['company_hash_id'] = company.hash_id
            user_form.cleaned_data['is_admin'] = False
            user_form.cleaned_data['is_agree_with_save_personal_data'] = True

            user = create(model=user_model, data=user_form.cleaned_data)

            return generate_json_response(data=model_to_dict(user))

        return generate_json_response(data={**user_form.errors}, status=400)

    def put(self, request, id):
        data = json_decode(request.body)

        old_user = get(user_model, hash_id=id)

        new_user = update(model=user_model, old_data=old_user, new_data=data)

        return generate_json_response(data=model_to_dict(new_user), status=200)

    def delete(self, request, id):
        delete(user_model, hash_id=id)

        return JsonResponse({}, status=200)


def get_company_users(request, id):
    users = serializers.serialize(
        'json', user_model.manager.exclude(is_admin=True).filter(company_hash_id=id)
    )

    return generate_json_response(data=users, status=200)
