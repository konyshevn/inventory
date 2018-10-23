from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Sum
import sys
from functools import reduce

# Create your models here.


#---------------Device---------------
class Nomenclature(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class DeviceType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Device(models.Model):
    inv_num = models.CharField(max_length=30, blank=True)
    serial_num = models.CharField(max_length=30, blank=True)
    name = models.ForeignKey(Nomenclature, on_delete=models.PROTECT, null=True)
    device_type = models.ForeignKey(DeviceType, on_delete=models.PROTECT, null=True)
    comment = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return str(self.name) + ' (sn: ' + str(self.serial_num) + ')'


#---------------Document---------------


#class DocumentManager(models.Manager):
#
#    def doc_create(self):


class Document(models.Model):
    doc_date = models.DateTimeField()
    doc_num = models.CharField(unique_for_date='doc_date', max_length=15)
    active = models.BooleanField(default=False)

    def doc_write(self):
        self.save()

    def get_table_unit(self):
        doc_type = self.__class__.__name__
        if self.table_unit:
            doc_table_unit = getattr(sys.modules[__name__], doc_type + 'TableUnit').objects.filter(doc=self)
        else:
            doc_table_unit = None
        return doc_table_unit

    def reg_delete(self):
        for reg in self.REG_LIST:
            base_doc_type = ContentType.objects.get_for_model(self)
            getattr(sys.modules[__name__], reg).objects.filter(base_doc_type=base_doc_type, base_doc_id=self.id).delete()
        self.active = False
        self.save()

    def reg_write(self):
        status = self.get_data()
        print(status)
        status_list = list(status.values())
        status_sum = reduce((lambda x, y: x & y['success']), status_list, status_list[0]['success'])
        if status_sum:
            for reg in status:
                getattr(sys.modules[__name__], reg).objects.bulk_create(status[reg]['recs'])
            self.active = True
            self.save()
        else:
            return status
            for reg in status:
                if not status[reg]['success']:
                    print('Ошибка проведения регистра ' + reg + ': ' + status[reg]['errors'])

    class Meta:
        abstract = True


class Department(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Person(models.Model):
    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)

    def __str__(self):
        return self.surname + ' ' + self.name


class Stock(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class DocWriteoff(Document):
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT, blank=True, null=True)
    devices = models.ManyToManyField(Device, through='DocWriteoffTableUnit')
    REG_LIST = ['RegDeviceStock']
    table_unit = True

    def get_data(self):
        status = {}
        status.update([('RegDeviceStock', {'recs': None, 'success': False, 'errors': []})])
        RegDeviceStock_recs = []
        for rec_table_unit in self.get_table_unit():
            RegDeviceStock_recs.append(RegDeviceStock(
                operation_type='-',
                base_doc=self,
                reg_date=self.doc_date,
                department=self.department,
                stock=self.stock,
                device=rec_table_unit.device,
                person=rec_table_unit.person,
                qty=rec_table_unit.qty))
        status['RegDeviceStock']['success'] = True
        status['RegDeviceStock']['recs'] = RegDeviceStock_recs
        return status

    def doc_write(self, doc_attr, table_unit):
        self.doc_date = doc_attr['doc_date']
        self.doc_num = doc_attr['doc_num']
        self.department = doc_attr['department']
        self.stock = doc_attr['stock']
        tableunit_recs = []
        for rec in table_unit:
            if rec:
                tableunit_recs.append(DocWriteoffTableUnit(
                    doc=self,
                    device=rec['device'],
                    person=rec['person'],
                    qty=rec['qty'],
                    comment=rec['comment']))
        self.save()
        DocWriteoffTableUnit.objects.filter(doc=self).delete()
        DocWriteoffTableUnit.objects.bulk_create(tableunit_recs)

    def __str__(self):
        return 'Списание ' + self.doc_num + ' ' + str(self.doc_date)


class DocWriteoffTableUnit(models.Model):
    doc = models.ForeignKey(DocWriteoff, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.PROTECT)
    person = models.ForeignKey(Person, on_delete=models.PROTECT, blank=True, null=True)
    qty = models.PositiveIntegerField(default=1)
    comment = models.CharField(max_length=70, blank=True)


class DocMove(Document):
    department_from = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='department_from')
    department_to = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='department_to')
    stock_from = models.ForeignKey(Stock, on_delete=models.PROTECT, blank=True, null=True, related_name='stock_from')
    stock_to = models.ForeignKey(Stock, on_delete=models.PROTECT, blank=True, null=True, related_name='stock_to')
    devices = models.ManyToManyField(Device, through='DocMoveTableUnit')
    REG_LIST = ['RegDeviceStock']
    table_unit = True

    def get_data(self):
        status = {}
        status.update([('RegDeviceStock', {'recs': None, 'success': False, 'errors': []})])
        RegDeviceStock_recs = []
        for rec_table_unit in self.get_table_unit():
            RegDeviceStock_recs.append(RegDeviceStock(
                operation_type='-',
                base_doc=self,
                reg_date=self.doc_date,
                department=self.department_from,
                stock=self.stock_from,
                device=rec_table_unit.device,
                person=rec_table_unit.person_from,
                qty=rec_table_unit.qty))
            RegDeviceStock_recs.append(RegDeviceStock(
                operation_type='+',
                base_doc=self,
                reg_date=self.doc_date,
                department=self.department_to,
                stock=self.stock_to,
                device=rec_table_unit.device,
                person=rec_table_unit.person_to,
                qty=rec_table_unit.qty))
        status['RegDeviceStock']['success'] = True
        status['RegDeviceStock']['recs'] = RegDeviceStock_recs
        return status

    def __str__(self):
        return 'Перемещение ' + self.doc_num + ' ' + str(self.doc_date)


class DocMoveTableUnit(models.Model):
    doc = models.ForeignKey(DocMove, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.PROTECT)
    person_from = models.ForeignKey(Person, on_delete=models.PROTECT, blank=True, null=True, related_name='person_from')
    person_to = models.ForeignKey(Person, on_delete=models.PROTECT, blank=True, null=True, related_name='person_to')
    qty = models.PositiveIntegerField(default=1)
    comment = models.CharField(max_length=70, blank=True)


class DocIncome(Document):
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT, blank=True, null=True)
    devices = models.ManyToManyField(Device, through='DocIncomeTableUnit')
    REG_LIST = ['RegDeviceStock']
    table_unit = True

    def get_data(self):
        status = {}
        status.update([('RegDeviceStock', {'recs': None, 'success': False, 'errors': []})])
        RegDeviceStock_recs = []
        for rec_table_unit in self.get_table_unit():
            RegDeviceStock_recs.append(RegDeviceStock(
                operation_type='+',
                base_doc=self,
                reg_date=self.doc_date,
                department=self.department,
                stock=self.stock,
                device=rec_table_unit.device,
                person=rec_table_unit.person,
                qty=rec_table_unit.qty))
        status['RegDeviceStock']['success'] = True
        status['RegDeviceStock']['recs'] = RegDeviceStock_recs
        return status

    def doc_write(self, doc_attr, table_unit):
        self.doc_date = doc_attr['doc_date']
        self.doc_num = doc_attr['doc_num']
        self.department = doc_attr['department']
        self.stock = doc_attr['stock']
        tableunit_recs = []
        for rec in table_unit:
            if rec:
                tableunit_recs.append(DocIncomeTableUnit(
                    doc=self,
                    device=rec['device'],
                    person=rec['person'],
                    qty=rec['qty'],
                    comment=rec['comment']))
        self.save()
        DocIncomeTableUnit.objects.filter(doc=self).delete()
        DocIncomeTableUnit.objects.bulk_create(tableunit_recs)

    def __str__(self):
        return 'Оприходование ' + self.doc_num + ' ' + str(self.doc_date)


class DocIncomeTableUnit(models.Model):
    doc = models.ForeignKey(DocIncome, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.PROTECT)
    person = models.ForeignKey(Person, on_delete=models.PROTECT, blank=True, null=True)
    qty = models.PositiveIntegerField(default=1)
    comment = models.CharField(max_length=70, blank=True)


#---------------Registry---------------

class Registry(models.Model):
    operation_types = (('+', '+'), ('-', '-'))
    operation_type = models.CharField(max_length=1, choices=operation_types)
    base_doc_type = models.ForeignKey(ContentType, on_delete=models.PROTECT,)
    base_doc_id = models.PositiveIntegerField()
    base_doc = GenericForeignKey('base_doc_type', 'base_doc_id')
    reg_date = models.DateTimeField()

    class Meta:
        abstract = True


class RegDeviceStock(Registry):
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT, blank=True, null=True)
    device = models.ForeignKey(Device, on_delete=models.PROTECT, default=1)
    person = models.ForeignKey(Person, on_delete=models.PROTECT, blank=True, null=True)
    qty = models.PositiveIntegerField()

    def __str__(self):
        return self.operation_type + ' ' + str(self.base_doc)
