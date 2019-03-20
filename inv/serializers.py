from rest_framework import serializers
from . import models
import gm2m.serializers.json
from django.contrib.contenttypes.models import ContentType

class DocIncomeTableUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DocIncomeTableUnit
        exclude = ()


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Device
        exclude = ()


class leaderField(serializers.RelatedField):
    def to_representation(self, value):
        return {'doc_id': value.id, 'contenttype_id': ContentType.objects.get_for_model(value).id}


class followerField(serializers.RelatedField):
    def to_representation(self, value):
        return {'doc_id': value.id, 'contenttype_id': ContentType.objects.get_for_model(value).id}


class DocIncomeSerializer(serializers.ModelSerializer):
    #doc_to_device = DocIncomeTableUnitSerializer(many=True)
    #leader = leaderField(many=True, read_only=True)
    #follower = followerField(many=True, read_only=True)

    class Meta:
        model = models.DocIncome
        exclude = ()

    def create(self, validated_data):
        #if validated_data['name'] == 'err':
        #    raise serializers.ValidationError('This field must be an integer value.')
        return self.Meta.model.objects.create(**validated_data)


class RegDeviceStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RegDeviceStock
        exclude = ()
