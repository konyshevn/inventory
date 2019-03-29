from rest_framework import serializers
from . import models
from django.contrib.contenttypes.models import ContentType


class RegDeviceStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RegDeviceStock
        exclude = ()


class leaderField(serializers.RelatedField):
    def to_representation(self, value):
        return {'doc_id': value.id, 'contenttype_id': ContentType.objects.get_for_model(value).id}


class CatalogSerializer(serializers.Serializer):
    pass


class DocumentSerializer(serializers.Serializer):
    def create(self, validated_data):
        print(validated_data)
        print(dict(validated_data['table_unit'][0]))
        cd = self.Meta.model.objects.create_doc(doc_attr=validated_data, table_unit=validated_data['table_unit'])
        if not cd['success']:
            raise serializers.ValidationError(cd['data'])
        return cd['data'][0]

    def update(self, instance, validated_data):
        cd = instance.update_doc(doc_attr=validated_data, table_unit=validated_data['table_unit'])
        if not cd['success']:
            raise serializers.ValidationError(cd['data'])
        return cd['data'][0]


class DocIncomeTableUnitSerializer(serializers.ModelSerializer):
    id = serializers.ModelField(model_field=models.DocIncomeTableUnit()._meta.get_field('id'), allow_null=True)

    class Meta:
        model = models.DocIncomeTableUnit
        exclude = ('doc',)


class DocIncomeSerializer(DocumentSerializer, serializers.ModelSerializer):
    table_unit = DocIncomeTableUnitSerializer(many=True)

    class Meta:
        model = models.DocIncome
        exclude = ('devices', )


class DocWriteoffTableUnitSerializer(serializers.ModelSerializer):
    id = serializers.ModelField(model_field=models.DocWriteoffTableUnit()._meta.get_field('id'), allow_null=True)

    class Meta:
        model = models.DocWriteoffTableUnit
        exclude = ('doc',)


class DocWriteoffSerializer(DocumentSerializer, serializers.ModelSerializer):
    table_unit = DocWriteoffTableUnitSerializer(many=True)

    class Meta:
        model = models.DocWriteoff
        exclude = ('devices', )


class DocMoveTableUnitSerializer(serializers.ModelSerializer):
    id = serializers.ModelField(model_field=models.DocMoveTableUnit()._meta.get_field('id'), allow_null=True)

    class Meta:
        model = models.DocMoveTableUnit
        exclude = ('doc',)


class DocMoveSerializer(DocumentSerializer, serializers.ModelSerializer):
    table_unit = DocMoveTableUnitSerializer(many=True)

    class Meta:
        model = models.DocMove
        exclude = ('devices', )


class DocInventoryTableUnitSerializer(serializers.ModelSerializer):
    id = serializers.ModelField(model_field=models.DocInventoryTableUnit()._meta.get_field('id'), allow_null=True)

    class Meta:
        model = models.DocInventoryTableUnit
        exclude = ('doc',)


class DocInventorySerializer(DocumentSerializer, serializers.ModelSerializer):
    table_unit = DocInventoryTableUnitSerializer(many=True)

    class Meta:
        model = models.DocInventory
        exclude = ('devices', )


class DeviceSerializer(CatalogSerializer, serializers.ModelSerializer):
    class Meta:
        model = models.Device
        exclude = ()


class DepartmentSerializer(CatalogSerializer, serializers.ModelSerializer):
    class Meta:
        model = models.Department
        exclude = ()


class StockSerializer(CatalogSerializer, serializers.ModelSerializer):
    class Meta:
        model = models.Stock
        exclude = ()
