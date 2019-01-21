from django import forms
from django.forms import ModelForm, modelformset_factory
from inv.models import *
import datetime
from inv.selectize_widget import ModelSelectizeWidget


class DeviceTypeSelectizeWidget(ModelSelectizeWidget):
    model = DeviceType
    search_fields = ['name__icontains']


class NomenclatureSelectizeWidget(ModelSelectizeWidget):
    model = Nomenclature
    search_fields = ['name__icontains']


class DepartmentSelectizeWidget(ModelSelectizeWidget):
    model = Department
    search_fields = ['name__icontains']


class StockSelectizeWidget(ModelSelectizeWidget):
    model = Stock
    search_fields = ['name__icontains']


class PersonSelectizeWidget(ModelSelectizeWidget):
    model = Person
    search_fields = ['name__icontains', 'surname__icontains']


class DeviceSelectizeWidget(ModelSelectizeWidget):
    model = Device
    search_fields = ['name__name__icontains', 'inv_num__icontains', 'serial_num__icontains']


class UploadFileForm(forms.Form):
    date = forms.DateTimeField(required=True, label='Дата нового оприходования', input_formats=('%d.%m.%Y %H:%M:%S',), widget=forms.DateTimeInput(format=('%d.%m.%Y %H:%M:%S',), attrs={'type': 'datetime-local'}))
    file = forms.FileField(label='Файл')


def device_list():
    defaul_val = [('', '-----')]
    devices = [(device.id, device) for device in Device.objects.all()]
    devices = defaul_val + devices
    return devices


class ReportCurrentLocationForm(forms.Form):
    device = forms.CharField(required=False, label='Устройство', widget=DeviceSelectizeWidget)
    department = forms.CharField(required=False, label='Подразделение', widget=DepartmentSelectizeWidget)
    stock = forms.CharField(required=False, label='Склад', widget=StockSelectizeWidget)
    person = forms.CharField(required=False, label='Сотрудник', widget=PersonSelectizeWidget)
    
    current_date = datetime.datetime.now().replace(tzinfo=tz.tzutc()).astimezone(tz=None).strftime('%d.%m.%Y')
    date_to = forms.DateTimeField(required=True, label='Дата', initial=current_date, input_formats=('%d.%m.%Y',), widget=forms.DateTimeInput(format=('%d.%m.%Y',), attrs={'type': 'datetime-local'}))


class ReportStatementDocsForm(forms.Form):
    #def __init__(self, *args, **kwargs):
    #    super(ReportStatementDocsForm, self).__init__(*args, **kwargs)
    #    self.fields['device'] = forms.CharField(required=True, label='Устройство', widget=forms.widgets.Select(choices=device_list()))
    device = forms.CharField(required=True, label='Устройство', widget=DeviceSelectizeWidget)
    date_from = forms.DateTimeField(required=False, label='Дата начала', input_formats=('%d.%m.%Y',), widget=forms.DateTimeInput(format=('%d.%m.%Y',), attrs={'type': 'datetime-local'}))
    date_to = forms.DateTimeField(required=False, label='Дата окончания', input_formats=('%d.%m.%Y',), widget=forms.DateTimeInput(format=('%d.%m.%Y',), attrs={'type': 'datetime-local'}))


class DocIncomeForm(ModelForm):
    class Meta:
        model = DocIncome
        fields = ['doc_num', 'doc_date', 'department', 'stock', 'comment']
        labels = {
            'doc_date': 'Дата',
            'doc_num': 'Номер',
            'department': 'Подразделение',
            'stock': 'Склад',
            'comment': 'Комментарий', }
        widgets = {
            'doc_date': forms.DateTimeInput,
            'department': DepartmentSelectizeWidget,
            'stock': StockSelectizeWidget,
        }


DocIncomeTableUnitFormSet = modelformset_factory(
    DocIncomeTableUnit,
    form=DocIncomeForm,
    labels={
        'device': 'Устройство',
        'person': 'Сотрудник',
        'qty': 'Количество',
        'comment': 'Комментарий'},
    fields=['device', 'person', 'qty', 'comment'], can_delete=True, extra=5,
    widgets={
        'device': DeviceSelectizeWidget,
        'person': PersonSelectizeWidget,
    },
)


class DocWriteoffForm(ModelForm):
    class Meta:
        model = DocWriteoff
        fields = ['doc_num', 'doc_date', 'department', 'stock', 'comment']
        labels = {
            'doc_date': 'Дата',
            'doc_num': 'Номер',
            'department': 'Подразделение',
            'stock': 'Склад',
            'comment': 'Комментарий',
        }
        widgets = {
            'doc_date': forms.DateTimeInput,
            'department': DepartmentSelectizeWidget,
            'stock': StockSelectizeWidget,
        }


DocWriteoffTableUnitFormSet = modelformset_factory(
    DocWriteoffTableUnit,
    form=DocWriteoffForm,
    labels={
        'device': 'Устройство',
        'person': 'Сотрудник',
        'qty': 'Количество',
        'comment': 'Комментарий'},
    fields=['device', 'person', 'qty', 'comment'],
    can_delete=True,
    extra=5,
    widgets={
        'device': DeviceSelectizeWidget,
        'person': PersonSelectizeWidget,
    }
)


class DocMoveForm(ModelForm):
    class Meta:
        model = DocMove
        fields = ['doc_num', 'doc_date', 'department_from', 'department_to', 'stock_from', 'stock_to', 'comment']
        labels = {
            'doc_date': 'Дата',
            'doc_num': 'Номер',
            'department_from': 'Подразделение отправитель',
            'department_to': 'Подразделение получатель',
            'stock_from': 'Склад отправитель',
            'stock_to': 'Склад получатель',
            'comment': 'Комментарий',
        }
        widgets = {
            'doc_date': forms.DateTimeInput,
            'department_from': DepartmentSelectizeWidget,
            'stock_from': StockSelectizeWidget,
            'department_to': DepartmentSelectizeWidget,
            'stock_to': StockSelectizeWidget,
        }


DocMoveTableUnitFormSet = modelformset_factory(
    DocMoveTableUnit,
    form=DocMoveForm,
    labels={
        'device': 'Устройство',
        'person_from': 'Сотрудник отправитель',
        'person_to': 'Сотрудник получатель',
        'qty': 'Количество',
        'comment': 'Комментарий'},
    fields=['device', 'person_from', 'person_to', 'qty', 'comment'],
    can_delete=True,
    extra=5,
    widgets={
        'device': DeviceSelectizeWidget,
        'person_from': PersonSelectizeWidget,
        'person_to': PersonSelectizeWidget,
    },
)


class DocInventoryForm(ModelForm):
    class Meta:
        model = DocInventory
        fields = ['doc_num', 'doc_date', 'department', 'stock', 'comment']
        labels = {
            'doc_date': 'Дата',
            'doc_num': 'Номер',
            'department': 'Подразделение',
            'stock': 'Склад',
            'comment': 'Комментарий',
        }
        widgets = {
            'doc_date': forms.DateTimeInput,
            'department': DepartmentSelectizeWidget,
            'stock': StockSelectizeWidget,
        }


DocInventoryTableUnitFormSet = modelformset_factory(
    DocInventoryTableUnit,
    form=DocInventoryForm,
    labels={
        'device': 'Устройство',
        'person_accountg': 'Сотрудник (учет)',
        'qty_accountg': 'Количество (учет)',

        'person_fact': 'Сотрудник (факт)',
        'stock_fact': 'Склад (факт)',
        'qty_fact': 'Количество (факт)',

        'comment': 'Комментарий'},
    fields=['device', 'person_accountg', 'qty_accountg', 'person_fact', 'stock_fact', 'qty_fact', 'comment'],
    can_delete=True,
    extra=5,
    widgets={
        'device': DeviceSelectizeWidget,
        'person_accountg': PersonSelectizeWidget,
        'person_fact': PersonSelectizeWidget,
        'stock_fact': StockSelectizeWidget,
    },
)


class DeviceForm(ModelForm):
    class Meta:
        model = Device
        fields = ['device_type', 'name', 'serial_num', 'inv_num', 'comment']
        labels = {
            'device_type': 'Тип',
            'name': 'Наименование',
            'serial_num': 'Серийный номер',
            'inv_num': 'Инвентарный номер',
            'comment': 'Комментарий'}
        widgets = {
        'device_type': DeviceTypeSelectizeWidget,
        'name': NomenclatureSelectizeWidget,
        }


class DeviceTypeForm(ModelForm):
    class Meta:
        model = DeviceType
        fields = ['name']
        labels = {
            'name': 'Наименование'}


class NomenclatureForm(ModelForm):
    class Meta:
        model = Nomenclature
        fields = ['name']
        labels = {
            'name': 'Наименование'}


class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = ['name']
        labels = {
            'name': 'Наименование'}


class StockForm(ModelForm):
    class Meta:
        model = Stock
        fields = ['name']
        labels = {
            'name': 'Наименование'}




class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ['surname', 'name', 'department']
        labels = {
            'surname': 'Фамилия',
            'name': 'Имя',
            'department': 'Подразделение'}
        widgets = {'department': DepartmentSelectizeWidget, }


class RegDeviceStockForm(ModelForm):
    class Meta:
        model = RegDeviceStock
        fields = ['operation_type', 'reg_date', 'department', 'stock', 'person', 'qty']
        labels = {
            'operation_type': 'Операция',
#            'base_doc': 'Документ-основание',
            'reg_date': 'Дата',
            'department': 'Подразделение',
            'stock': 'Склад',
            'person': 'Сотрудник',
            'qty': 'Количество'}
