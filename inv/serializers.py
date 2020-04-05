from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from . import models
from django.contrib.contenttypes.models import ContentType


class RegDeviceStockSerializer(serializers.ModelSerializer):
    base_doc = serializers.SerializerMethodField()

    def get_base_doc(self, obj):
        doc = {
            "docType": obj.base_doc_type.model,
            "docId": obj.base_doc_id
        }
        return doc

    class Meta:
        model = models.RegDeviceStock
        exclude = ('base_doc_id', 'base_doc_type')
        read_only_fields = ['__all__']


class leaderField(serializers.RelatedField):
    def to_representation(self, value):
        return {'doc_id': value.id, 'contenttype_id': ContentType.objects.get_for_model(value).id}


class CatalogSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super(CatalogSerializer, self).__init__(*args, **kwargs)

        if 'labels' in self.fields:
            raise RuntimeError(
                'You cant have labels field defined '
                'while using MyModelSerializer'
            )

        self.fields['labels'] = SerializerMethodField()

    def get_labels(self, *args):
        labels = {}

        for field in self.Meta.model._meta.get_fields():
            if field.name in self.fields:
                labels[field.name] = field.verbose_name

        labels['_model'] = {
            'singular': self.Meta.model._meta.verbose_name.title(),
            'plural': self.Meta.model._meta.verbose_name_plural.title(),
        }
        return labels


class DocumentSerializer(serializers.Serializer):
    doc_num = serializers.IntegerField(required=False, allow_null=True)
    def create(self, validated_data):
        print(validated_data)
        #print(dict(validated_data['table_unit'][0]))
        cd = self.Meta.model.objects.create_doc(doc_attr=validated_data, table_unit=validated_data['table_unit'])
        if not cd['success']:
            raise serializers.ValidationError(cd['data'])
        return cd['data'][0]

    def update(self, instance, validated_data):
        cd = instance.update_doc(doc_attr=validated_data, table_unit=validated_data['table_unit'])
        if not cd['success']:
            raise serializers.ValidationError(cd['data'])
        return cd['data'][0]
    
    #def validate(self, data):
        """
        Check that start is before finish.
        """
        #if data['start'] > data['finish']:
        #    raise serializers.ValidationError("finish must occur after start")
        #return data


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


class PersonSerializer(CatalogSerializer, serializers.ModelSerializer):
    class Meta:
        model = models.Person
        exclude = ()


class NomenclatureSerializer(CatalogSerializer, serializers.ModelSerializer):
    class Meta:
        model = models.Nomenclature
        exclude = ()


class DeviceTypeSerializer(CatalogSerializer, serializers.ModelSerializer):
    class Meta:
        model = models.DeviceType
        exclude = ()
