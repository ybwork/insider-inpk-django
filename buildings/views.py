import random

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.db import transaction, DatabaseError
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.views import View

from auth.models import Company
from auth.models import User
from buildings.models import Building, House, FlatSchema, Floor, Flat, FloorType, FlatType, FloorTypeEntrance
from insider.services import Serialization, Helper
from buildings.forms import BuildingForm, HouseForm, FlatSchemaForm

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
floor_type_entrance_model = FloorTypeEntrance

building_form = BuildingForm
house_form = HouseForm
flat_schema_form = FlatSchemaForm

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


def decode(data):
    return serialization.json_decode(data)


def encode(format, data):
    return serializers.serialize(format, data)


def generate_response(data={}, status=200):
    response = JsonResponse(data=data, status=status, safe=False)
    response['Access-Control-Allow-Origin'] = '*'
    return response


def bind_data_with_form(form, data):
    return form(data)


def fetch_from_db(model, **condition):
    return model.objects.get(**condition)


def fetch_all_from_db(model, condition={}):
    return model.objects.filter(**condition)


def delete_from_db(model, **condition):
    result = model.objects.filter(**condition).delete()

    if result[0]:
        return result
    raise SomethingWentWrong()


class SomethingWentWrong(Exception):
    pass


class Building(View):
    def get(self, request, id):
        building = fetch_from_db(building_model, **{'hash_id': id})

        return generate_response(data=model_to_dict(building), status=200)

    def post(self, request):
        data = decode(request.body)

        form = bind_data_with_form(building_form, data)

        if form.is_valid():
            building = self.create_building(form.cleaned_data)
            return generate_response(data=model_to_dict(building), status=200)

        return generate_response(data=form.errors, status=400)

    def create_building(self, data):
        company = fetch_from_db(company_model, **{'hash_id': data['company_id']})

        return building_model.objects.create(
            hash_id=helper.create_hash(),
            company=company,
            company_hash_id=company.hash_id,
            name=data['name'],
            region=data['region'],
            district=data['district'],
            city=data['city'],
            country=data['country'],
            images=data['images'],
            video=data['video'],
            coordinates=data['coordinates'],
            currency=data['currency'],
        )

    def put(self, request, id):
        data = decode(request.body)

        form = bind_data_with_form(building_form, data)

        if form.is_valid():
            old_building = fetch_from_db(building_model, **{'hash_id': id})

            new_building = self.update_building(old_building, form.cleaned_data)

            return generate_response(data=model_to_dict(new_building), status=200)

        return generate_response(data=form.errors, status=400)

    def update_building(self, building, data):
        building.name = data['name']
        building.region = data['region']
        building.district = data['district']
        building.city = data['city']
        building.country = data['country']
        building.images = data['images']
        building.video = data['video']
        building.coordinates = data['coordinates']
        building.currency = data['currency']

        building.save()

        return building

    def delete(self, request, id):
        try:
            delete_from_db(building_model, **{'hash_id': id})
            return generate_response(status=200)
        except SomethingWentWrong:
            return generate_response(status=500)


def get_company_buildings(request, id):
    data = fetch_all_from_db(
        model=building_model,
        condition={'company_hash_id': id}
    )

    company_buildings = encode(format='json', data=data)

    return generate_response(data=company_buildings, status=200)


class House(View):
    def get(self, request, id):
        house = fetch_from_db(house_model, **{'hash_id': id})

        return generate_response(data=model_to_dict(house), status=200)

    def post(self, request):
        data = decode(request.body)

        form = bind_data_with_form(house_form, data)

        if form.is_valid():
            house = self.create_house(form.cleaned_data)
            return generate_response(data=model_to_dict(house), status=200)

        return generate_response(data=form.errors, status=400)

    def create_house(self, data):
        building = fetch_from_db(building_model, **{'hash_id': data['building_id']})

        return house_model.objects.create(
            hash_id=helper.create_hash(),
            building=building,
            building_hash_id=building.hash_id,
            living_floors=data['living_floors'],
            number_of_floors=data['number_of_floors'],
            number_of_entrance=data['number_of_entrance'],
            number_of_flat=data['number_of_flat'],
            street_name=data['street_name'],
            number=data['number'],
            finishing=data['finishing'],
            materials=data['materials'],
            stage_development=data['stage_development'],
            start_development=self.get_correct_date(data['start_development']),
            end_development=self.get_correct_date(data['end_development']),
        )

    def get_correct_date(self, date):
        if date:
            return date
        return None

    def put(self, request, id):
        data = decode(request.body)

        form = bind_data_with_form(house_form, data)

        if form.is_valid():
            old_house = fetch_from_db(house_model, **{'hash_id': id})

            new_house = self.update_house(old_house, form.cleaned_data)

            return generate_response(data=model_to_dict(new_house), status=200)

        return generate_response(data=form.errors, status=400)

    def update_house(self, house, data):
        house.number_of_floors = data['number_of_floors']
        house.living_floors = data['living_floors']
        house.number_of_entrance = data['number_of_entrance']
        house.number_of_flat = data['number_of_flat']
        house.street_name = data['street_name']
        house.number = data['number']
        house.finishing = data['finishing']
        house.materials = data['materials']
        house.stage_development = data['stage_development']
        house.start_development = self.get_correct_date(data['start_development'])
        house.end_development = self.get_correct_date(data['end_development'])

        house.save()

        return house

    def delete(self, request, id):
        try:
            delete_from_db(house_model, **{'hash_id': id})
            return generate_response(status=200)
        except SomethingWentWrong:
            return generate_response(status=500)


def get_building_houses(request, id):
    data = fetch_all_from_db(
        model=house_model,
        condition={'building_hash_id': id}
    )

    houses = encode(format='json', data=data)

    return generate_response(data=houses, status=200)

# def get_house_floors(request, id):
#     data = floor_model.manager.filter(house_hash_id=id)
#
#     house_floors = serializers.serialize('json', data)
#
#     return JsonResponse(house_floors, status=200, safe=False)


# def get_house_flats(request, id):
#     data = flat_model.manager.filter(house_hash_id=id)
#
#     house_flats = serializers.serialize('json', data)
#
#     return JsonResponse(house_flats, status=200, safe=False)


class FlatSchema(View):
    def get(self, request, id):
        flats_schemas = fetch_from_db(flat_schema_model, **{'hash_id': id})

        return generate_response(data=model_to_dict(flats_schemas), status=200)

    def post(self, request):
        data = decode(request.body)

        form = bind_data_with_form(flat_schema_form, data)

        if form.is_valid():
            flat_schema = self.create_flat_schema(form.cleaned_data)
            return generate_response(data=model_to_dict(flat_schema), status=200)

        return generate_response(data=form.errors, status=400)

    def create_flat_schema(self, data):
        house = house_model.objects.get(hash_id=data['house_id'])

        return flat_schema_model.objects.create(
            hash_id=helper.create_hash(),
            house=house,
            house_hash_id=house.hash_id,
            type=data['type'],
            image=data['image'],
            number_of_balcony=data['number_of_balcony'],
            number_of_loggia=data['number_of_loggia'],
            area=data['area'],
            price=data['price'],
        )

    def put(self, request, id):
        data = decode(request.body)

        form = bind_data_with_form(flat_schema_form, data)

        if form.is_valid():
            old_flat_schema = fetch_from_db(flat_schema_model, **{'hash_id': id})

            new_flat_schema = self.update_flat_schema(old_flat_schema, form.cleaned_data)

            return generate_response(data=model_to_dict(new_flat_schema), status=200)

        return generate_response(data=form.errors, status=400)

    def update_flat_schema(self, flat_schema, data):
        flat_schema.type = data['type']
        flat_schema.image = data['image']
        flat_schema.number_of_balcony = data['number_of_balcony']
        flat_schema.number_of_loggia = data['number_of_loggia']
        flat_schema.area = data['area']
        flat_schema.price = data['price']

        flat_schema.save()

        return flat_schema

    def delete(self, request, id):
        try:
            delete_from_db(flat_schema_model, **{'hash_id': id})
            return generate_response(status=200)
        except SomethingWentWrong:
            return generate_response(status=500)

# def get_house_ftats_schemas(request, id):
#     data = flat_schema_model.manager.filter(house_hash_id=id)
#
#     house_flats_schemas = serializers.serialize('json', data)
#
#     return JsonResponse(house_flats_schemas, status=200, safe=False)


class FloorType(View):
    def get(self, request):
        floor_types = serializers.serialize(
            'json', floor_type_model.manager.filter(house_hash_id=request.GET['house_id'])
        )

        return JsonResponse(floor_types, status=200, safe=False)

    def post(self, request):
        data = serialization.json_decode(request.body)

        house = house_model.objects.get(hash_id=data['house_id'])

        data['house'] = house
        data['house_hash_id'] = house.hash_id

        with transaction.atomic():
            floor_type = floor_type_model.manager.create(data)
            data['floor_type'] = floor_type
            data['floor_type_hash_id'] = floor_type.hash_id

            entrances = [
                [1, 25],
            ]

            floor_type_entrances = (FloorTypeEntrance(
                hash_id=helper.create_hash(),
                floor_type=floor_type,
                floor_type_hash_id=floor_type.hash_id,
                number='%s' % number,
                number_of_flats='%s' % number_of_flats
            )for number, number_of_flats in entrances)

            floor_type_entrance_model.objects.bulk_create(floor_type_entrances)

            floor_model.manager.multiple_create(data)

        return HttpResponse('good')

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

        return HttpResponse('сформировать ответ, когда фронтендер будет знать, что ему нужно')

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


# class FlatType(View):
#     def get(self, request):
#         return HttpResponse('get flat type')
#
#     def post(self, request):
#         data = serialization.json_decode(request.body)
#         # return HttpResponse(data['number_of_flats_in_entrance'][num]['number_of'])
#
#         # TO DO
#         # len(data['flats'])
#         # self.is_correct_number_of_flats(data)
#
#         flat_type = self.create_flat_type(data)
#
#         return HttpResponse(flat_type)
#
#     def create_flat_type(self, data):
#         with transaction.atomic():
#             house = house_model.objects.get(hash_id=data['house_id'])
#             flat_schema = flat_schema_model.objects.get(hash_id=data['flat_schema_id'])
#             floor_type = floor_type_model.objects.get(hash_id=data['floor_type_id'])
#
#             # flat_type = flat_type_model.objects.create(
#             #     hash_id=helper.create_hash(),
#             #     house=house,
#             #     house_hash_id=house.hash_id,
#             #     floor_type=floor_type,
#             #     floor_type_hash_id=floor_type.hash_id,
#             #     coordinates=data['coordinates'],
#             # )
#
#             # flats = (flat_model(
#             #     hash_id=helper.create_hash(),
#             #     house=house,
#             #     house_hash_id=house.hash_id,
#             #     flat_schema=flat_schema,
#             #     flat_schema_hash_id=flat_schema.hash_id,
#             #     flat_type=flat_type,
#             #     flat_type_hash_id=flat_type.hash_id,
#             #     entrance=data['entrance'],
#             #     number=0,
#             #     area=data['area'],
#             #     price=data['price'],
#             #     windows=data['windows'],
#             #     status=data['status'],
#             #     floor='%s' % floor
#             # )for floor in data['clone_floors'])
#
#             flats_objects = []
#
#             for floor in data['clone_floors']:
#
#                 for flat_type in data['flats']:
#
#                     if floor == data['clone_floors'][0]:
#                         num = flat_type['number']
#                     else:
#                         number_entrance = str(flat_type['entrance'])
#                         number_of_flats_in_entrance = data['number_of_flats_in_entrance'][number_entrance]['number_of']
#                         flat_type['number'] += number_of_flats_in_entrance
#
#                     flat_object = flat_model(
#                         hash_id=helper.create_hash(),
#                         house=house,
#                         house_hash_id=house.hash_id,
#                         flat_schema=flat_schema,
#                         flat_schema_hash_id=flat_schema.hash_id,
#                         # flat_type=flat_type,
#                         # flat_type_hash_id=flat_type.hash_id,
#                         entrance=flat_type['entrance'],
#                         number=flat_type['number'],
#                         area=flat_type['area'],
#                         price=flat_type['price'],
#                         windows=flat_type['windows'],
#                         status=flat_type['status'],
#                         floor=floor,
#                         coordinates=flat_type['coordinates'],
#                     )
#
#                     flats_objects.append((
#                         flat_object
#                     ))
#
#             flat_model.objects.bulk_create(flats_objects)
#
#             return data['clone_floors']
#
#     def put(self, request, id):
#         flat = flat_model.manager.filter(flat_type__hash_id=id).update()
#         return HttpResponse(flat)
#
#     def delete(self, request, id):
#         return HttpResponse('delete flat type')


class FlatType(View):
    def get(self, request):
        return HttpResponse('get flat type')

    def post(self, request):
        data = serialization.json_decode(request.body)

        house = house_model.objects.get(hash_id=data['house_id'])
        data['house'] = house
        data['house_hash_id'] = house.hash_id

        floor_type = floor_type_model.manager.get(hash_id=data['floor_type_id'])
        data['floor_type'] = floor_type
        data['floor_type_hash_id'] = floor_type.hash_id

        flat_schema = flat_schema_model.objects.get(hash_id=data['flat_schema_id'])

        data['flat_schema'] = flat_schema
        data['flat_schema_hash_id'] = flat_schema.hash_id

        with transaction.atomic():
            flat_type = flat_type_model.manager.create(data)

            data['flat_type'] = flat_type
            data['flat_type_hash_id'] = flat_type.hash_id
            print(data['coordinates'])
            print(isinstance(data['coordinates'], str))
            flats = flat_model.manager.multiple_create(data)

        return generate_response(data=model_to_dict(flat_type), status=200)

    def put(self, request, id):
        flat = flat_model.manager.filter(flat_type__hash_id=id).update()
        return HttpResponse(flat)

    def delete(self, request, id):
        return HttpResponse('delete flat type')


# def numbering_flats(request):
#     data = serialization.json_decode(request.body)
#
#     number_flat = 1
#     number_of_entrance = data['number_of_entrance'] + 1
#
#     with transaction.atomic():
#         for entrance in range(1, number_of_entrance):
#
#             for clone_floor in data['clone_floors']:
#                 flats = flat_model.manager.filter(
#                     house_hash_id=data['house_id']
#                 ).filter(
#                     floor=clone_floor
#                 ).filter(
#                     entrance=entrance
#                 )
#
#                 for flat in flats:
#                     flat.number = number_flat
#                     flat.save()
#                     number_flat += 1
#
#     return JsonResponse({}, status=200)

def numbering_flats(request):
    data = serialization.json_decode(request.body)

    with transaction.atomic():
        flats = flat_model.manager.filter(
            house_hash_id=data['house_id']
        )

        number_of_entrance = flats.values('entrance').distinct().count() + 1
        number_first_flat = flats.first().number

        for entrance in range(1, number_of_entrance):
            number_of_flats_in_etrance = data['number_of_flats_in_entrance'][str(entrance)]['number_of']

            flats_by_entrance = flats.filter(entrance=entrance)

            for flat in flats_by_entrance:
                if flat.number:
                    number_first_flat = flat.number

                flat.number = number_first_flat
                flat.save()
                number_first_flat += number_of_flats_in_etrance

    return JsonResponse({}, status=200)