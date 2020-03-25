from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db.models import Sum
from django.db.models.deletion import ProtectedError
import sys, copy
from functools import reduce
import datetime, time
from dateutil import tz


# Create your models here.
def check_operation(operation, status):
    if not operation['success']:
        status['success'] = False
        status['data'].extend(operation['data'])


# ---------------Device---------------
# Мета-класс справочник
class Catalog(models.Model):
    # Метод "Запись данных в справочник".
    # Записывает переданные ему данные из формы в элемент справочника.
    # Все проверки перед записью в элемент справочника должны быть сделаны заранее,
    # метод принимает только "чистые/проверенные" данные для записи.
    # catlg_attr - словарь: ключ - наименование атрибута справочника
    def catlg_write(self, catlg_attr):
        status = {'success': True, 'data': []}
        # проход по всем пользовательским атрибутам справочника
        for attr in self.__dict__.keys():
            # если атрибут присутствует среди значений переданных из формы,
            # то присвоить соотвествующему атрибуту справочника переданное значение из формы.
            if attr in catlg_attr:
                setattr(self, attr, catlg_attr[attr])
        try:
            self.save()
        except Exception as err:
            status['success'] = False
            status['data'] = [str(err)]
        return status

    def catlg_delete(self):
        status = {'success': True, 'data': []}
        try:
            self.delete()
        except ProtectedError as err:
            status['success'] = False
            status['data'] = ['Ошибка. Данный элемент используется в: %s' % [str(item) for item in err.protected_objects]]
            # print('Ошибка. Данный элемент используется в: %s' % [str(item) for item in err.protected_objects])
        return status

    class Meta:
        abstract = True


class Nomenclature(Catalog):
    label = models.CharField(max_length=30, unique=True, verbose_name='Наименование')

    class Meta:
        verbose_name_plural = 'Номенклатура'
        verbose_name = 'Номенклатура'

    def __str__(self):
        return self.label


class DeviceType(Catalog):
    label = models.CharField(max_length=30, unique=True, verbose_name='Наименование')

    class Meta:
        verbose_name_plural = 'Типы устройств'
        verbose_name = 'Тип устройства'

    def __str__(self):
        return self.label


class Device(Catalog):
    inv_num = models.CharField(max_length=30, blank=True, verbose_name='Инвентарный номер')
    serial_num = models.CharField(max_length=30, blank=True)
    nomenclature = models.ForeignKey(Nomenclature, on_delete=models.PROTECT, null=True)
    deviceType = models.ForeignKey(DeviceType, on_delete=models.PROTECT, null=True)
    comment = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = 'Устройства'
        verbose_name = 'Устройство'

    def __str__(self):
        return str(self.deviceType) + ' ' + str(self.nomenclature) + ' (sn: ' + str(self.serial_num) + ')'


class Department(Catalog):
    label = models.CharField(max_length=50, unique=True, verbose_name='Наименование')

    class Meta:
        verbose_name_plural = 'Подразделения'
        verbose_name = 'Подразделение'

    def __str__(self):
        return self.label


class Person(Catalog):
    surname = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Сотрудники'
        verbose_name = 'Сотрудник'

    def __str__(self):
        return self.surname + ' ' + self.name


class Stock(Catalog):
    label = models.CharField(max_length=30, unique=True, verbose_name='Наименование')

    class Meta:
        verbose_name_plural = 'Склады'
        verbose_name = 'Склад'

    def __str__(self):
        return self.label


#---------------Document---------------
class DocumentManager(models.Manager):
    def get_doc_num(self):
        doc_all = self.all().order_by('-doc_num')
        if doc_all:
            last_num = int(doc_all[0].doc_num)
        else:
            last_num = 0
        doc_num = last_num + 1
        return doc_num

    def create_doc(self, doc_attr, table_unit):
        status = {'success': True, 'data': []}

        if doc_attr['doc_num'] is None:
            doc_attr['doc_num'] = self.get_doc_num()

        if doc_attr['doc_date'] is None:
            doc_attr['doc_date'] = datetime.datetime.now()

        doc = self.model()
        dw = doc.doc_write(doc_attr=doc_attr, table_unit=table_unit)
        print(doc)
        check_operation(operation=dw, status=status)

        rd = doc.reg_delete()
        check_operation(operation=rd, status=status)

        if doc_attr['active']:
            rw = doc.reg_write()
            check_operation(operation=rw, status=status)

        if status['success']:
            status['data'] = [doc]
        return status


class RegDeviceStockManager(models.Manager):
    def saldo(self, device=None, date_from=None, date_to=None, department=None, stock=None, person=None):
        start = time.time()
        filter_vals = {}
        if device is not None:
            filter_vals.update([('device', device)])

        if date_from is not None:
            filter_vals.update([('reg_date__gte', date_from)])

        if date_to is not None:
            filter_vals.update([('reg_date__lte', date_to)])

        if department is not None:
            filter_vals.update([('department', department)])

        if stock is not None:
            filter_vals.update([('stock', stock)])

        if person is not None:
            filter_vals.update([('person', person)])

        filter_minus = filter_vals.copy()
        filter_plus = filter_vals.copy()
        filter_minus.update([('operation_type', '-')])
        filter_plus.update([('operation_type', '+')])

        qty_minus = list(self.filter(**filter_minus).values('device').annotate(total=Sum('qty')))
        qty_plus = list(self.filter(**filter_plus).values('device').annotate(total=Sum('qty')))

        if not qty_minus:
            qty_minus = 0
        else:
            qty_minus = qty_minus[0]['total']

        if not qty_plus:
            qty_plus = 0
        else:
            qty_plus = qty_plus[0]['total']
        #print('saldo_TOTAL: %s' % str(time.time() - start))
        return qty_plus - qty_minus

    def current_location(self, device, date):
        start = time.time()
        location = {'department': '', 'stock': '', 'person': '', 'qty': None}
        qty = self.saldo(device=device, date_to=date)
        if qty == 1:
            reg_rec = self.filter(device=device, operation_type='+', reg_date__lte=date).order_by('-reg_date').first()
            location['department'] = reg_rec.department
            location['stock'] = reg_rec.stock
            location['person'] = reg_rec.person
            location['qty'] = qty
        #print('current_location_TOTAL: %s' % str(time.time() - start))
        return location


# Мета-класс документ
class Document(models.Model):
    doc_date = models.DateTimeField()
    doc_num = models.IntegerField(unique_for_date='doc_date')
    active = models.BooleanField(default=False)
    comment = models.CharField(max_length=70, blank=True)
    leader_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, null=True)
    leader_id = models.PositiveIntegerField(null=True)
    leader = GenericForeignKey('leader_type', 'leader_id')
    _FOLLOWER_TYPES = []

    # универсальный метод для записи регистров любого документа.
    def reg_write(self):
        status = {reg: {'success': True, 'errors': []} for reg in self._REG_LIST}

        if len(self._REG_LIST) == 0:
            self.active = True
            self.save()
            return {'success': True, 'data': []}

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
                        # прервать цикл прохода по _MULTI движениям 
                        break
                    else:
                        new_rec.save()

        status_list = list(status.values())
        status_sum = reduce((lambda x, y: x & y['success']), status_list, status_list[0]['success'])
        #status_errors = {k: v['errors'] for k, v in status.items() if not v['success']}
        status_errors0 = [['Регистр %s: %s' % (k, err) for err in v['errors']] for k, v in status.items() if not v['success']]
        status_errors = [item for sublist in status_errors0 for item in sublist]
        print(status_errors)
        if status_sum:
            self.active = True
            self.save()
            return {'success': True, 'data': status_errors}
        else:
            self.reg_delete()
            return {'success': False, 'data': status_errors}

    # Метод "Запись данных в документ".
    # Записывает переданные ему данные из формы в документ.
    # Все проверки перед записью документа должны быть сделаны заранее,
    # метод принимает только "чистые/проверенные" данные для записи.
    # doc_attr - словарь: ключ - наименование атрибута документа
    # table_unit - список. Элемент списка - словарь: ключ - наименование атрибута TableUnit.
    # Ключ "id" - существующий объект TableUnit.
    def doc_write(self, doc_attr, table_unit):
        # проход по всем пользовательским атрибутам документа
        doc_model = self._meta.model
        for attr_obj in doc_model._meta.fields:
            attr = attr_obj.name
            # если атрибут присутствует среди значений переданных из формы,
            # то присвоить соотвествующему атрибуту документа переданное значение из формы.
            if attr in doc_attr:
                setattr(self, attr, doc_attr[attr])

            # если это новый документ и у него не заполнен номер, то получить номер автоматом
            if ((doc_attr['doc_num'] is None) and (doc_attr['id'] is None)):
                setattr(self, 'doc_num', doc_model.objects.get_doc_num())

        try:
            self.save()
        except Exception as err:
            return {'success': False, 'data': [err]}

        if self._TABLE_UNIT_EXIST:
            # удалить записи табличной части, которых нет в данных из формы (аргумент функции - table_unit)
            for rec in self.get_table_unit():
                print('doc_tu', rec.id)
                is_exist = False
                for row in table_unit:
                    print('arg_tu', row)
                    if row['id'] == rec.id:
                        is_exist = True
                        continue
                if not is_exist:
                    rec.delete()

            table_unit_model = getattr(sys.modules[__name__], self.__class__.__name__ + 'TableUnit')

            # rec - словарь с ключами ввиде атрибутов TableUnit, значения - то что выбрано в форме.
            # проход по всем словарям представляющих TableUnit, т.е. по всем строкам из табличной формы.
            #print(table_unit)
            for rec in table_unit:
                if rec:
                    # удалить помеченные в форме записи TableUnit
                    if (('DELETE' in rec) and (rec['DELETE'])):
                        if (('id' in rec) and (rec['id'] is not None)):
                            table_unit_model.objects.get(id=rec['id']).delete()
                        continue

                    # если ключ id из словаря переданного из формы TableUnit равен None, то это новая запись в TableUnit
                    # если ключ id НЕ None, то в значении ключа id объект TableUnit, который нужно модифийировать
                    if rec['id'] is not None:
                        if isinstance(rec['id'], int):
                             table_unit_item = table_unit_model.objects.get(id=rec['id'])
                        # если в качестве id передана строка, значит это временный id из JS для новой записи
                        elif isinstance(rec['id'], str):
                            table_unit_item = table_unit_model(doc=self)
                        else:
                            table_unit_item = rec['id']
                    else:
                        table_unit_item = table_unit_model(doc=self)

                    # проход по всем пользовательским атрибутам TableUnit, attr - наименование атрибута.
                    for attr_obj in table_unit_model._meta.fields:
                        attr = attr_obj.name

                        # если атрибут присутствует среди значений переданных из формы,
                        # то присвоить соотвествующему атрибуту записи/строки TableUnit переданное значение из формы.
                        if (attr in rec) & (attr != 'id'):

                            setattr(table_unit_item, attr, rec[attr])

                    # после прохода по всем атрибутам сохранить запись
                    try:
                        table_unit_item.save()
                    except Exception as err:
                        return {'success': False, 'data': [err]}


        try:
            self.save()
        except Exception as err:
            return {'success': False, 'data': [err]}

        return {'success': True, 'data': []}

    # Метод "получение табличной части документа". Возвращает набор QuerySet всех объектов TableUnit для данного документа
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
        try:
            self.save()
        except Exception as err:
            return {'success': False, 'data': [err]}
        return {'success': True, 'data': []}

    def doc_delete(self):
        status = {'success': True, 'data': []}
        if len(self.get_follower) != 0:
            print('Followers exist - %s - %s' % (len(self.get_follower), str(self.get_follower)))
            status['success'] = False
            status['data'] = 'Не удалось удалить. На основании документа созданы документы: %s' % str(', '.join([str(item) for item in self.get_follower]))
            return status
        rd = self.reg_delete()
        check_operation(operation=rd, status=status)
        try:
            self.delete()
        except Exception as err:
            status['success'] = False
            status['data'].extend(str(err))
        return status

    def update_doc(self, doc_attr, table_unit):
        status = {'success': True, 'data': []}

        if doc_attr['doc_num'] is None:
            doc_attr['doc_num'] = self.doc_num

        if doc_attr['doc_date'] is None:
            doc_attr['doc_date'] = self.doc_date

        doc_before_update_attr = {}
        doc_model = self._meta.model
        for attr_obj in doc_model._meta.fields:
            attr = attr_obj.name
            doc_before_update_attr[attr] = getattr(self, attr)


        doc_before_update_table_unit = []
        table_unit_model = getattr(sys.modules[__name__], self.__class__.__name__ + 'TableUnit')
        for rec in self.get_table_unit():
            row = {}
            for attr_obj in table_unit_model._meta.fields:
                attr = attr_obj.name
                row[attr] = getattr(rec, attr)
            doc_before_update_table_unit.append(row)

        print('doc_before_update_attr:', doc_before_update_attr)
        print('doc_before_update_table_unit:', doc_before_update_table_unit)

        doc = self
        dw = doc.doc_write(doc_attr=doc_attr, table_unit=table_unit)
        print(doc)
        check_operation(operation=dw, status=status)

        rd = doc.reg_delete()
        check_operation(operation=rd, status=status)

        if doc_attr['active']:
            rw = doc.reg_write()
            check_operation(operation=rw, status=status)

        if status['success']:
            status['data'] = [doc]
        else:
            print('Status False. Lets restore')
            doc.doc_write(doc_attr=doc_before_update_attr, table_unit=doc_before_update_table_unit)
            doc.reg_delete()
            doc.reg_write()
        return status

    def set_leader(self, leader_doc):
        self.leader = leader_doc
        self.save()

    @property
    def get_follower(self):
        hierarchy = []
        for follower_type in self._FOLLOWER_TYPES:
            leader_typec = ContentType.objects.get_for_model(self._meta.model)
            hierarchy.extend(list(follower_type.objects.filter(leader_id=self.id, leader_type=leader_typec)))
        print(hierarchy)
        return hierarchy

    @property
    def get_leader(self):
        hierarchy = self.leader
        return hierarchy

    objects = DocumentManager()

    class Meta:
        abstract = True

    def __str__(self):
        local_date = self.doc_date.replace(tzinfo=tz.tzutc()).astimezone(tz=None).strftime('%d.%m.%Y %H:%M:%S')
        doc_desc = '%s №%s от %s' % (self._meta.verbose_name.title(), self.doc_num, local_date)
        return doc_desc


class DocumentTableUnit(models.Model):
    rowOrder = models.PositiveIntegerField(blank=True, null=True)
    DELETE = models.BooleanField(blank=True, null=True)

    class Meta:
        ordering = ['rowOrder']
        abstract = True

    def __str__(self):
        return str(self.doc)


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

    class Meta:
        verbose_name_plural = 'Списания'
        verbose_name = 'Списание'


class DocWriteoffTableUnit(DocumentTableUnit):
    doc = models.ForeignKey(DocWriteoff, on_delete=models.CASCADE, related_name='table_unit')
    device = models.ForeignKey(Device, on_delete=models.PROTECT, blank=True, null=True)
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

    # Карта соотвествия атрибутов Регистра и атрибудов Документа, Табличной части, Констант
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

    class Meta:
        verbose_name_plural = 'Перемещения'
        verbose_name = 'Перемещение'


class DocMoveTableUnit(DocumentTableUnit):
    doc = models.ForeignKey(DocMove, on_delete=models.CASCADE, related_name='table_unit')
    device = models.ForeignKey(Device, on_delete=models.PROTECT, blank=True, null=True)
    person_from = models.ForeignKey(Person, on_delete=models.PROTECT, blank=True, null=True, related_name='person_from')
    person_to = models.ForeignKey(Person, on_delete=models.PROTECT, blank=True, null=True, related_name='person_to')
    qty = models.PositiveIntegerField(default=1)
    comment = models.CharField(max_length=70, blank=True)


class DocIncome(Document):
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT, blank=True, null=True)
    devices = models.ManyToManyField(Device, through='DocIncomeTableUnit')
    _REG_LIST = ['RegDeviceStock']
    _FOLLOWER_TYPES = [DocWriteoff]
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

    class Meta:
        verbose_name_plural = 'Оприходования'
        verbose_name = 'Оприходование'


class DocIncomeTableUnit(DocumentTableUnit):
    doc = models.ForeignKey(DocIncome, on_delete=models.CASCADE, related_name='table_unit')
    device = models.ForeignKey(Device, on_delete=models.PROTECT, blank=True, null=True)
    person = models.ForeignKey(Person, on_delete=models.PROTECT, blank=True, null=True)
    qty = models.PositiveIntegerField(default=1)
    comment = models.CharField(max_length=70, blank=True)


class DocInventory(Document):
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT, blank=True, null=True)
    devices = models.ManyToManyField(Device, through='DocInventoryTableUnit')
    _FOLLOWER_TYPES = [DocIncome, DocWriteoff, DocMove]
    _REG_LIST = []
    _TABLE_UNIT_EXIST = True
    _REG_DOC_ATTR_MAP = {
    }
    _REG_TU_ATTR_MAP = {
    }
    _REG_CONST_ATTR_MAP = {
    }

    # For django template
    def doc_inventory_fill_saldo(self, department, stock=None):
        start = time.time()
        table_unit = []
        for device in Device.objects.all():
            location = RegDeviceStock.objects.current_location(device=device, date=self.doc_date)
            if (location['department'] == department) and (location['qty'] == 1) and ((location['stock'] == stock) or (stock is not None)):
                table_unit.append({
                    'device': device,
                    'person_accountg': location['person'],
                    'qty_accountg': location['qty'],
                    'person_fact': location['person'],
                    'stock_fact': location['stock'],
                    'qty_fact': location['qty'],
                    'id': None,
                })
        print('doc_inventory_fill_saldo_TOTAL: %s' % str(time.time() - start))
        return table_unit

    # For API
    def fill_saldo(self, department, stock=None):
        def get_instance_pk(value):
            return value.id if value is not None else None

        table_unit = []
        for device in Device.objects.all():
            location = RegDeviceStock.objects.current_location(device=device, date=self.doc_date)
            if (location['department'] == department) and (location['qty'] == 1) and ((stock is None) or location['stock'] == stock):
                table_unit.append({
                    'device': get_instance_pk(device),
                    'person_accountg': get_instance_pk(location['person']),
                    'qty_accountg': location['qty'],
                    'person_fact': get_instance_pk(location['person']),
                    'stock_fact': get_instance_pk(location['stock']),
                    'qty_fact': location['qty'],
                    'id': None,
                })
        return table_unit

    def follower_create(self, model_follower):
        table_unit = []
        doc_leader = self
        for rec in doc_leader.get_table_unit():
            qty_diff = rec.qty_fact - rec.qty_accountg
            if (qty_diff > 0) & (model_follower == DocIncome):
                table_unit.append({
                    'device': rec.device,
                    'person': rec.person_fact,
                    'qty': qty_diff,
                    'comment': rec.comment,
                    'id': None,
                })
            elif (qty_diff < 0) & (model_follower == DocWriteoff):
                table_unit.append({
                    'device': rec.device,
                    'person': rec.person_accountg,
                    'qty': qty_diff * -1,
                    'comment': rec.comment,
                    'id': None,
                })
            elif (qty_diff == 0) & (model_follower == DocMove) & ((doc_leader.stock != rec.stock_fact) or (rec.person_accountg != rec.person_fact)):
                print('MOVE')
                table_unit_rec = {
                    'device': rec.device,
                    'person_from': rec.person_accountg,
                    'person_to': rec.person_fact,
                    'qty': rec.qty_fact,
                    'comment': rec.comment,
                    'id': None,
                }
                stock_to_flag = False
                for row in table_unit:
                    if row['stock_to']:
                        if row['stock_to'] == rec.stock_fact:
                            row['table_unit'].append(table_unit_rec)
                            stock_to_flag = True
                if not stock_to_flag:
                    table_unit.append({'stock_to': rec.stock_fact, 'table_unit': [table_unit_rec, ]})

        if model_follower == DocMove:
            doc_follower_id = []
            for row in table_unit:
                doc_attr = {
                    'doc_date': doc_leader.doc_date,
                    'doc_num': model_follower.objects.get_doc_num(),
                    'department_from': doc_leader.department,
                    'department_to': doc_leader.department,
                    'stock_from': doc_leader.stock,
                    'stock_to': row['stock_to'],
                }
                doc_follower = model_follower()
                doc_follower.doc_write(doc_attr=doc_attr, table_unit=row['table_unit'])
                doc_follower.set_leader(doc_leader)
                doc_follower_id.append({'name': str(doc_follower), 'id': doc_follower.id})
            return doc_follower_id

        doc_attr = {
            'doc_date': doc_leader.doc_date,
            'doc_num': model_follower.objects.get_doc_num(),
            'department': doc_leader.department,
            'stock': doc_leader.stock,
        }
        doc_follower = model_follower()
        doc_follower.doc_write(doc_attr=doc_attr, table_unit=table_unit)
        doc_follower.set_leader(doc_leader)
        return [{'name': str(doc_follower), 'id': doc_follower.id}]

    class Meta:
        verbose_name_plural = 'Инвентаризации'
        verbose_name = 'Инвентаризация'


class DocInventoryTableUnit(DocumentTableUnit):
    doc = models.ForeignKey(DocInventory, on_delete=models.CASCADE, related_name='table_unit')
    device = models.ForeignKey(Device, on_delete=models.PROTECT, blank=True, null=True)

    person_accountg = models.ForeignKey(Person, on_delete=models.PROTECT, blank=True, null=True, related_name='person_accountg')
    qty_accountg = models.PositiveIntegerField(default=1)

    person_fact = models.ForeignKey(Person, on_delete=models.PROTECT, blank=True, null=True, related_name='person_fact')
    stock_fact = models.ForeignKey(Stock, on_delete=models.PROTECT, blank=True, null=True, related_name='stock_fact')
    qty_fact = models.PositiveIntegerField(default=1)

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
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT, blank=True, null=True, default='')
    device = models.ForeignKey(Device, on_delete=models.PROTECT)
    person = models.ForeignKey(Person, on_delete=models.PROTECT, blank=True, null=True, default='')
    qty = models.PositiveIntegerField()
    objects = RegDeviceStockManager()

    def check_rec(self):
        errors = []

        if self.operation_type == '+':
            saldo = RegDeviceStock.objects.saldo(device=self.device, date_to=self.reg_date)
            if saldo > 0:
                errors.append('Устройство %s было оприходовано ранее и на дату %s еще не списано.' % (self.device, self.reg_date.strftime('%d.%m.%Y %H:%M:%S')))
                return (False, errors)

        if self.operation_type == '-':
            saldo = RegDeviceStock.objects.saldo(device=self.device, date_to=self.reg_date, department=self.department)
            if saldo <= 0:
                errors.append('Устройство %s не закреплено за подразделением %s на дату %s.' % (self.device, self.department, self.reg_date.strftime('%d.%m.%Y %H:%M:%S')))
                return (False, errors)

        return (True, [])

    def __str__(self):
        return self.operation_type + ' ' + str(self.base_doc)
