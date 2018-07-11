import json
import random
import sys
from uuid import uuid4

from django.core.exceptions import SuspiciousOperation, ValidationError
from django.http import HttpResponse
from django.middleware.csrf import _get_new_csrf_string, _salt_cipher_secret


class Serialization:
    def json_decode(self, data):
        return json.loads(data)

    def json_encode(self, data):
        return json.dumps(data)


class Deserialization:
    def json_decode(self, data):
        return json.loads(data)


class Validation:
    def validate(self, object):
        try:
            object.full_clean()
        except ValidationError:
            raise SuspiciousOperation()


class Helper:
    def create_hash(self):
        hash = str(uuid4())

        return hash.split('-')[0]