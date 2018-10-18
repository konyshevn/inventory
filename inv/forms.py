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
    fields=['device', 'person', 'qty', 'comment'], can_delete=True)




#class DocIncomeTableUnitFormSet(DocIncomeTableUnitFormSetBase):
