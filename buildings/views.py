from django.contrib.postgres.aggregates import ArrayAgg
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.views import View

from auth.models import Company
from auth.models import User
from buildings.models import Building, House, FlatSchema, Floor, Flat, FloorType, FlatType
from insider.services import Serialization, Helper

serialization = Serialization()
helper = Helper()

company_model = Company
building_model = Building
house_model = House
flat_schema_model = FlatSchema
floor_model = Floor
floor_type_model = FloorType
flat_type_model = FlatType
flat_model = Flat
user_model = User

"""
    company_id = request.user.company_id

    buildings = building_model.manager.values('id').all().filter(company_id=company_id)

    building = [value['id'] for value in buildings]

    if id not in building:
        return HttpResponse(status=403)
"""

"""
    - отправить файлы
    
    - получить файлы
    
    - сжать файлы
    
    - переименовать файлы
    
    - сохранить на диск
    
    fs = FileSystemStorage()
    images = request.FILES.getlist('image[]')
    for image in images:
        fs.save(image.name, image)

    fs = FileSystemStorage()
    file = request.FILES['image']
    fs.save(file.name, file)

    response = HttpResponse(status=200)
    response["Access-Control-Allow-Origin"] = "*"
    return response
"""


class Building(View):
    def get(self, request):
        data = building_model.manager.all()

        buildings = serializers.serialize('json', data)

        response = JsonResponse(buildings, status=200, safe=False)
        response['Access-Control-Allow-Origin'] = '*'
        return response

    def post(self, request):
        data = serialization.json_decode(request.body)

        company = company_model.manager.get(hash_id=data['company_id'])

        data['company'] = company
        data['company_hash_id'] = company.hash_id

        building = building_model.manager.create(data)

        response = JsonResponse(model_to_dict(building), status=200)
        response['Access-Control-Allow-Origin'] = '*'
        return response

    def put(self, request, id):
        data = serialization.json_decode(request.body)

        old_building = building_model.manager.get(hash_id=id)

        new_building = building_model.manager.update(old_building, data)

        response = JsonResponse(model_to_dict(new_building), status=200)
        response['Access-Control-Allow-Origin'] = '*'
        return response

    def delete(self, request, id):
        building_model.manager.filter(hash_id=id).delete()

        response = HttpResponse(status=200)
        response['Access-Control-Allow-Origin'] = '*'
        return response


def get_company_buildings(request, id):
    data = building_model.manager.filter(company_hash_id=id)

    company_buildings = serializers.serialize('json', data)

    response = JsonResponse(company_buildings, status=200, safe=False)
    response['Access-Control-Allow-Origin'] = '*'
    return response


def get_building_houses(request, id):
    data = house_model.manager.select_related().filter(building_hash_id=id)

    building_houses = serializers.serialize('json', data)

    return JsonResponse(building_houses, status=200, safe=False)


class House(View):
    def get(self, request):
        data = house_model.manager.all()

        houses = serializers.serialize('json', data)

        return JsonResponse(houses, status=200, safe=False)

    def post(self, request):
        data = serialization.json_decode(request.body)

        building = building_model.manager.get(hash_id=data['building_id'])

        data['building'] = building
        data['building_hash_id'] = building.hash_id

        house = house_model.manager.create(data)

        response = JsonResponse(model_to_dict(house), status=200)
        response['Access-Control-Allow-Origin'] = '*'
        return response

    def put(self, request, id):
        data = serialization.json_decode(request.body)

        old_house = house_model.manager.get(hash_id=id)

        new_house = house_model.manager.update(old_house, data)

        return JsonResponse(model_to_dict(new_house), status=200, reason='OK')

    def delete(self, request, id):
        house_model.manager.filter(hash_id=id).delete()

        return HttpResponse(status=200, reason='OK')


def get_house_ftats_schemas(request, id):
    data = flat_schema_model.manager.filter(house_hash_id=id)

    house_flats_schemas = serializers.serialize('json', data)

    return JsonResponse(house_flats_schemas, status=200, safe=False)


def get_house_floors(request, id):
    data = floor_model.manager.filter(house_hash_id=id)

    house_floors = serializers.serialize('json', data)

    return JsonResponse(house_floors, status=200, safe=False)


def get_house_flats(request, id):
    data = flat_model.manager.filter(house_hash_id=id)

    house_flats = serializers.serialize('json', data)

    return JsonResponse(house_flats, status=200, safe=False)


class FlatSchema(View):
    def get(self, request):
        flats_schemas = serializers.serialize('json', flat_schema_model.manager.all())

        return JsonResponse(flats_schemas, status=200, safe=False)

    def post(self, request):
        data = serialization.json_decode(request.body)

        house = house_model.manager.get(hash_id=data['house_id'])

        data['house'] = house
        data['house_hash_id'] = house.hash_id

        flat_schema = flat_schema_model.manager.create(data)

        response = JsonResponse(model_to_dict(flat_schema), status=200)
        response['Access-Control-Allow-Origin'] = '*'
        return response

    def put(self, request, id):
        data = serialization.json_decode(request.body)

        old_flat_schema = flat_schema_model.manager.get(hash_id=id)

        new_flat_schema = flat_schema_model.manager.update(old_flat_schema, data)

        return JsonResponse(model_to_dict(new_flat_schema), status=200, reason='OK')

    def delete(self, request, id):
        flat_schema_model.manager.filter(hash_id=id).delete()

        return HttpResponse(status=200, reason='OK')


class FloorType(View):
    def get(self, request):
        floor_types = serializers.serialize(
            'json', floor_type_model.manager.filter(house_hash_id=request.GET['house_id'])
        )

        return JsonResponse(floor_types, status=200, safe=False)

    def post(self, request):
        data = serialization.json_decode(request.body)

        house = house_model.manager.get(hash_id=data['house_id'])

        data['house'] = house
        data['house_hash_id'] = house.hash_id

        with transaction.atomic():
            floor_type = floor_type_model.manager.create(data)
            data['floor_type'] = floor_type
            data['floor_type_hash_id'] = floor_type.hash_id

            floor_model.manager.multiple_create(data)

        return HttpResponse('сформировать ответ, когда это козёл фронтендер будет знать, что ему нужно')

    def put(self, request, id):
        data = serialization.json_decode(request.body)

        with transaction.atomic():
            floor_type_model.manager.filter(hash_id=id).delete()

            house = house_model.manager.get(hash_id=data['house_id'])
            data['house'] = house
            data['house_hash_id'] = house.hash_id

            floor_type = floor_type_model.manager.create(data)
            data['floor_type'] = floor_type
            data['floor_type_hash_id'] = floor_type.hash_id

            floor_model.manager.multiple_create(data)

        return HttpResponse(' сформировать ответ, когда это козёл фронтендер будет знать, что ему нужно')

    def delete(self, request, id):
        floor_type_model.manager.filter(hash_id=id).delete()

        return HttpResponse(status=200, reason='OK')


class Flat(View):
    def get(self, request):
        flat = serializers.serialize('json', flat_model.manager.all())

        return JsonResponse(flat, status=200, safe=False)

    def post(self, request):
        data = serialization.json_decode(request.body)

        house = house_model.manager.get(hash_id=data['house_id'])
        data['house'] = house
        data['house_hash_id'] = house.hash_id

        floor = floor_model.manager.get(hash_id=data['floor_id'])
        data['floor'] = floor
        data['floor_hash_id'] = floor.hash_id

        flat_schema = flat_schema_model.manager.get(hash_id=data['planing_id'])
        data['flat_schema'] = flat_schema
        data['flat_schema_hash_id'] = flat_schema.hash_id

        flat = flat_model.manager.create(data)

        response = JsonResponse(model_to_dict(flat), status=200)
        response['Access-Control-Allow-Origin'] = '*'
        return response

    def put(self, request, id):
        data = serialization.json_decode(request.body)

        old_flat = flat_model.manager.get(hash_id=id)

        new_flat = flat_model.manager.update(old_flat, data)

        return JsonResponse(model_to_dict(new_flat), status=200, reason='OK')

    def delete(self, request, id):
        flat_model.manager.filter(hash_id=id).delete()

        return HttpResponse(status=200, reason='OK')


class FlatType(View):
    def get(self, request):
        return HttpResponse('get flat type')

    def post(self, request):
        data = serialization.json_decode(request.body)

        house = house_model.manager.get(hash_id=data['house_id'])
        data['house'] = house
        data['house_hash_id'] = house.hash_id

        floor_type = floor_type_model.manager.get(hash_id=data['floor_type_id'])
        data['floor_type'] = floor_type
        data['floor_type_hash_id'] = floor_type.hash_id

        flat_schema = flat_schema_model.manager.get(hash_id=data['flat_schema_id'])
        data['flat_schema'] = flat_schema
        data['flat_schema_hash_id'] = flat_schema.hash_id

        with transaction.atomic():
            flat_type = flat_type_model.manager.create(data)
            data['flat_type'] = flat_type
            data['flat_type_hash_id'] = flat_type.hash_id

            flats = flat_model.manager.multiple_create(data)

        return HttpResponse(flats)

    def put(self, request, id):
        flat = flat_model.manager.filter(flat_type__hash_id=id).update()
        return HttpResponse(flat)

    def delete(self, request, id):
        return HttpResponse('delete flat type')


def numbering_flats(request):
    data = serialization.json_decode(request.body)

    number_flat = 1
    number_of_entrance = data['number_of_entrance'] + 1

    with transaction.atomic():
        for entrance in range(1, number_of_entrance):

            for clone_floor in data['clone_floors']:
                flats = flat_model.manager.filter(
                    house_hash_id=data['house_id']
                ).filter(
                    floor=clone_floor
                ).filter(
                    entrance=entrance
                )

                for flat in flats:
                    flat.number = number_flat
                    flat.save()
                    number_flat += 1

    return JsonResponse({}, status=200)