from _db import models
from rest_framework import serializers


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.House
        fields = ('id', 'user', 'name', 'address', 'number', 'image1', 'image2', 'image3', 'image4', 'image5', )


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Section
        fields = ('id', 'house', 'name', )


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Floor
        fields = ('id', 'section', 'name', )


class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Apartment
        fields = ('id', 'floor', 'name', 'apartment_area', 'user', 'tariff', 'account')


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = ('id', 'name',  'active', 'measure')


class TariffServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TariffService
        fields = ('id', 'service',  'tariff', 'price')


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = ('id', 'wallet',  'money', 'status')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'email',  'first_name', 'last_name', 'middle_name', 'is_active', 'date_joined', 'role', 'number', 'user_type')


class MeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Measure
        fields = ('id', 'name')
