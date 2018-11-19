from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Sum
import sys
from functools import reduce
import datetime
from dateutil import tz

# Create your models here.


#---------------Device---------------
# Мета-класс справочник
class Catalog(models.Model):
    # Метод "Запись данных в справочник".
    # Записывает переданные ему данные из формы в элемент справочника.
    # Все проверки перед записью в элемент справочника должны быть сделаны заранее,
    # метод принимает только "чистые/проверенные" данные для записи.
    # catlg_attr - словарь: ключ - наименование атрибута справочника
    def catlg_write(self, catlg_attr):
        # проход по всем пользовательским атрибутам справочника
        for attr in self.__dict__.keys():
            # если атрибут присутствует среди значений переданных из формы,
            # то присвоить соотвествующему атрибуту справочника переданное значение из формы.
            if attr in catlg_attr:
                setattr(self, attr, catlg_attr[attr])
        self.save()

    class Meta:
        abstract = True


class Nomenclature(Catalog):
    name = models.CharField(max_length=30, unique=True, verbose_name='Наименование')

    class Meta:
        verbose_name_plural = 'Номенклатура'
        verbose_name = 'Номенклатура'

    def __str__(self):
        return self.name


class DeviceType(Catalog):
    name = models.CharField(max_length=30, unique=True, verbose_name='Наименование')

    class Meta:
        verbose_name_plural = 'Типы устройств'
        verbose_name = 'Тип устройства'

    def __str__(self):
        return self.name


class Device(Catalog):
    inv_num = models.CharField(max_length=30, blank=True, verbose_name='Инвентарный номер')
    serial_num = models.CharField(max_length=30, blank=True)
    name = models.ForeignKey(Nomenclature, on_delete=models.PROTECT, null=True)
    device_type = models.ForeignKey(DeviceType, on_delete=models.PROTECT, null=True)
    comment = models.CharField(max_length=30, blank=True)

    class Meta:
        verbose_name_plural = 'Устройства'
        verbose_name = 'Устройство'

    def __str__(self):
        return str(self.name) + ' (sn: ' + str(self.serial_num) + ')'


class Department(Catalog):
    name = models.CharField(max_length=30, unique=True, verbose_name='Наименование')

    class Meta:
        verbose_name_plural = 'Подразделения'
        verbose_name = 'Подразделение'

    def __str__(self):
        return self.name


class Person(Catalog):
    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Сотрудники'
        verbose_name = 'Сотрудник'

    def __str__(self):
        return self.surname + ' ' + self.name


class Stock(Catalog):
    name = models.CharField(max_length=30, unique=True, verbose_name='Наименование')

    class Meta:
        verbose_name_plural = 'Склады'
        verbose_name = 'Склад'

    def __str__(self):
        return self.name


#---------------Document---------------


#class DocumentManager(models.Manager):
#
#    def doc_create(self):

# Мета-класс документ
class Document(models.Model):
    doc_date = models.DateTimeField()
    doc_num = models.CharField(unique_for_date='doc_date', max_length=15)
    active = models.BooleanField(default=False)

    # универсальный метод для записи регистров любого документа. НЕ РАБОЧИЙ!
    def reg_write2(self):
        status = {reg: {'success': True, 'errors': []} for reg in self._REG_LIST}

        # Проход по экземплярам TableUnit
        for rec in self.get_table_unit():

            # Проход по регистрам документа
            for reg in self._REG_LIST:

                if self._REG_CONST_ATTR_MAP[reg]['_MULTI']:
                    attr_multi_count = self._REG_CONST_ATTR_MAP[reg]['_MULTI']
                else:
                    attr_multi_count = 1

                for i in range(0, attr_multi_count):
                    # новая запись в регистр
                    new_rec = getattr(sys.modules[__name__], reg)(base_doc=self)

                    # Проход по атрибутам регистра (новой записи в регистр)
                    # new_rec._meta.fields - список атрибутов модели регистра ввиде объектов
                    # attr_obj - объект атрибута модели регистра
                    # attr - имя конкретного атрибута модели регистра
                    for attr_obj in new_rec._meta.fields:
                        attr = attr_obj.name
                        attr_map_exist = False

                        if attr in self._REG_DOC_ATTR_MAP[reg]:
                            attr_doc_name = self._REG_DOC_ATTR_MAP[reg][attr]
                            if isinstance(attr_doc_name, tuple):
                                attr_value = getattr(self, attr_doc_name[i])
                            else:
                                attr_value = getattr(self, attr_doc_name)
                            attr_map_exist = True

                        elif attr in self._REG_TU_ATTR_MAP[reg]:
                            attr_tu_name = self._REG_TU_ATTR_MAP[reg][attr]
                            if isinstance(attr_tu_name, tuple):
                                attr_value = getattr(rec, attr_tu_name[i])
                            else:
                                attr_value = getattr(rec, attr_tu_name)
                            attr_map_exist = True

                        elif attr in self._REG_CONST_ATTR_MAP[reg]:
                            attr_const_name = self._REG_CONST_ATTR_MAP[reg][attr]
                            if isinstance(attr_const_name, tuple):
                                attr_value = attr_const_name[i]
                            else:
                                attr_value = attr_const_name
                            attr_map_exist = True

                        if attr_map_exist:
                            setattr(new_rec, attr, attr_value)

                    new_rec_status = new_rec.check_rec()
                    if not new_rec_status[0]:
                        status[reg]['success'] = False
                        status[reg]['errors'].extend(new_rec_status[1])
                    else:
                        new_rec.save()

        status_list = list(status.values())
        status_sum = reduce((lambda x, y: x & y['success']), status_list, status_list[0]['success'])
        status_errors = {k: v['errors'] for k, v in status.items() if not v['success']}
        if status_sum:
            self.active = True
            self.save()
            return (True, status_errors)
        else:
            self.reg_delete()
            return (False, status_errors)

    # Метод "Запись данных в документ".
    # Записывает переданные ему данные из формы в документ.
    # Все проверки перед записью документа должны быть сделаны заранее,
    # метод принимает только "чистые/проверенные" данные для записи.
    # doc_attr - словарь: ключ - наименование атрибута документа
    # table_unit - список. Элемент списка - словарь: ключ - наименование атрибута TableUnit.
    # Ключ "id" - существующий объект TableUnit.
    def doc_write(self, doc_attr, table_unit):
        # проход по всем пользовательским атрибутам документа
        for attr in self.__dict__.keys():
            # если атрибут присутствует среди значений переданных из формы,
            # то присвоить соотвествующему атрибуту документа переданное значение из формы.
            if attr in doc_attr:
                setattr(self, attr, doc_attr[attr])
        self.save()

        if self._TABLE_UNIT_EXIST:
            table_unit_model = getattr(sys.modules[__name__], self.__class__.__name__ + 'TableUnit')
            # rec - словарь с ключами ввиде атрибутов TableUnit, значения - то что выбрано в форме.
            # проход по всем словарям представляющих TableUnit, т.е. по всем строкам из табличной формы.
            for rec in table_unit:
                # создать новую запись для TableUnit, потребуется далее в случае если это новая строка, а не модификация старой
                print('-' * 50)
                print(rec)
                new_rec_flag = False
                new_rec = table_unit_model(doc=self)
                if rec:
                    # проход по всем пользовательским атрибутам TableUnit, attr - наименование атрибута.
                    for attr in table_unit_model.__dict__.keys():
                        # если атрибут присутствует среди значений переданных из формы,
                        # то присвоить соотвествующему атрибуту записи/строки TableUnit переданное значение из формы.
                        if attr in rec:
                            # если ключ id из словаря переданного из формы TableUnit равен None, то это новая запись в TableUnit
                            # если ключ id НЕ None, то в значении ключа id объект TableUnit, который нужно модифийировать
                            if rec['id'] is not None:
                                setattr(rec['id'], attr, rec[attr])
                            else:
                                new_rec_flag = True
                                setattr(new_rec, attr, rec[attr])
                    # после прохода по всем атрибутам сохранить новую запись
                    if new_rec_flag:
                        new_rec.save()
        self.save()

    # Метод "получение табличной части документа". Возвращает набор QuerySet все объектов TableUnit для данного документа
    def get_table_unit(self):
        doc_type = self.__class__.__name__
        if self._TABLE_UNIT_EXIST:
            doc_table_unit = getattr(sys.modules[__name__], doc_type + 'TableUnit').objects.filter(doc=self)
        else:
            doc_table_unit = None
        return doc_table_unit

    # Метод "удаление записей по регистрам для даннго документа"
    def reg_delete(self):
        for reg in self._REG_LIST:
            base_doc_type = ContentType.objects.get_for_model(self)
            getattr(sys.modules[__name__], reg).objects.filter(base_doc_type=base_doc_type, base_doc_id=self.id).delete()
        self.active = False
        self.save()

    # метод "запись по регистрам".
    # Получет данные для записи, затем если нет ошибок, то делает записи
    def reg_write(self):
        status = self.get_data()
        status_list = list(status.values())
        status_sum = reduce((lambda x, y: x & y['success']), status_list, status_list[0]['success'])
        status_errors = {k: v['errors'] for k, v in status.items() if not v['success']}
        if status_sum:
            for reg in status:
                getattr(sys.modules[__name__], reg).objects.bulk_create(status[reg]['recs'])
            self.active = True
            self.save()
            return (True, status_errors)
        else:
            for reg in status:
                if not status[reg]['success']:
                    print('Ошибка проведения регистра ' + reg + ': ' + status[reg]['errors'])
            return (False, status_errors)

    class Meta:
        abstract = True


class DocWriteoff(Document):
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT, blank=True, null=True)
    devices = models.ManyToManyField(Device, through='DocWriteoffTableUnit')
    _REG_LIST = ['RegDeviceStock']
    _TABLE_UNIT_EXIST = True
    _REG_DOC_ATTR_MAP = {
        'RegDeviceStock': {
            'reg_date': 'doc_date',
            'department': 'department',
            'stock': 'stock',
        },
    }
    _REG_TU_ATTR_MAP = {
        'RegDeviceStock': {
            'device': 'device',
            'person': 'person',
            'qty': 'qty',
            'base_doc': 'doc',
        },
    }
    _REG_CONST_ATTR_MAP = {
        'RegDeviceStock': {
            '_MULTI': False,
            'operation_type': '-',
        },
    }

    # метод "получить данные для записи в регистр".
    # возвращает словарь вида {'Регистр1': {'recs':<данные для записи>, 'success':<есть ли логические ошибки данных>, 'errors': <ошибки>}}
    # надо переделать механизм записи в регистры!
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

    def __str__(self):
        local_date = self.doc_date.replace(tzinfo=tz.tzutc()).astimezone(tz=None).strftime('%d.%m.%Y %H:%M:%S')
        doc_desc = 'Списание №%s от %s' % (self.doc_num, local_date)
        return doc_desc


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
    _REG_LIST = ['RegDeviceStock']
    _TABLE_UNIT_EXIST = True

    # Карта соотвествия атрибутов Регистра и атрибудов Документа, Табличной части, Кностант
    # Ключ - имя атрибута регистра
    # Значение - имя атрибута Документа/Табличной части или константа
    # Если один документ делает несколько движений,
    # то имя атрибута Документа/Табличной части или константа указываются в кортеже, в том порядке в котором они должны быть записаны.
    _REG_DOC_ATTR_MAP = {
        'RegDeviceStock': {
            'reg_date': 'doc_date',
            'department': ('department_from', 'department_to'),
            'stock': ('stock_from', 'stock_to'),
        },
    }
    _REG_TU_ATTR_MAP = {
        'RegDeviceStock': {
            'device': 'device',
            'person': ('person_from', 'person_to'),
            'qty': 'qty',
            'base_doc': 'doc',
        },
    }
    # Карта для констант.
    # Константа _MULTI обязательна.
    # Она показывает сколько движений делает документ по регистру. Или False если не делает.
    _REG_CONST_ATTR_MAP = {
        'RegDeviceStock': {
            '_MULTI': 2,
            'operation_type': ('-', '+'),
        },
    }

    # метод "получить данные для записи в регистр".
    # возвращает словарь вида {'Регистр1': {'recs':<данные для записи>, 'success':<есть ли логические ошибки данных>, 'errors': <ошибки>}}
    # надо переделать механизм записи в регистры!
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
        local_date = self.doc_date.replace(tzinfo=tz.tzutc()).astimezone(tz=None).strftime('%d.%m.%Y %H:%M:%S')
        doc_desc = 'Перемещение №%s от %s' % (self.doc_num, local_date)
        return doc_desc


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
    _REG_LIST = ['RegDeviceStock']
    _TABLE_UNIT_EXIST = True
    _REG_DOC_ATTR_MAP = {
        'RegDeviceStock': {
            'reg_date': 'doc_date',
            'department': 'department',
            'stock': 'stock',
        },
    }
    _REG_TU_ATTR_MAP = {
        'RegDeviceStock': {
            'device': 'device',
            'person': 'person',
            'qty': 'qty',
            'base_doc': 'doc',
        },
    }
    _REG_CONST_ATTR_MAP = {
        'RegDeviceStock': {
            '_MULTI': False,
            'operation_type': '+',
        },
    }

    # метод "получить данные для записи в регистр".
    # возвращает словарь вида {'Регистр1': {'recs':<данные для записи>, 'success':<есть ли логические ошибки данных>, 'errors': <ошибки>}}
    # надо переделать механизм записи в регистры!
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

    def doc_write2(self, doc_attr, table_unit):
        self.doc_date = doc_attr['doc_date']
        self.doc_num = doc_attr['doc_num']
        self.department = doc_attr['department']
        self.stock = doc_attr['stock']
        self.save()
        tableunit_recs = []
        for rec in table_unit:
            if rec:
                tableunit_recs.append(DocIncomeTableUnit(
                    doc=self,
                    device=rec['device'],
                    person=rec['person'],
                    qty=rec['qty'],
                    comment=rec['comment']))
        DocIncomeTableUnit.objects.filter(doc=self).delete()
        DocIncomeTableUnit.objects.bulk_create(tableunit_recs)

    def __str__(self):
        local_date = self.doc_date.replace(tzinfo=tz.tzutc()).astimezone(tz=None).strftime('%d.%m.%Y %H:%M:%S')
        doc_desc = 'Оприходование №%s от %s' % (self.doc_num, local_date)
        return doc_desc


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

    def check_rec(self):
        errors = []
        devices_minus = list(RegDeviceStock.objects.filter(reg_date__lte=self.reg_date, device=self.device, operation_type='-').values('device').annotate(total=Sum('qty')))
        devices_plus = list(RegDeviceStock.objects.filter(reg_date__lte=self.reg_date, device=self.device, operation_type='+').values('device').annotate(total=Sum('qty')))
        if not devices_minus:
            devices_minus = 0
        else:
            devices_minus = devices_minus[0]['total']
        if not devices_plus:
            devices_plus = 0
        else:
            devices_plus = devices_plus[0]['total']

        print('devices_minus: %s' % devices_minus)
        print('devices_plus: %s' % devices_plus)

        if self.operation_type == '+':
            if (devices_plus - devices_minus) > 0:
                errors.append('Устройство %s было оприходовано ранее и на дату %s еще не списано.' % (self.device, self.reg_date.strftime('%d.%m.%Y %H:%M:%S')))
                return (False, errors)

        return (True, [])

    def __str__(self):
        return self.operation_type + ' ' + str(self.base_doc)
