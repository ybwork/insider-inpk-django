from django.core.exceptions import ObjectDoesNotExist
from django.middleware.csrf import _get_new_csrf_string, _salt_cipher_secret
from django.shortcuts import render, render_to_response
from django.urls import reverse
from django.contrib.auth.hashers import check_password, make_password
from django.core import serializers
from django.core.mail import send_mail, get_connection
from django.db import transaction
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.views.generic.base import View
from auth.forms import LoginForm, RegisterForm, ResetPasswordForm
from auth.models import Company, User
from insider.services import Deserialization, Helper

deserialization = Deserialization()
user_model = User
company_model = Company
helper = Helper()
register_form = RegisterForm
login_form = LoginForm
reset_password_form = ResetPasswordForm


# def create(model, data):
#     return model.manager.create(data)
#
#
# def get(model, **condition):
#     return model.manager.get(**condition)
#
#
# def all(model):
#     return model.manager.all()
#
#
# def update(model, old_data, new_data):
#     return model.manager.update(old_data, new_data)
#
#
# def delete(model, **condition):
#     return model.manager.get(**condition).delete()


def json_decode(data):
    return deserialization.json_decode(data)


# def json_encode_queryset(data):
#     return serializers.serialize('json', data)


def generate_json_response(data={}, status=200):
    response = JsonResponse(data=data, status=status, safe=False)
    response['Access-Control-Allow-Origin'] = '*'
    return response


def is_equal_passwords(password, password_confirmation):
    if password == password_confirmation:
        return True
    return False


def create_link_confirmation(url_name, code, url_param_name):
    """ когда зальём на сервак, придумать как динамически получать имя домена """
    return 'http://172.100.2.15:8000' + reverse(
        url_name,
        kwargs={url_param_name: code}
    )


def create_response_with_html_template(path_to_template):
    return render_to_response(template_name=path_to_template)


def redirect_to_page(page):
    return HttpResponseRedirect(reverse(page))


@require_http_methods(['POST'])
def register(request):
    data = json_decode(request.body)

    form = get_register_form(data)

    if not is_equal_passwords(data['password'], data['password_confirmation']):
        return JsonResponse({'message': 'Пароли не совпадают'}, status=400)

    if form.is_valid():
        user = create_user(form.cleaned_data, is_amdin=True)

        send_confirmation_account_to_email(user)

        success_message = 'Вы успешно зарегистрировались! На вашу почту отправленно сообщение с подтверждением.'

        return generate_json_response(data={'message': success_message}, status=200)

    return generate_json_response(data={**form.errors}, status=400)


def get_register_form(data):
    return register_form(data)


def create_user(data, is_amdin):
    with transaction.atomic():
        company = company_model.objects.create(
            hash_id=helper.create_hash(),
            name=data['company_name'],
        )

        return user_model.objects.create(
            hash_id=helper.create_hash(),
            company=company,
            company_hash_id=company.hash_id,
            first_name=data['first_name'],
            last_name=data['last_name'],
            middle_name=data['middle_name'],
            email=data['email'],
            email_code=helper.create_hash(),
            phone=data['phone'],
            password=make_password(data['password']),
            is_agree_with_save_personal_data=data['is_agree_with_save_personal_data'],
            api_key=generate_api_key(),
            is_admin=is_amdin,
        )


def send_confirmation_account_to_email(user):
    link_confirmation = create_link_confirmation(
        url_name='confirm_email',
        code=user.email_code,
        url_param_name='email_code'
    )

    message = 'Для подтверждения аккаунта перейдите по этой ссылке: ' + link_confirmation

    return send_mail(
        subject='test',
        message=message,
        from_email='inpk@gmail.com',
        recipient_list=[user.email],
        connection=get_connection()
    )


@require_http_methods(['POST'])
def login(request):
    data = json_decode(request.body)

    form = get_login_form(data)

    if form.is_valid():
        user = get_user_by_email(data['email'])

        if is_user_exists(user) and is_valid_user_password(data['password'], user.password):
            return generate_json_response(data=model_to_dict(user), status=200)

        return generate_json_response(data={'message': 'Логин или пароль не верны'}, status=400)

    return JsonResponse(form.errors, status=400)


def get_login_form(data):
    return login_form(data)


def get_user_by_email(email):
    return user_model.objects.select_related().filter(email=email).first()


def is_user_exists(user):
    if user:
        return True

    return False


def is_valid_user_password(current_password, password_from_db):
    if check_password(current_password, password_from_db):
        return True

    return False


def confirm_email(request, email_code):
    try:
        user = get_user_by_email_code(email_code)
        confirm_user_email(user)
    except ObjectDoesNotExist:
        return create_response_with_html_template(path_to_template='404/404.html')

    return redirect_to_page('home')


def get_user_by_email_code(email_code):
    return user_model.objects.get(email_code=email_code)


def confirm_user_email(user):
    user.is_confirmed_email = True
    user.save()
    return user


@require_http_methods(['POST'])
def send_reset_link_email(request):
    data = json_decode(request.body)

    user = get_user_by_email(data['email'])

    if not is_user_exists(user):
        return generate_json_response(
            data={'message': 'Такой почтовый ящик не найден в нашей системе'},
            status=400
        )

    password_code = add_password_code_confirmation_to_user(user)

    confirmation = send_confirmation_reset_password_to_email(password_code, data['email'])

    if is_confrimation_send(confirmation):
        return generate_json_response(data={'message': 'Успешно'}, status=200)
    return generate_json_response(status=500)


# def get_user_object_by_email(email):
#     return user_model.objects.get(email=email)


def add_password_code_confirmation_to_user(user):
    user.password_code = create_confirmation_code_for_reset_password()
    user.save()
    return user.password_code


def create_confirmation_code_for_reset_password():
    return helper.create_hash()


def send_confirmation_reset_password_to_email(password_code, email):
    link_confirmation = create_link_confirmation(
        url_name='show_reset_password_form',
        code=password_code,
        url_param_name='password_code'
    )

    message = 'Для сброса пароля перейдите по этой ссылке: ' + link_confirmation

    return send_mail(
        subject='test',
        message=message,
        from_email='inpk@gmail.com',
        recipient_list=[email],
        connection=get_connection()
    )


def is_confrimation_send(confirmation):
    if confirmation:
        return True
    return False


def show_reset_password_form(request, password_code):
    try:
        user = get_user_object_by_password_code(password_code)
    except ObjectDoesNotExist:
        return create_response_with_html_template(path_to_template='404/404.html')

    return render(request, 'reset_password/reset_password.html', model_to_dict(user))


def get_user_object_by_password_code(password_code):
    return user_model.objects.get(password_code=password_code)


def reset_password(request):
    data = json_decode(request.body)

    if not is_equal_passwords(data['password'], data['password_confirmation']):
        return JsonResponse({'message': 'Пароли не совпадают'}, status=400)

    form = get_reset_password_form(data)

    if form.is_valid():
        user = get_user_object_by_password_code(data['password_code'])

        update_user_password(user, form.cleaned_data['password'])

        return HttpResponse('должен быть редирект на логин, но я хз, как это с vue')

    return JsonResponse(form.errors, status=400)


def get_reset_password_form(data):
    return reset_password_form(data)


def update_user_password(user, password):
    user.password = make_password(password)
    user.save()
    return user.password


@require_http_methods(['POST'])
def logout(request):
    data = json_decode(request.body)

    update_api_key(data)

    return generate_json_response(status=200)


def update_api_key(data):
    user = user_model.objects.get(api_key=data['api_key'])
    user.api_key = generate_api_key()
    user.save()
    return user.api_key


def generate_api_key():
    csrf_secret = _get_new_csrf_string()
    return _salt_cipher_secret(csrf_secret)

# class User(View):
#     def get(self, request):
#         users = all(user_model)
#
#         return generate_json_response(data=json_encode_queryset(users))
#
#     def post(self, request):
#         data = json_decode(request.body)
#
#         form = RegisterForm(data)
#
#         if form.is_valid():
#             company = get(model=company_model, hash_id=data['company_id'])
#
#             form.cleaned_data['company'] = company
#             form.cleaned_data['company_hash_id'] = company.hash_id
#             form.cleaned_data['is_admin'] = False
#             form.cleaned_data['is_agree_with_save_personal_data'] = True
#
#             user = create(model=user_model, data=form.cleaned_data)
#
#             return generate_json_response(data=model_to_dict(user))
#
#         return generate_json_response(data={**form.errors}, status=400)
#
#     def put(self, request, id):
#         data = json_decode(request.body)
#
#         form = RegisterForm(data)
#
#         if form.is_valid():
#             old_user = get(user_model, hash_id=id)
#
#             new_user = update(model=user_model, old_data=old_user, new_data=data)
#
#             return generate_json_response(data=model_to_dict(new_user), status=200)
#
#         return JsonResponse(form.errors, status=400)
#
#     def delete(self, request, id):
#         delete(user_model, hash_id=id)
#
#         return JsonResponse({}, status=200)
#
#
# def get_company_users(request, id):
#     users = serializers.serialize(
#         'json', user_model.manager.exclude(is_admin=True).filter(company_hash_id=id)
#     )
#
#     return generate_json_response(data=users, status=200)
