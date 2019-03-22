from rest_framework import serializers
from . import models
import gm2m.serializers.json
from django.contrib.contenttypes.models import ContentType


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Device
        exclude = ()


class leaderField(serializers.RelatedField):
    def to_representation(self, value):
        return {'doc_id': value.id, 'contenttype_id': ContentType.objects.get_for_model(value).id}


class DocIncomeTableUnitSerializer(serializers.ModelSerializer):
    id = serializers.ModelField(model_field=models.DocIncomeTableUnit()._meta.get_field('id'), allow_null=True)

    class Meta:
        model = models.DocIncomeTableUnit
        exclude = ('doc',)
        #fields = ('id', 'device', 'person', 'qty', 'comment')

    #def to_representation(self, value):
    #    return {'id': value.id, 'device': value.device.id}


class DocIncomeSerializer(serializers.ModelSerializer):
    table_unit = DocIncomeTableUnitSerializer(many=True)

    class Meta:
        model = models.DocIncome
        exclude = ('devices', )

    def create(self, validated_data):
        print(validated_data)
        print(dict(validated_data['table_unit'][0]))
        dc = self.Meta.model.objects.create_doc(doc_attr=validated_data, table_unit=validated_data['table_unit'])
        #doc = self.Meta.model()
        #dw = doc.doc_write(doc_attr=validated_data, table_unit=validated_data['table_unit'])
        #rd = doc.reg_delete()
        #rw = doc.reg_write()
        #if validated_data['name'] == 'err':
        #    raise serializers.ValidationError('This field must be an integer value.')
        #return self.Meta.model.objects.create(**validated_data)
        if not dc['success']:
            raise serializers.ValidationError(dc['data'])
        return dc['data']


class RegDeviceStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RegDeviceStock
        exclude = ()
