from django.contrib.auth.hashers import make_password
from django.db import models

from insider.services import Helper, Validation

helper = Helper()
validation = Validation()


class CompanyManager(models.Manager):
    def create(self, data):
        company = self.model(
            hash_id=helper.create_hash(),
            name=data['company_name'],
        )

        company.save()

        return company


class Company(models.Model):
    hash_id = models.CharField(max_length=16, db_index=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'company'

    manager = CompanyManager()


class UserManager(models.Manager):
    def create(self, data):
        user = self.model(
            hash_id=helper.create_hash(),
            company=data['company'],
            company_hash_id=data['company_hash_id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            middle_name=data['middle_name'],
            email=data['email'],
            email_code=data['email_code'],
            phone=data['phone'],
            password=make_password(data['password']),
            is_agree_with_save_personal_data=data['is_agree_with_save_personal_data'],
            api_key=helper.generate_api_key(),
            is_admin=data['is_admin'],
        )

        user.save()

        return user

    def update(self, user, data):
        if self.is_password_exists(data['password']):
            data['password'] = make_password(data['password'])
        else:
            data['password'] = user.password

        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.middle_name = data['middle_name']
        user.email = data['email']
        user.phone = data['phone']
        user.password = data['password']

        user.save()

        return user

    def is_password_exists(self, password):
        if password:
            return True

        return False

    def update_api_key(self, api_key):
        user = self.get(api_key=api_key)

        user.api_key = helper.generate_api_key()

        user.save()

        return user.api_key


class User(models.Model):
    hash_id = models.CharField(max_length=16, db_index=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    company_hash_id = models.CharField(max_length=16, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(blank=True, max_length=100)
    middle_name = models.CharField(blank=True, max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=50, unique=True)
    """ минимальное значение пароля 6 символо, сделать проверку в форме, 
    потому что для модели не работает 
    """
    password = models.CharField(max_length=255)
    is_agree_with_save_personal_data = models.BooleanField()
    api_key = models.CharField(max_length=255, db_index=True)
    is_confirmed_email = models.BooleanField(default=False)
    is_confirmed_phone = models.BooleanField(default=False)
    is_admin = models.BooleanField(db_index=True, blank=True, default=False)
    email_code = models.CharField(max_length=255, null=True)
    phone_code = models.PositiveIntegerField(default=0)
    password_code = models.CharField(max_length=255, default='')

    class Meta:
        db_table = 'user'

    manager = UserManager()
