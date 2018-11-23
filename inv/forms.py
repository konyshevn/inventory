from django import forms
from django.forms import ModelForm, modelformset_factory
from inv.models import *
import datetime


def device_list():
    defaul_val = [('', '-----')]
    devices = [(device.id, device) for device in Device.objects.all()]
    devices = defaul_val + devices
    return devices


def department_list():
    defaul_val = [('', '-----')]
    departments = [(department, department) for department in Department.objects.all()]
    departments = defaul_val + departments
    return departments


class ReportCurrentLocationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ReportCurrentLocationForm, self).__init__(*args, **kwargs)
        self.fields['device'] = forms.CharField(required=False, label='Устройство', widget=forms.widgets.Select(choices=device_list()))
        self.fields['department'] = forms.CharField(required=False, label='Подразделение', widget=forms.widgets.Select(choices=department_list()))

    date_to = forms.DateTimeField(required=True, label='Дата', input_formats=('%d.%m.%Y',), widget=forms.DateTimeInput(format=('%d.%m.%Y',), attrs={'type': 'datetime-local'}))


class DocIncomeForm(ModelForm):
    class Meta:
        model = DocIncome
        fields = ['doc_num', 'doc_date', 'department', 'stock']
        labels = {
            'doc_date': 'Дата',
            'doc_num': 'Номер',
            'department': 'Подразделение',
            'stock': 'Склад'}
        widgets = {'doc_date': forms.DateTimeInput}


DocIncomeTableUnitFormSet = modelformset_factory(
    DocIncomeTableUnit,
    form=DocIncomeForm,
    labels={
        'device': 'Устройство',
        'person': 'Сотрудник',
        'qty': 'Количество',
        'comment': 'Комментарий'},
    fields=['device', 'person', 'qty', 'comment'], can_delete=True, extra=5,
    widgets={'device': forms.Select, }
    )


class DocWriteoffForm(ModelForm):
    class Meta:
        model = DocWriteoff
        fields = ['doc_num', 'doc_date', 'department', 'stock']
        labels = {
            'doc_date': 'Дата',
            'doc_num': 'Номер',
            'department': 'Подразделение',
            'stock': 'Склад'}


DocWriteoffTableUnitFormSet = modelformset_factory(
    DocWriteoffTableUnit,
    form=DocWriteoffForm,
    labels={
        'device': 'Устройство',
        'person': 'Сотрудник',
        'qty': 'Количество',
        'comment': 'Комментарий'},
    fields=['device', 'person', 'qty', 'comment'], can_delete=True, extra=5)


class DocMoveForm(ModelForm):
    class Meta:
        model = DocMove
        fields = ['doc_num', 'doc_date', 'department_from', 'department_to', 'stock_from', 'stock_to']
        labels = {
            'doc_date': 'Дата',
            'doc_num': 'Номер',
            'department_from': 'Подразделение отправитель',
            'department_to': 'Подразделение получатель',
            'stock_from': 'Склад отправитель',
            'stock_to': 'Склад получатель'}


DocMoveTableUnitFormSet = modelformset_factory(
    DocMoveTableUnit,
    form=DocMoveForm,
    labels={
        'device': 'Устройство',
        'person_from': 'Сотрудник отправитель',
        'person_to': 'Сотрудник получатель',
        'qty': 'Количество',
        'comment': 'Комментарий'},
    fields=['device', 'person_from', 'person_to', 'qty', 'comment'], can_delete=True, extra=5)


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
