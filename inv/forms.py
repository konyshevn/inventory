from django import forms
from django.forms import ModelForm, modelformset_factory
from inv.models import *


class DocIncomeForm(ModelForm):
    class Meta:
        model = DocIncome
        fields = ['doc_num', 'doc_date', 'department', 'stock']
        labels = {
            'doc_date': 'Дата',
            'doc_num': 'Номер',
            'department': 'Подразделение',
            'stock': 'Склад'}


DocIncomeTableUnitFormSet = modelformset_factory(
    DocIncomeTableUnit,
    form=DocIncomeForm,
    labels={
        'device': 'Устройство',
        'person': 'Сотрудник',
        'qty': 'Количество',
        'comment': 'Комментарий'},
    fields=['device', 'person', 'qty', 'comment'], can_delete=True, extra=5)


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
