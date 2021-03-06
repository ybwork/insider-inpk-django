from django.db import models
from auth.models import Company
from insider.services import Validation, Helper


validation = Validation()
helper = Helper()


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


class House(models.Model):
    hash_id = models.CharField(max_length=16, db_index=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    building_hash_id = models.CharField(max_length=16, db_index=True)
    number_of_floors = models.PositiveSmallIntegerField(blank=True, null=True)
    living_floors = models.TextField(default='')
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


class FlatSchema(models.Model):
    hash_id = models.CharField(max_length=16, db_index=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    house_hash_id = models.CharField(max_length=16, db_index=True)
    type = models.CharField(max_length=100)
    image = models.CharField(max_length=255, blank=True, default='')
    number_of_balcony = models.PositiveSmallIntegerField(blank=True, null=True)
    number_of_loggia = models.PositiveSmallIntegerField(blank=True, null=True)
    number_of_rooms = models.PositiveIntegerField(null=True)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'building_house_flats_schemas'
        ordering = ['id']


class FloorType(models.Model):
    hash_id = models.CharField(max_length=16, db_index=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    house_hash_id = models.CharField(max_length=16, db_index=True, null=True)
    image = models.CharField(max_length=255, null=True)
    number = models.IntegerField(null=True)
    clone_floors = models.CharField(max_length=255, null=True)
    number_of_flats = models.PositiveIntegerField(null=True)

    class Meta:
        db_table = 'building_house_floors_types'
        ordering = ['id']


class Floor(models.Model):
    hash_id = models.CharField(max_length=16, db_index=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    house_hash_id = models.CharField(max_length=16, db_index=True)
    floor_type = models.ForeignKey(FloorType, on_delete=models.CASCADE, null=True)
    floor_type_hash_id = models.CharField(max_length=16, db_index=True, null=True)
    number = models.PositiveIntegerField(null=True)

    class Meta:
        db_table = 'building_house_floors'
        ordering = ['id']


class FlatType(models.Model):
    hash_id = models.CharField(max_length=16, db_index=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    house_hash_id = models.CharField(max_length=16, db_index=True)
    floor_type = models.ForeignKey(FloorType, on_delete=models.CASCADE)
    floor_type_hash_id = models.CharField(max_length=16, db_index=True)
    flat_schema = models.ForeignKey(FlatSchema, on_delete=models.CASCADE)
    flat_schema_hash_id = models.CharField(max_length=16, db_index=True)
    number = models.IntegerField(null=True)
    entrance = models.IntegerField(null=True)
    coordinates = models.TextField()
    windows = models.TextField(blank=True)

    class Meta:
        db_table = 'building_house_flats_types'
        ordering = ['id']


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
    number = models.PositiveIntegerField()
    windows = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    area = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    status = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'building_house_flats'
        ordering = ['id']




