import json
import os

from django.contrib.postgres.aggregates import ArrayAgg
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.db.models import Max, Min
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import get_object_or_404
from django.views import View

from auth.models import Company
from auth.models import User
from buildings.models import Building, House, FlatSchema, Floor, Flat, FloorType, FlatType
from insider.services import Serialization, Helper
from buildings.forms import BuildingForm, HouseForm, FlatSchemaForm, FloorTypeForm, FlatTypeForm, FlatForm

from insider.settings import PROJECT_ROOT

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

building_form = BuildingForm
house_form = HouseForm
flat_schema_form = FlatSchemaForm
floor_type_form = FloorTypeForm
flat_type_form = FlatTypeForm
flat_form = FlatForm

fs = FileSystemStorage()

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


def create_image_name(image):
    image_extension = os.path.splitext(image.name)[1]
    return helper.create_hash() + image_extension


def save_image_in_dir(name, image):
    fs.save(name, image)


def delete_image_from_dir(path_to_image):
    os.remove(PROJECT_ROOT + path_to_image)


def is_image_exists(name):
    return os.path.exists(PROJECT_ROOT + '/media/' + name)


def decode_from_json_format(data):
    return serialization.json_decode(data)


def encode_objects_in_assigned_format(format, data):
    return serializers.serialize(format, data)


def generate_response(data={}, status=200):
    response = JsonResponse(data=data, status=status, safe=False)
    response['Access-Control-Allow-Origin'] = '*'
    return response


def bind_data_with_form(form, data):
    return form(data)


def fetch_from_db(model, condition):
    return model.objects.get(**condition)


def fetch_all_from_db(model, condition={}):
    return model.objects.filter(**condition)


def delete_from_db(model, condition):
    return model.objects.filter(**condition).delete()


class Building(View):
    def get(self, request, id):
        building = fetch_from_db(model=building_model, condition={'hash_id': id})

        return generate_response(data=model_to_dict(building), status=200)

    def post(self, request):
        data = decode_from_json_format(data=request.body.decode('utf-8'))

        form = bind_data_with_form(form=building_form, data=data)

        if form.is_valid():
            building = self.create_building(data=form.cleaned_data)

            return generate_response(data=model_to_dict(building), status=200)

        return generate_response(data=form.errors, status=400)

    def create_building(self, data):
        company = fetch_from_db(model=company_model, condition={'hash_id': data['company_id']})

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
        data = decode_from_json_format(data=request.body.decode('utf-8'))

        form = bind_data_with_form(form=building_form, data=data)

        if form.is_valid():
            old_building = fetch_from_db(model=building_model, condition={'hash_id': id})

            new_building = self.update_building(building=old_building, data=form.cleaned_data)

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
        delete_from_db(model=building_model, condition={'hash_id': id})

        return generate_response(status=200)


def get_company_buildings(request, id):
    buildings_with_number_of_flats_by_type = []

    buildings = building_model.objects.filter(company_hash_id=id)

    for building in buildings:
        buildings_flats = {}

        flats_by_type = {}

        houses = house_model.objects.filter(building_hash_id=building.hash_id)

        for house in houses:
            flats_schemas = flat_schema_model.objects.filter(house_hash_id=house.hash_id)

            for flat_schema in flats_schemas:
                flats = flat_model.objects.filter(
                    house_hash_id=house.hash_id
                ).filter(
                    flat_schema_hash_id=flat_schema.hash_id
                )

                if flat_schema.type in flats_by_type:
                    flats_by_type[flat_schema.type] += flats.count()
                else:
                    flats_by_type[flat_schema.type] = flats.count()

        buildings_flats['flats_by_type'] = flats_by_type
        buildings_flats['building'] = model_to_dict(building)

        buildings_with_number_of_flats_by_type.append(buildings_flats)

    return generate_response(data=buildings_with_number_of_flats_by_type, status=200)


class House(View):
    def get(self, request, id):
        data = fetch_from_db(model=house_model, condition={'hash_id': id})

        return generate_response(data=model_to_dict(data), status=200)

    def post(self, request):
        data = decode_from_json_format(data=request.body.decode('utf-8'))

        form = bind_data_with_form(form=house_form, data=data)

        if form.is_valid():
            house = self.create_house(data=form.cleaned_data)

            return generate_response(data=model_to_dict(house), status=200)

        return generate_response(data=form.errors, status=400)

    def create_house(self, data):
        building = fetch_from_db(model=building_model, condition={'hash_id': data['building_id']})

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
            start_development=self.get_correct_date(date=data['start_development']),
            end_development=self.get_correct_date(date=data['end_development']),
        )

    def get_correct_date(self, date):
        if date:
            return date

        return None

    def put(self, request, id):
        data = decode_from_json_format(data=request.body.decode('utf-8'))

        form = bind_data_with_form(form=house_form, data=data)

        if form.is_valid():
            old_house = fetch_from_db(model=house_model, condition={'hash_id': id})

            new_house = self.update_house(house=old_house, data=form.cleaned_data)

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
        delete_from_db(model=house_model, condition={'hash_id': id})

        return generate_response(status=200)


def get_building_houses(request, id):
    houses = fetch_all_from_db(
        model=house_model,
        condition={'building_hash_id': id}
    )

    houses_flats = []
    for house in houses:
        flat_schemas = flat_schema_model.objects.filter(house_hash_id=house.hash_id)
        flats = flat_model.objects.filter(house_hash_id=house.hash_id)

        number_of_flats_by_type = []

        if not flat_schemas or not flats:
            return number_of_flats_by_type

        flats_by_type = {
            'house': model_to_dict(house),
            'flats': get_flats_with_number_of_by_type(flat_schemas, flats)
        }

        houses_flats.append(flats_by_type)

    return generate_response(data=houses_flats, status=200)


class FlatSchema(View):
    def get(self, request, id):
        flats_schemas = fetch_from_db(model=flat_schema_model, condition={'hash_id': id})

        return generate_response(data=model_to_dict(flats_schemas), status=200)

    def post(self, request):
        form = bind_data_with_form(form=flat_schema_form, data=request.POST)

        if form.is_valid():
            if request.FILES:
                image_name = create_image_name(image=request.FILES['image'])
                save_image_in_dir(name=image_name, image=request.FILES['image'])
                form.cleaned_data['image'] = '/media/' + image_name
            else:
                form.cleaned_data['image'] = ''

            flat_schema = self.create_flat_schema(data=form.cleaned_data)

            return generate_response(data=model_to_dict(flat_schema), status=200)

        return generate_response(data=form.errors, status=400)

    def create_flat_schema(self, data):
        house = fetch_from_db(model=house_model, condition={'hash_id': data['house_id']})

        return flat_schema_model.objects.create(
            hash_id=helper.create_hash(),
            house=house,
            house_hash_id=house.hash_id,
            type=data['type'],
            image=data['image'],
            number_of_balcony=data['number_of_balcony'],
            number_of_loggia=data['number_of_loggia'],
            number_of_romms=data['number_of_rooms'],
            area=data['area'],
            price=data['price'],
        )

    def put(self, request, id):
        if request.content_type.startswith('multipart'):
            data, files = request.parse_file_upload(request.META, request)
            flat_schema = data.dict()
        else:
            files = False
            flat_schema = QueryDict(request.body).dict()

        form = bind_data_with_form(form=flat_schema_form, data=flat_schema)

        if form.is_valid():
            old_flat_schema = fetch_from_db(model=flat_schema_model, condition={'hash_id': id})

            if files:
                delete_image_from_dir(old_flat_schema.image)
                image_name = create_image_name(image=files['image'])
                save_image_in_dir(name=image_name, image=files['image'])
                form.cleaned_data['image'] = '/media/' + image_name
            else:
                form.cleaned_data['image'] = old_flat_schema.image

            new_flat_schema = self.update_flat_schema(flat_schema=old_flat_schema, data=form.cleaned_data)

            return generate_response(data=model_to_dict(new_flat_schema), status=200)

        return generate_response(data=form.errors, status=400)

    def update_flat_schema(self, flat_schema, data):
        flat_schema.type = data['type']
        flat_schema.image = data['image']
        flat_schema.number_of_balcony = data['number_of_balcony']
        flat_schema.number_of_loggia = data['number_of_loggia']
        flat_schema.number_of_rooms = data['number_of_rooms'],
        flat_schema.area = data['area']
        flat_schema.price = data['price']

        flat_schema.save()

        return flat_schema

    def delete(self, request, id):
        flat_schema = flat_schema_model.objects.get(hash_id=id)

        if flat_schema.image:
            delete_image_from_dir(flat_schema.image)

        flat_schema.delete()

        return generate_response(status=200)


def get_house_ftats_schemas(request, id):
    data = fetch_all_from_db(model=flat_schema_model, condition={'house_hash_id': id})

    return generate_response(
        data=encode_objects_in_assigned_format(format='json', data=data),
        status=200
    )


class FloorType(View):
    def get(self, request, id):
        floor_type = fetch_from_db(model=floor_type_model, condition={'hash_id': id})

        return generate_response(data=model_to_dict(floor_type))

    def post(self, request):
        form = bind_data_with_form(form=floor_type_form, data=request.POST)

        if form.is_valid():

            if request.FILES:
                image_name = create_image_name(image=request.FILES['image'])
                save_image_in_dir(name=image_name, image=request.FILES['image'])
                form.cleaned_data['image'] = '/media/' + image_name
            else:
                form.cleaned_data['image'] = ''

            floor_type = self.create_floor_type(data=form.cleaned_data)

            return generate_response(data=model_to_dict(floor_type), status=200)

        return generate_response(data=form.errors, status=400)

    def create_floor_type(self, data):
        with transaction.atomic():
            house = fetch_from_db(model=house_model, condition={'hash_id': data['house_id']})

            floor_type = floor_type_model.objects.create(
                hash_id=helper.create_hash(),
                house=house,
                house_hash_id=house.hash_id,
                number=data['number'],
                clone_floors=data['clone_floors'],
                image=data['image'],
                number_of_flats=data['number_of_flats']
            )

            floors_numbers = self.create_floors_numbers(data)

            floors = (floor_model(
                hash_id=helper.create_hash(),
                house=house,
                house_hash_id=house.hash_id,
                floor_type=floor_type,
                floor_type_hash_id=floor_type.hash_id,
                number='%s' % floor_number
            ) for floor_number in floors_numbers)

            floor_model.objects.bulk_create(floors)

            return floor_type

    def create_floors_numbers(self, data):
        new_clone_floors = []

        if data['clone_floors']:
            new_clone_floors = data['clone_floors'].split(',')

        new_clone_floors.insert(0, data['number'])

        return new_clone_floors

    def put(self, request, id):
        if request.content_type.startswith('multipart'):
            data, files = request.parse_file_upload(request.META, request)
            floor_type = data.dict()
        else:
            files = False
            floor_type = QueryDict(request.body).dict()

        form = bind_data_with_form(form=floor_type_form, data=floor_type)

        if form.is_valid():
            old_floor_type = fetch_from_db(model=floor_type_model, condition={'hash_id': id})

            if files:
                delete_image_from_dir(old_floor_type.image)
                image_name = create_image_name(image=files['image'])
                save_image_in_dir(name=image_name, image=files['image'])
                form.cleaned_data['image'] = '/media/' + image_name
            else:
                form.cleaned_data['image'] = old_floor_type.image

            new_floor_type = self.update_floor_type(data=form.cleaned_data, id=id)

            return generate_response(data=model_to_dict(new_floor_type), status=200)

        return generate_response(data=form.errors, status=400)

    def update_floor_type(self, data, id):
        with transaction.atomic():
            delete_from_db(model=floor_type_model, condition={'hash_id': id})

            house = fetch_from_db(model=house_model, condition={'hash_id': data['house_id']})

            floor_type = floor_type_model.objects.create(
                hash_id=helper.create_hash(),
                house=house,
                house_hash_id=house.hash_id,
                image=data['image'],
                number=data['number'],
                clone_floors=data['clone_floors'],
                number_of_flats=data['number_of_flats']
            )

            floors = (floor_model(
                hash_id=helper.create_hash(),
                house=house,
                house_hash_id=house.hash_id,
                floor_type=floor_type,
                floor_type_hash_id=floor_type.hash_id,
                number='%s' % number
            ) for number in data['clone_floors'].split(','))

            floor_model.objects.bulk_create(floors)

            return floor_type

    def delete(self, request, id):
        floor_type = floor_type_model.objects.get(hash_id=id)

        if floor_type.image:
            delete_image_from_dir(floor_type.image)

        floor_type.delete()

        return generate_response(status=200)


def get_house_floor_types(request, id):
    floor_types = floor_type_model.objects.filter(house_hash_id=id)
    flat_types = flat_type_model.objects.filter(house_hash_id=id)

    floor_types_with_marking_enable = []

    if floor_types:
        previous_floor_type_hash_id = floor_types.first().hash_id
        for floor_type in floor_types.values():
            number_of_marked_flats_on_previous_floor = flat_types.filter(
                floor_type_hash_id=previous_floor_type_hash_id
            ).count()

            number_of_flats_on_previous_floor_type = floor_types.filter(
                hash_id=previous_floor_type_hash_id
            )[0].number_of_flats

            if number_of_flats_on_previous_floor_type == number_of_marked_flats_on_previous_floor:
                floor_type['marking_enable'] = True
            else:
                floor_type['marking_enable'] = False

            if floor_type['number'] == 1:
                floor_type['marking_enable'] = True

            previous_floor_type_hash_id = floor_type['hash_id']

            floor_types_with_marking_enable.append(floor_type)

    return generate_response(
        data=floor_types_with_marking_enable,
        status=200
    )


class FlatType(View):
    def get(self, request, id):
        flat_type = flat_model.objects.filter(flat_type__hash_id=id).first()

        return generate_response(data=model_to_dict(flat_type), status=200)

    def post(self, request):
        data = decode_from_json_format(data=request.body.decode('utf-8'))

        form = bind_data_with_form(form=flat_type_form, data=data)

        if form.is_valid():
            floor_types = floor_type_model.objects.filter(house_hash_id=form.cleaned_data['house_id'])

            flat_types = flat_type_model.objects.filter(
                house_hash_id=form.cleaned_data['house_id']
            )

            flats = flat_model.objects.filter(house_hash_id=data['house_id'])

            # Если нет ни одной квартиры, то создавай без валидации
            if not flats:
                flat_type = self.create_flat_type(form.cleaned_data)
                return generate_response(data=model_to_dict(flat_type), status=200)

            # Если не валидный номер подъезда, то выдай ошибку
            if not self.valid_entrance(flat_types, form.cleaned_data):
                return generate_response(
                    data={'message': ['Размечайте подъезды по очерёдно']},
                    status=400
                )

            # Если на этом этаже больше квартир чем должно быть.
            if not self.is_exists_available_flats_for_marking(floor_types, flat_types, form.cleaned_data):
                return generate_response(
                    data={'message': ['Нельзя разметить больше квартир, чем должно быть на этаже']},
                    status=400
                )

            # Если квартира с таким номером уже существует, то выдай ошибку.
            if self.is_flat_exists(flat_types, form.cleaned_data):
                return generate_response(
                    data={'message': ['Квартира с таким нормером уже существует']},
                    status=400
                )

            # Если не первый этаж и нет квартир на предыдущем этаже, то выдай ошибку.
            if not self.is_first_floor_type(floor_types, form.cleaned_data) and not self.is_exists_flats_on_pevious_floor(floor_types, flats, form.cleaned_data):
                return generate_response(
                    data={'message': ['Для разметки этого этажа нужно разметить предыдущий']},
                    status=400
                )

            # Если не первый типовой этаж и на предыдущем размеченны не все, то выдай ошибку.
            if not self.is_first_floor_type(floor_types, form.cleaned_data) and not self.is_marked_previous_floor(floor_types, flat_types, flats, form.cleaned_data):
                return generate_response(
                    data={'message': ['Для разметки этого этажа нужно разметить предыдущий']},
                    status=400
                )

            # Если на этаже нет ни одной, то создай без проверки на последовательность.
            if not self.is_exists_flats_on_floor_in_entrance(flat_types, form.cleaned_data):
                flat_type = self.create_flat_type(form.cleaned_data)
                return generate_response(data=model_to_dict(flat_type), status=200)

            # Если номер квартиры не равен номеру последней квартиры на этаже плюс один, то выдай ошибку.
            if not self.is_flat_number_by_order(flat_types, form.cleaned_data):
                return generate_response(
                    data={'message': ['Номера квартир на этаже должны идти по порядку']},
                    status=400
                )

            flat_type = self.create_flat_type(form.cleaned_data)

            return generate_response(data=model_to_dict(flat_type), status=200)

        return generate_response(data=form.errors, status=400)

    def valid_entrance(self, flat_types, data):
        entrance_last_flat_on_floor = flat_types.filter(
            floor_type_hash_id=data['floor_type_id']
        )

        if not entrance_last_flat_on_floor:
            return True

        current_entrance = data['entrance']

        if abs(entrance_last_flat_on_floor.last().entrance - current_entrance) > 1:
            return False
        return True

    def is_exists_available_flats_for_marking(self, floor_types, flat_types, data):
        max_number_of_flats = floor_types.filter(hash_id=data['floor_type_id'])[0].number_of_flats
        current_number_of_makred_flats = flat_types.filter(floor_type_hash_id=data['floor_type_id']).count()

        if current_number_of_makred_flats >= max_number_of_flats:
            return False
        return True

    def is_exists_flats_on_pevious_floor(self, floor_types, flats, data):
        previous_floor = floor_types.filter(hash_id=data['floor_type_id'])[0].number - 1
        flats = flat_model.objects.filter(floor=previous_floor).first()

        if flats:
            return True
        return False

    def is_first_floor_type(self, floor_types, data):
        first_floor_type_number = floor_types.filter(
            house_hash_id=data['house_id']
        ).aggregate(Min('number'))['number__min']

        current_floor_type_number = floor_types.filter(hash_id=data['floor_type_id'])[0].number

        if current_floor_type_number == first_floor_type_number:
            return True
        return False

    def is_marked_previous_entrance(self):
        pass

    def is_marked_previous_floor(self, floor_types, flat_types, flats, data):
        if not flats:
            return True

        if self.is_first_floor_type(floor_types, data):
            return True

        previous_floor = floor_types.filter(hash_id=data['floor_type_id'])[0].number - 1
        hash_id_previous_flat_type = flats.filter(floor=previous_floor).first().flat_type_hash_id
        hash_id_previous_floor_type = flat_types.filter(hash_id=hash_id_previous_flat_type)[0].floor_type_hash_id

        number_of_flats_on_floor = floor_types.filter(hash_id=hash_id_previous_floor_type)[0].number_of_flats
        number_of_marked_flats_on_floor = flats.filter(floor=previous_floor).count()

        if number_of_marked_flats_on_floor >= number_of_flats_on_floor:
            return True
        return False

    def is_flat_exists(self, flat_types, data):
        if flat_types.filter(number=data['number']):
            return True
        return False

    def is_exists_flats_on_floor_in_entrance(self, flat_types, data):
        if flat_types.filter(floor_type_hash_id=data['floor_type_id']).filter(entrance=data['entrance']):
            return True
        return False

    def is_flat_number_by_order(self, flat_types, data):
        last_flat_type_in_entrance = flat_types.filter(entrance=data['entrance']).last()

        if data['number'] == last_flat_type_in_entrance.number + 1:
            return True
        return False

    def create_flat_type(self, data):
        house = fetch_from_db(model=house_model, condition={'hash_id': data['house_id']})

        floor_type = floor_type_model.objects.filter(
            house_hash_id=data['house_id']
        ).filter(
            hash_id=data['floor_type_id']
        ).first()

        clone_floors = []
        if floor_type.clone_floors:
            clone_floors = floor_type.clone_floors.split(',')
        clone_floors.insert(0, floor_type.number)

        flat_schema = fetch_from_db(
            model=flat_schema_model,
            condition={'hash_id': data['flat_schema_id']}
        )

        with transaction.atomic():
            flat_type = flat_type_model.objects.create(
                hash_id=helper.create_hash(),
                house=house,
                house_hash_id=house.hash_id,
                floor_type=floor_type,
                floor_type_hash_id=floor_type.hash_id,
                flat_schema=flat_schema,
                flat_schema_hash_id=flat_schema.hash_id,
                number=data['number'],
                entrance=data['entrance'],
                coordinates=data['coordinates'],
            )

            flats_objects = []
            for floor in clone_floors:
                flat_object = flat_model(
                    hash_id=helper.create_hash(),
                    house=house,
                    house_hash_id=house.hash_id,
                    flat_schema=flat_schema,
                    flat_schema_hash_id=flat_schema.hash_id,
                    flat_type=flat_type,
                    flat_type_hash_id=flat_type.hash_id,
                    entrance=data['entrance'],
                    number=data['number'],
                    price=flat_schema.price,
                    area=flat_schema.area,
                    windows=data['windows'],
                    status=1,
                    floor=floor
                )

                data['number'] = 0

                flats_objects.append((
                    flat_object
                ))

            flat = flat_model.objects.bulk_create(flats_objects)

        return flat[0]

    def put(self, request, id):
        data = decode_from_json_format(data=request.body.decode('utf-8'))

        form = bind_data_with_form(form=flat_type_form, data=data)

        if form.is_valid():
            house = house_model.objects.filter(hash_id=form.cleaned_data['house_id']).first()
            floor_types = floor_type_model.objects.filter(house_hash_id=form.cleaned_data['house_id'])
            flat_types = flat_type_model.objects.filter(house_hash_id=form.cleaned_data['house_id'])
            flats = flat_model.objects.filter(house_hash_id=form.cleaned_data['house_id'])

            if self.is_house_marked(flats):

                if not self.is_edit_first_flat(flat_types, id):
                    return generate_response(
                        data={'message': ['Для автоматической перенумерации измените номер 1-ой квартиры.']},
                        status=400
                    )

                flat_type_number = form.cleaned_data['number']
                flat_last_new_number = 0
                for entrance in range(1, house.number_of_entrance + 1):
                    for floor_type in floor_types:
                        clone_floors = []
                        if floor_type.clone_floors:
                            clone_floors = floor_type.clone_floors.split(',')
                        clone_floors.insert(0, floor_type.number)

                        flat_types_in_entrance = flat_types.filter(
                            floor_type_hash_id=floor_type.hash_id
                        ).filter(
                            entrance=entrance
                        )

                        if floor_type.number > floor_types.first().number or entrance > 1:
                            flat_type_number = flat_last_new_number + 1

                        for flat_type in flat_types_in_entrance:
                            flat_type.number = flat_type_number
                            flat_type.save()
                            flat_type_number += 1

                            flat_number = flat_type.number

                            number_of_flats_on_floor_type_in_entrance = flat_types_in_entrance.count()

                            flat_type_flats = flats.filter(flat_type_hash_id=flat_type.hash_id)
                            for flat in flat_type_flats:
                                flat.number = flat_number
                                flat.save()
                                flat_number += number_of_flats_on_floor_type_in_entrance
                                flat_last_new_number = flat.number

                return generate_response(data={}, status=200)
            else:
                floor_types = floor_type_model.objects.filter(
                    house_hash_id=form.cleaned_data['house_id']
                )

                old_flat_type = flat_types.filter(hash_id=id).first()
                new_flat_type_number = form.cleaned_data['number']
                new_flat_type_entrance = form.cleaned_data['entrance']

                if old_flat_type.number != new_flat_type_number:
                    # Если квартира с таким номером уже существует, то выдай ошибку.
                    if self.is_flat_exists(flat_types, form.cleaned_data):
                        return generate_response(
                            data={'message': ['Квартира с таким нормером уже существует']},
                            status=400
                        )

                if old_flat_type.entrance != new_flat_type_entrance:
                    # Если не валидный номер подъезда, то выдай ошибку
                    if not self.valid_entrance(flat_types, form.cleaned_data):
                        return generate_response(
                            data={'message': ['Размечайте подъезды по очереди']},
                            status=400
                        )

                # Если на этом этаже больше квартир чем должно быть.
                if not self.is_exists_available_flats_for_marking(floor_types, flat_types, form.cleaned_data):
                    return generate_response(
                        data={'message': ['Нельзя разметить больше квартир, чем должно быть на этаже']},
                        status=400
                    )

                # Если не первый этаж и нет квартир на предыдущем этаже, то выдай ошибку.
                if not self.is_first_floor_type(floor_types, form.cleaned_data) and not self.is_exists_flats_on_pevious_floor(floor_types, flats, form.cleaned_data):
                    return generate_response(
                        data={'message': ['Для разметки этого этажа нужно разметить предыдущий']},
                        status=400
                    )

                # Если не первый этаж и на предыдущем размеченны не все, то выдай ошибку.
                if not self.is_first_floor_type(floor_types, form.cleaned_data) and not self.is_marked_previous_floor(floor_types, flat_types, flats, form.cleaned_data):
                    return generate_response(
                        data={'message': ['Для разметки этого этажа нужно разметить предыдущий']},
                        status=400
                    )

                # Если на этаже нет ни одной, то создай без валидации.
                if not self.is_exists_flats_on_floor_in_entrance(flat_types, form.cleaned_data):
                    delete_from_db(model=flat_type_model, condition={'hash_id': id})
                    flat_type = self.create_flat_type(form.cleaned_data)
                    return generate_response(data=model_to_dict(flat_type), status=200)

                # Если номер квартиры не равен номеру последней квартиры на этаже плюс один, то выдай ошибку.
                flat_type_on_delete = flat_types.filter(entrance=data['entrance']).last().number
                last_flat_type_in_entrance = flat_types.filter(
                    entrance=data['entrance']
                ).filter(number=flat_type_on_delete - 1).first()

                if form.cleaned_data['number'] != last_flat_type_in_entrance.number + 1:
                    return generate_response(
                        data={'message': ['Номера квартир на этаже должны идти по порядку']},
                        status=400
                    )

                flat_types.filter(hash_id=id).delete()

                flat_type = self.create_flat_type(form.cleaned_data)

            return generate_response(data=model_to_dict(flat_type), status=200)

        return generate_response(data=form.errors, status=400)

    def is_house_marked(self, flats):
        if flats.filter(number=0):
            return False
        return True

    def is_edit_first_flat(self, flat_types, id):
        if flat_types.first() == flat_types.filter(hash_id=id).first():
            return True
        return False

    def delete(self, request, id):
        delete_from_db(model=flat_type_model, condition={'hash_id': id})

        return generate_response(status=200)


def get_floor_type_flat_types(request, id):
    flats_types = fetch_all_from_db(model=flat_type_model, condition={'floor_type_hash_id': id})

    return generate_response(
        data=encode_objects_in_assigned_format(format='json', data=flats_types),
        status=200
    )


def numbering_flats(request):
    data = serialization.json_decode(request.body.decode('utf-8'))

    with transaction.atomic():
        flats = fetch_all_from_db(
            model=flat_model,
            condition={'house_hash_id': data['house_id']}
        )

        number_of_entrance = flats.values('entrance').distinct().count() + 1
        floor_types = floor_type_model.objects.filter(house_hash_id=data['house_id'])

        for entrance in range(1, number_of_entrance):
            for floor_type in floor_types:
                floors = []
                if floor_type.clone_floors:
                    floors = floor_type.clone_floors.split(',')
                floors.insert(0, str(floor_type.number))

                for floor in floors:
                    if int(floor) == 1:
                        previous_floor = 1
                    else:
                        previous_floor = int(floor) - 1

                    last_flat_number = flats.filter(entrance=entrance).filter(floor=previous_floor).last().number
                    flats_in_entrance_on_floor = flats.filter(entrance=entrance).filter(floor=floor)

                    for flat in flats_in_entrance_on_floor:
                        if flat.number:
                            flat.number = flat.number
                            flat.save()
                        else:
                            last_flat_number += 1
                            flat.number = last_flat_number
                            flat.save()

    return JsonResponse({}, status=200)


def get_house_flats(request, id):
    flat_schemas = flat_schema_model.objects.filter(house_hash_id=id)
    flats = flat_model.objects.filter(house_hash_id=id)

    flats_with_number_of_by_type = {}

    if not flat_schemas or not flats:
        return flats_with_number_of_by_type

    flats_with_number_of_by_type['flats'] = get_flats_by_floor(flat_schemas, flats)
    flats_with_number_of_by_type['number_of_flats_by_type'] = get_flats_with_number_of_by_type(flat_schemas, flats)

    return generate_response(data=flats_with_number_of_by_type, status=200)


def get_flats_by_floor(flat_schemas, flats):
    flats_by_floor = []

    max_floor = flats.aggregate(Max('floor'))['floor__max']
    min_floor = flats.aggregate(Min('floor'))['floor__min']

    for floor in range(min_floor, max_floor + 1):
        flats_floor = []

        for flat in flats.filter(floor=floor).values():
            flat_schema = flat_schemas.filter(
                hash_id=flat['flat_schema_hash_id']
            ).first()

            flat['number_of_rooms'] = flat_schema.number_of_rooms
            flat['flat_schema'] = flat_schema.type

            flats_floor.append(flat)

        flats_by_floor.append(flats_floor)

    return flats_by_floor


def get_flats_with_number_of_by_type(flat_schemas, flats):
    number_of_flats_by_type = []

    for flat_schema in flat_schemas:
        number_of_flats = flats.filter(flat_schema_hash_id=flat_schema.hash_id).count()

        number_of_flat_by_type = {
            'type': flat_schema.type,
            'number_of': number_of_flats
        }

        number_of_flats_by_type.append(number_of_flat_by_type)

    return number_of_flats_by_type


class Flat(View):
    # def get(self, request):
    #     flat = serializers.serialize('json', flat_model.manager.all())
    #
    #     return JsonResponse(flat, status=200, safe=False)

    # def post(self, request):
    #     data = serialization.json_decode(request.body.decode('utf-8'))
    #
    #     house = house_model.manager.get(hash_id=data['house_id'])
    #     data['house'] = house
    #     data['house_hash_id'] = house.hash_id
    #
    #     floor = floor_model.manager.get(hash_id=data['floor_id'])
    #     data['floor'] = floor
    #     data['floor_hash_id'] = floor.hash_id
    #
    #     flat_schema = flat_schema_model.manager.get(hash_id=data['planing_id'])
    #     data['flat_schema'] = flat_schema
    #     data['flat_schema_hash_id'] = flat_schema.hash_id
    #
    #     flat = flat_model.manager.create(data)
    #
    #     response = JsonResponse(model_to_dict(flat), status=200)
    #     response['Access-Control-Allow-Origin'] = '*'
    #     return response

    def put(self, request, id):
        data = decode_from_json_format(data=request.body.decode('utf-8'))

        form = bind_data_with_form(form=flat_form, data=data)

        if form.is_valid():
            old_flat = get_object_or_404(flat_model, hash_id=id)

            new_flat = self.update_flat(old_flat, data)

            return generate_response(data=model_to_dict(new_flat), status=200)

        return generate_response(data=form.errors, status=400)

    def update_flat(self, old_flat, data):
        old_flat.price = data['price']
        old_flat.status = data['status']
        old_flat.area = data['area']
        old_flat.save()
        return old_flat

    # def delete(self, request, id):
    #     flat_model.manager.filter(hash_id=id).delete()
    #
    #     return HttpResponse(status=200, reason='OK')