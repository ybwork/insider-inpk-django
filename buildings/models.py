from django.db import models
from auth.models import Company
from insider.services import Validation, Helper

validation = Validation()
helper = Helper()


class BuildingManager(models.Manager):
    def create(self, data):
        building = self.model(
            hash_id=helper.create_hash(),
            company=data['company'],
            company_hash_id=data['company_hash_id'],
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

        building.save()

        return building

    def update(self, building, data):
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


class Building(models.Model):
    hash_id = models.CharField(max_length=16, db_index=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    company_hash_id = models.CharField(max_length=16, db_index=True)
    name = models.CharField(max_length=255, default='')
    region = models.CharField(max_length=100, blank=True, default='')
    district = models.CharField(max_length=100, blank=True, default='')
    city = models.CharField(max_length=50, blank=True, default='')
    country = models.CharField(max_length=100, blank=True, default='')
    images = models.TextField(blank=True, default='')
    video = models.TextField(blank=True, default='')
    coordinates = models.TextField(blank=True, default='')
    currency = models.CharField(max_length=50, blank=True, default='')

    class Meta:
        db_table = 'building'
        ordering = ['id']

    manager = BuildingManager()


class HouseManager(models.Manager):
    def create(self, data):
        if not data['start_development']:
            data['start_development'] = None

        if not data['end_development']:
            data['end_development'] = None

        house = self.model(
            hash_id=helper.create_hash(),
            building=data['building'],
            building_hash_id=data['building_hash_id'],
            living_floors=data['living_floors'],
            number_of_floors=data['number_of_floors'],
            number_of_entrance=data['number_of_entrance'],
            number_of_flat=data['number_of_flat'],
            street_name=data['street_name'],
            number=data['number'],
            finishing=data['finishing'],
            materials=data['materials'],
            stage_development=data['stage_development'],
            start_development=data['start_development'],
            end_development=data['end_development'],
        )

        house.save()

        return house

    def update(self, house, data):
        if not data['start_development']:
            data['start_development'] = None

        if not data['end_development']:
            data['end_development'] = None

        house.number_of_floors = data['number_of_floors']
        house.living_floors = data['living_floors']
        house.number_of_entrance = data['number_of_entrance']
        house.number_of_flat = data['number_of_flat']
        house.street_name = data['street_name']
        house.number = data['number']
        house.finishing = data['finishing']
        house.materials = data['materials']
        house.stage_development = data['stage_development']
        house.start_development = data['start_development']
        house.end_development = data['end_development']

        house.save()

        return house


class House(models.Model):
    hash_id = models.CharField(max_length=16, db_index=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    building_hash_id = models.CharField(max_length=16, db_index=True)
    number_of_floors = models.PositiveSmallIntegerField(blank=True, null=True)
    living_floors = models.TextField(blank=True, default='')
    number_of_entrance = models.PositiveSmallIntegerField(blank=True, null=True)
    number_of_flat = models.PositiveIntegerField(blank=True, null=True)
    street_name = models.CharField(max_length=100)
    number = models.CharField(max_length=255)
    finishing = models.TextField(blank=True, default='')
    materials = models.TextField(blank=True, default='')
    stage_development = models.CharField(max_length=100, blank=True, default='')
    start_development = models.DateField(null=True, blank=True)
    end_development = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'building_houses'
        ordering = ['id']

    manager = HouseManager()


class FlatSchemaManager(models.Manager):
    def create(self, data):
        flat_schema = self.model(
            hash_id=helper.create_hash(),
            house_hash_id=data['house_hash_id'],
            house=data['house'],
            type=data['type'],
            image=data['image'],
            number_of_balcony=data['number_of_balcony'],
            number_of_loggia=data['number_of_loggia'],
            area=data['area'],
            price=data['price'],
        )

        flat_schema.save()

        return flat_schema

    def update(self, flat_schema, data):
        flat_schema.type = data['type']
        flat_schema.image = data['image']
        flat_schema.number_of_balcony = data['number_of_balcony']
        flat_schema.number_of_loggia = data['number_of_loggia']
        flat_schema.area = data['area']
        flat_schema.price = data['price']

        flat_schema.save()

        return flat_schema


class FlatSchema(models.Model):
    hash_id = models.CharField(max_length=16, db_index=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    house_hash_id = models.CharField(max_length=16, db_index=True)
    type = models.CharField(max_length=100)
    image = models.CharField(max_length=255, blank=True, default='')
    number_of_balcony = models.PositiveSmallIntegerField(blank=True, null=True)
    number_of_loggia = models.PositiveSmallIntegerField(blank=True, null=True)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'building_house_flats_schemas'
        ordering = ['id']

    manager = FlatSchemaManager()


class FloorTypeManager(models.Manager):
    def create(self, data):
        floor_type = self.model(
            hash_id=helper.create_hash(),
            house=data['house'],
            house_hash_id=data['house_hash_id'],
            image=data['image']
        )

        floor_type.save()

        return floor_type


class FloorType(models.Model):
    hash_id = models.CharField(max_length=16, db_index=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    house_hash_id = models.CharField(max_length=16, db_index=True, null=True)
    image = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'building_house_floors_types'
        ordering = ['id']

    manager = FloorTypeManager()


class FloorManager(models.Manager):
    def create(self, data):
        floor = self.model(
            hash_id=helper.create_hash(),
            house=data['house'],
            house_hash_id=data['house_hash_id'],
            floor_type=data['floor_type'],
            floor_type_hash_id=data['floor_type_hash_id'],
            number=data['number'],
        )

        floor.save()

        return floor

    def multiple_create(self, data):
        floors = (Floor(
            hash_id=helper.create_hash(),
            house=data['house'],
            house_hash_id=data['house_hash_id'],
            floor_type=data['floor_type'],
            floor_type_hash_id=data['floor_type_hash_id'],
            number='%s' % number
        ) for number in data['clone_floors'])

        self.bulk_create(floors)

    def update(self, floor, data):
        floor.number = data['number']

        floor.save()

        return floor


class Floor(models.Model):
    hash_id = models.CharField(max_length=16, db_index=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    house_hash_id = models.CharField(max_length=16, db_index=True)
    floor_type = models.ForeignKey(FloorType, on_delete=models.CASCADE, null=True)
    floor_type_hash_id = models.CharField(max_length=16, db_index=True, null=True)
    number = models.IntegerField()

    class Meta:
        db_table = 'building_house_floors'
        ordering = ['id']

    manager = FloorManager()


class FlatTypeManager(models.Manager):
    def create(self, data):
        flat_type = self.model(
            hash_id=helper.create_hash(),
            house=data['house'],
            house_hash_id=data['house_hash_id'],
            floor_type=data['floor_type'],
            floor_type_hash_id=data['floor_type_hash_id'],
            coordinates=data['coordinates'],
        )

        flat_type.save()

        return flat_type


class FlatType(models.Model):
    hash_id = models.CharField(max_length=16, db_index=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    house_hash_id = models.CharField(max_length=16, db_index=True)
    floor_type = models.ForeignKey(FloorType, on_delete=models.CASCADE)
    floor_type_hash_id = models.CharField(max_length=16, db_index=True)
    coordinates = models.TextField()

    class Meta:
        db_table = 'building_house_flats_types'
        ordering = ['id']

    manager = FlatTypeManager()


class FlatManager(models.Manager):
    def multiple_create(self, data):
        flats = []

        for floor in data['clone_floors']:
            flat = Flat(
                hash_id=helper.create_hash(),
                house=data['house'],
                house_hash_id=data['house_hash_id'],
                flat_schema=data['flat_schema'],
                flat_schema_hash_id=data['flat_schema_hash_id'],
                flat_type=data['flat_type'],
                flat_type_hash_id=data['flat_type_hash_id'],
                entrance=data['entrance'],
                number=data['number'],
                area=data['area'],
                price=data['price'],
                windows=data['windows'],
                status=data['status'],
                floor=floor
            )

            data['number'] = 0

            flats.append((
                flat
            ))

        self.bulk_create(flats)

        return flats

    def update(self, flat, data):
        flat.entrance = data['entrance']
        flat.number = data['number']
        flat.area = data['area']
        flat.price = data['price']
        flat.windows = data['windows']
        flat.status = data['status']

        flat.save()

        return flat


class Flat(models.Model):
    hash_id = models.CharField(max_length=16, null=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    house_hash_id = models.CharField(max_length=16, db_index=True)
    flat_schema = models.ForeignKey(FlatSchema, on_delete=models.CASCADE)
    flat_schema_hash_id = models.CharField(max_length=16, db_index=True)
    flat_type = models.ForeignKey(FlatType, on_delete=models.CASCADE, null=True)
    flat_type_hash_id = models.CharField(max_length=16, db_index=True, null=True)
    floor = models.PositiveIntegerField()
    entrance = models.PositiveIntegerField()
    number = models.PositiveIntegerField(blank=True, null=True)
    area = models.DecimalField(blank=True, max_digits=10, decimal_places=2)
    price = models.DecimalField(blank=True, max_digits=10, decimal_places=2)
    windows = models.TextField(blank=True)
    status = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'building_house_flats'
        ordering = ['id']

    manager = FlatManager()




