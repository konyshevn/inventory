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
    fields=['device', 'person', 'qty', 'comment'], can_delete=True, extra=1)


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
    fields=['device', 'person', 'qty', 'comment'], can_delete=True)


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
    fields=['device', 'person_from', 'person_to', 'qty', 'comment'], can_delete=True)
#class DocIncomeTableUnitFormSet(DocIncomeTableUnitFormSetBase):
