import re

from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, render_to_response
from django.template.defaulttags import url
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from django.core import serializers
from django.core.mail import send_mail, get_connection
from django.db import transaction
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import path
from django.views.decorators.http import require_http_methods
from django.views.generic.base import View
from auth.forms import CompanyForm, LoginForm, RegisterForm
from auth.models import Company, User
from insider.services import Deserialization, Helper

deserialization = Deserialization()
user_model = User
company_model = Company
helper = Helper()


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

    form = RegisterForm(data)

    if form.is_valid():
        with transaction.atomic():
            created_company = company_model.manager.create(form.cleaned_data)

            form.cleaned_data['company'] = created_company
            form.cleaned_data['company_hash_id'] = created_company.hash_id
            form.cleaned_data['email_code'] = helper.create_hash()
            form.cleaned_data['is_admin'] = True

            created_user = user_model.manager.create(form.cleaned_data)

            """ отправка письма на почту для подтверждения аккаунта, зашить  """
            message = 'https:/' + reverse(
                'confirm_email',
                kwargs={'email_code': created_user.email_code}
            ) + '?api_key=' + created_user.api_key

            mail = send_mail(
                subject='test',
                message=message,
                from_email='inpk@gmail.com',
                recipient_list=[created_user.email],
                connection=get_connection()
            )

        return generate_json_response(data={**model_to_dict(created_company), **model_to_dict(created_user)}, status=200)

    return generate_json_response(data={**form.errors}, status=400)


@require_http_methods(['POST'])
def login(request):
    data = json_decode(request.body)

    form = LoginForm(data)

    if form.is_valid():
        user = get_user_with_company(email=data['email'])

        if is_user_exists(user) and is_valid_password(data['password'], user.password):
            return generate_json_response(data=model_to_dict(user), status=200)

        return generate_json_response(data={'message': 'Логин или пароль не верны'}, status=400)

    return JsonResponse(form.errors, status=400)


def confirm_email(request, email_code):
    try:
        user = user_model.manager.get(email_code=email_code)
        user.is_confirmed_email = True
        user.save()
    except ObjectDoesNotExist:
        return render_to_response(template_name='404/404.html')

    return HttpResponseRedirect(reverse('home'))


def send_reset_link_on_email(request):
    pass

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

    user_model.manager.update_api_key(data['api_key'])

    return generate_json_response(status=200)


class User(View):
    def get(self, request):
        users = all(user_model)

        return generate_json_response(data=json_encode_queryset(users))

    def post(self, request):
        data = json_decode(request.body)

        form = RegisterForm(data)

        if form.is_valid():
            company = get(model=company_model, hash_id=data['company_id'])

            form.cleaned_data['company'] = company
            form.cleaned_data['company_hash_id'] = company.hash_id
            form.cleaned_data['is_admin'] = False
            form.cleaned_data['is_agree_with_save_personal_data'] = True

            user = create(model=user_model, data=form.cleaned_data)

            return generate_json_response(data=model_to_dict(user))

        return generate_json_response(data={**form.errors}, status=400)

    def put(self, request, id):
        data = json_decode(request.body)

        form = RegisterForm(data)

        if form.is_valid():
            old_user = get(user_model, hash_id=id)

            new_user = update(model=user_model, old_data=old_user, new_data=data)

            return generate_json_response(data=model_to_dict(new_user), status=200)

        return JsonResponse(form.errors, status=400)

    def delete(self, request, id):
        delete(user_model, hash_id=id)

        return JsonResponse({}, status=200)


def get_company_users(request, id):
    users = serializers.serialize(
        'json', user_model.manager.exclude(is_admin=True).filter(company_hash_id=id)
    )

    return generate_json_response(data=users, status=200)
